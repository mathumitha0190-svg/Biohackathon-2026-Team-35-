from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import MODEL_ARTIFACT_PATH, MODEL_METRICS_PATH, MODELS_DIR, REPORTS_DIR
from .data import MODEL_FEATURES, TARGET, model_input_frame


@dataclass(frozen=True)
class PredictionResult:
    tier: str
    probability: float
    risk_tier: str
    top_drivers: list[tuple[str, float]]


def make_pipeline(features: list[str]) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                features,
            )
        ],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=2000,
                    solver="liblinear",
                    random_state=42,
                ),
            ),
        ]
    )


def risk_tier(probability: float) -> str:
    if probability >= 0.65:
        return "High"
    if probability >= 0.35:
        return "Medium"
    return "Low"


def threshold_table(y_true: np.ndarray, probabilities: np.ndarray) -> list[dict[str, float]]:
    rows = []
    for threshold in [0.25, 0.35, 0.5, 0.65, 0.75]:
        preds = (probabilities >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, preds, labels=[0, 1]).ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) else 0.0
        specificity = tn / (tn + fp) if (tn + fp) else 0.0
        rows.append(
            {
                "threshold": threshold,
                "sensitivity": sensitivity,
                "specificity": specificity,
                "f1": f1_score(y_true, preds, zero_division=0),
            }
        )
    return rows


def evaluate(y_true: np.ndarray, probabilities: np.ndarray) -> dict:
    preds = (probabilities >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, preds, labels=[0, 1]).ravel()
    sensitivity = tp / (tp + fn) if (tp + fn) else 0.0
    specificity = tn / (tn + fp) if (tn + fp) else 0.0
    return {
        "auroc": roc_auc_score(y_true, probabilities),
        "auprc": average_precision_score(y_true, probabilities),
        "sensitivity": sensitivity,
        "specificity": specificity,
        "f1": f1_score(y_true, preds, zero_division=0),
        "brier_score": brier_score_loss(y_true, probabilities),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "threshold_table": threshold_table(y_true, probabilities),
    }


def train_models(df: pd.DataFrame) -> tuple[dict, dict]:
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df[TARGET],
        random_state=42,
    )

    models = {}
    metrics = {
        "row_counts": {
            "train": int(len(train_df)),
            "test": int(len(test_df)),
            "positive_total": int((df[TARGET] == 1).sum()),
            "negative_total": int((df[TARGET] == 0).sum()),
        },
        "tiers": {},
    }

    for tier, features in MODEL_FEATURES.items():
        pipeline = make_pipeline(features)
        pipeline.fit(train_df[features], train_df[TARGET])
        probabilities = pipeline.predict_proba(test_df[features])[:, 1]
        models[tier] = {"pipeline": pipeline, "features": features}
        metrics["tiers"][tier] = evaluate(test_df[TARGET].to_numpy(), probabilities)

    artifact = {
        "models": models,
        "metrics": metrics,
        "feature_sets": MODEL_FEATURES,
        "target": TARGET,
    }
    return artifact, metrics


def save_artifacts(artifact: dict, metrics: dict, artifact_path: Path = MODEL_ARTIFACT_PATH) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, artifact_path)
    MODEL_METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def load_artifact(path: Path = MODEL_ARTIFACT_PATH) -> dict:
    return joblib.load(path)


def predict_patient(artifact: dict, patient: dict, tier: str) -> PredictionResult:
    model_info = artifact["models"][tier]
    frame = model_input_frame(patient, tier)
    probability = float(model_info["pipeline"].predict_proba(frame)[0, 1])
    drivers = top_coefficient_drivers(model_info["pipeline"], frame, model_info["features"])
    return PredictionResult(tier, probability, risk_tier(probability), drivers)


def top_coefficient_drivers(pipeline: Pipeline, frame: pd.DataFrame, features: list[str], n: int = 5) -> list[tuple[str, float]]:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    transformed = preprocessor.transform(frame)
    contributions = transformed[0] * model.coef_[0]
    ranked = sorted(
        zip(features, contributions),
        key=lambda item: abs(item[1]),
        reverse=True,
    )
    return [(feature, float(value)) for feature, value in ranked[:n]]
