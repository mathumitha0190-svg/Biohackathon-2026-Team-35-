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
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config import (
    MODEL_ARTIFACT_PATH,
    MODEL_METRICS_PATH,
    MODEL_REPORT_PATH,
    MODELS_DIR,
    REPORTS_DIR,
)
from .data import MODEL_FEATURES, TARGET, model_input_frame


REQUIRED_CI_METRICS = [
    "auroc",
    "auprc",
    "sensitivity",
    "specificity",
    "f1",
    "brier_score",
]


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
    for threshold in np.round(np.arange(0.05, 1.0, 0.05), 2):
        preds = (probabilities >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true, preds, labels=[0, 1]).ravel()
        sensitivity = tp / (tp + fn) if (tp + fn) else 0.0
        specificity = tn / (tn + fp) if (tn + fp) else 0.0
        rows.append(
            {
                "threshold": float(threshold),
                "sensitivity": sensitivity,
                "specificity": specificity,
                "f1": f1_score(y_true, preds, zero_division=0),
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp),
            }
        )
    return rows


def metric_values(y_true: np.ndarray, probabilities: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    preds = (probabilities >= threshold).astype(int)
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
    }


def bootstrap_confidence_intervals(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    threshold: float = 0.5,
    n_bootstrap: int = 500,
    random_state: int = 42,
) -> dict[str, dict[str, float]]:
    rng = np.random.default_rng(random_state)
    values = {metric: [] for metric in REQUIRED_CI_METRICS}
    indices = np.arange(len(y_true))

    for _ in range(n_bootstrap):
        sample_indices = rng.choice(indices, size=len(indices), replace=True)
        sample_y = y_true[sample_indices]
        sample_probabilities = probabilities[sample_indices]
        if len(np.unique(sample_y)) < 2:
            continue
        sample_metrics = metric_values(sample_y, sample_probabilities, threshold)
        for metric in REQUIRED_CI_METRICS:
            values[metric].append(sample_metrics[metric])

    return {
        metric: {
            "low": float(np.percentile(metric_values_list, 2.5)),
            "high": float(np.percentile(metric_values_list, 97.5)),
        }
        for metric, metric_values_list in values.items()
        if metric_values_list
    }


def calibration_bins(y_true: np.ndarray, probabilities: np.ndarray, n_bins: int = 5) -> list[dict[str, float | int]]:
    frame = pd.DataFrame({"y_true": y_true, "probability": probabilities})
    frame["bin"] = pd.cut(
        frame["probability"],
        bins=np.linspace(0, 1, n_bins + 1),
        include_lowest=True,
        right=True,
    )
    rows = []
    for interval, group in frame.groupby("bin", observed=True):
        if group.empty:
            continue
        rows.append(
            {
                "bin_lower": float(interval.left),
                "bin_upper": float(interval.right),
                "n": int(len(group)),
                "mean_predicted": float(group["probability"].mean()),
                "observed_rate": float(group["y_true"].mean()),
            }
        )
    return rows


def select_screening_threshold(table: list[dict[str, float]]) -> dict[str, float | str]:
    eligible = [row for row in table if row["sensitivity"] >= 0.85]
    if eligible:
        selected = max(eligible, key=lambda row: (row["specificity"], row["threshold"]))
        reason = "highest specificity while maintaining sensitivity >= 0.85"
    else:
        selected = max(table, key=lambda row: (row["sensitivity"], row["specificity"]))
        reason = "no threshold reached sensitivity >= 0.85; selected best available sensitivity"
    return {**selected, "reason": reason}


def subgroup_metrics(test_df: pd.DataFrame, y_true: np.ndarray, probabilities: np.ndarray) -> dict:
    frame = test_df[["age", "bmi"]].copy()
    frame["y_true"] = y_true
    frame["probability"] = probabilities
    subgroup_specs = {
        "bmi_group": pd.cut(
            frame["bmi"],
            bins=[-np.inf, 25, 30, np.inf],
            labels=["<25", "25-29.9", ">=30"],
            right=False,
        ),
        "age_group": pd.cut(
            frame["age"],
            bins=[-np.inf, 25, 35, np.inf],
            labels=["<25", "25-34", ">=35"],
            right=False,
        ),
    }

    results = {}
    for subgroup_name, labels in subgroup_specs.items():
        frame[subgroup_name] = labels
        results[subgroup_name] = {}
        for label, group in frame.groupby(subgroup_name, observed=False):
            label_key = str(label)
            y_group = group["y_true"].to_numpy()
            probability_group = group["probability"].to_numpy()
            positive_count = int((y_group == 1).sum())
            result = {
                "n": int(len(group)),
                "positive_count": positive_count,
                "insufficient": False,
            }
            if len(group) < 20:
                result.update(
                    {
                        "insufficient": True,
                        "reason": "n < 20",
                    }
                )
            elif len(np.unique(y_group)) < 2:
                result.update(
                    {
                        "insufficient": True,
                        "reason": "only one class present",
                    }
                )
            else:
                result.update(metric_values(y_group, probability_group))
            results[subgroup_name][label_key] = result
    return results


def evaluate(y_true: np.ndarray, probabilities: np.ndarray, test_df: pd.DataFrame) -> dict:
    base_metrics = metric_values(y_true, probabilities)
    table = threshold_table(y_true, probabilities)
    preds = (probabilities >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, preds, labels=[0, 1]).ravel()
    return {
        **base_metrics,
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "threshold_table": table,
        "selected_threshold": select_screening_threshold(table),
        "confidence_intervals": bootstrap_confidence_intervals(y_true, probabilities),
        "calibration_bins": calibration_bins(y_true, probabilities),
        "subgroup_metrics": subgroup_metrics(test_df, y_true, probabilities),
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
        metrics["tiers"][tier] = evaluate(test_df[TARGET].to_numpy(), probabilities, test_df)

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
    MODEL_REPORT_PATH.write_text(metrics_to_markdown(metrics), encoding="utf-8")


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


def format_ci(metric: str, metrics: dict) -> str:
    ci = metrics["confidence_intervals"].get(metric)
    if not ci:
        return "n/a"
    return f"{metrics[metric]:.3f} ({ci['low']:.3f}-{ci['high']:.3f})"


def metrics_to_markdown(metrics: dict) -> str:
    lines = [
        "# PCOS Navigator Model Report",
        "",
        "This report is generated by `uv run python scripts/train_models.py`.",
        "",
        "## Dataset Split",
        "",
        f"- Training rows: {metrics['row_counts']['train']}",
        f"- Test rows: {metrics['row_counts']['test']}",
        f"- PCOS positive total: {metrics['row_counts']['positive_total']}",
        f"- PCOS negative total: {metrics['row_counts']['negative_total']}",
        "",
        "## Tier Comparison",
        "",
        "| Tier | AUROC (95% CI) | AUPRC (95% CI) | Sensitivity (95% CI) | Specificity (95% CI) | Brier (95% CI) | Selected threshold |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for tier, tier_metrics in metrics["tiers"].items():
        selected = tier_metrics["selected_threshold"]
        lines.append(
            "| "
            + " | ".join(
                [
                    tier,
                    format_ci("auroc", tier_metrics),
                    format_ci("auprc", tier_metrics),
                    format_ci("sensitivity", tier_metrics),
                    format_ci("specificity", tier_metrics),
                    format_ci("brier_score", tier_metrics),
                    f"{selected['threshold']:.2f}",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Selected Screening Thresholds",
            "",
            "| Tier | Threshold | Sensitivity | Specificity | Reason |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for tier, tier_metrics in metrics["tiers"].items():
        selected = tier_metrics["selected_threshold"]
        lines.append(
            f"| {tier} | {selected['threshold']:.2f} | {selected['sensitivity']:.3f} | {selected['specificity']:.3f} | {selected['reason']} |"
        )

    lines.extend(
        [
            "",
            "## Subgroup Caveats",
            "",
            "Subgroup rows with `n < 20` or only one outcome class are marked as insufficient and should not be overinterpreted.",
            "",
        ]
    )
    for tier, tier_metrics in metrics["tiers"].items():
        lines.append(f"### {tier.title()}")
        lines.append("")
        lines.append("| Group | Segment | n | Positive | Status | AUROC |")
        lines.append("|---|---|---:|---:|---|---:|")
        for group_name, group_metrics in tier_metrics["subgroup_metrics"].items():
            for segment, segment_metrics in group_metrics.items():
                status = segment_metrics.get("reason", "ok")
                auroc = segment_metrics.get("auroc")
                auroc_text = "n/a" if auroc is None else f"{auroc:.3f}"
                lines.append(
                    f"| {group_name} | {segment} | {segment_metrics['n']} | {segment_metrics['positive_count']} | {status} | {auroc_text} |"
                )
        lines.append("")

    lines.extend(
        [
            "## Dataset Limitations",
            "",
            "- This is a retrospective hackathon dataset with 541 labeled rows.",
            "- The model should be treated as triage support, not a diagnostic device.",
            "- External prospective validation is required before clinical deployment.",
            "- Subgroup results are descriptive only because test-set groups are small.",
        ]
    )
    return "\n".join(lines) + "\n"
