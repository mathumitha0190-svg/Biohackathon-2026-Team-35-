from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .config import PCOS_WORKBOOK


TARGET = "pcos"
IDENTIFIER_COLUMNS = {"sl_no", "patient_file_no"}
EXCLUDED_MODEL_COLUMNS = {
    "blood_group",
    "pregnant",
    "i_beta_hcg",
    "ii_beta_hcg",
    "marraige_status",
    "no_of_abortions",
}

COLUMN_RENAMES = {
    "pcos_y_n": "pcos",
    "age_yrs": "age",
    "weight_kg": "weight_kg",
    "height_cm": "height_cm",
    "bmi": "bmi",
    "blood_group": "blood_group",
    "pulse_rate_bpm": "pulse_rate",
    "rr_breaths_min": "respiratory_rate",
    "hb_g_dl": "hemoglobin",
    "cycle_r_i": "cycle",
    "cycle_length_days": "cycle_length",
    "marraige_status_yrs": "marraige_status",
    "pregnant_y_n": "pregnant",
    "no_of_abortions": "no_of_abortions",
    "i_beta_hcg_miu_ml": "i_beta_hcg",
    "ii_beta_hcg_miu_ml": "ii_beta_hcg",
    "fsh_miu_ml": "fsh",
    "lh_miu_ml": "lh",
    "fsh_lh": "fsh_lh_ratio",
    "hip_inch": "hip",
    "waist_inch": "waist",
    "waist_hip_ratio": "waist_hip_ratio",
    "tsh_miu_l": "tsh",
    "amh_ng_ml": "amh",
    "prl_ng_ml": "prl",
    "vit_d3_ng_ml": "vit_d3",
    "prg_ng_ml": "prg",
    "rbs_mg_dl": "rbs",
    "weight_gain_y_n": "weight_gain",
    "hair_growth_y_n": "hair_growth",
    "skin_darkening_y_n": "skin_darkening",
    "hair_loss_y_n": "hair_loss",
    "pimples_y_n": "pimples",
    "fast_food_y_n": "fast_food",
    "reg_exercise_y_n": "regular_exercise",
    "bp_systolic_mmhg": "bp_systolic",
    "bp_diastolic_mmhg": "bp_diastolic",
    "follicle_no_l": "follicle_no_l",
    "follicle_no_r": "follicle_no_r",
    "avg_f_size_l_mm": "avg_f_size_l",
    "avg_f_size_r_mm": "avg_f_size_r",
    "endometrium_mm": "endometrium",
}

BINARY_COLUMNS = [
    "pregnant",
    "weight_gain",
    "hair_growth",
    "skin_darkening",
    "hair_loss",
    "pimples",
    "fast_food",
    "regular_exercise",
]

HISTORY_FEATURES = [
    "age",
    "weight_kg",
    "height_cm",
    "bmi",
    "cycle",
    "cycle_length",
    "weight_gain",
    "hair_growth",
    "skin_darkening",
    "hair_loss",
    "pimples",
]

BASIC_CLINICAL_FEATURES = HISTORY_FEATURES + [
    "bp_systolic",
    "bp_diastolic",
    "rbs",
    "tsh",
    "prl",
    "fsh",
    "lh",
    "hemoglobin",
    "waist",
    "hip",
    "waist_hip_ratio",
]

FULL_DIAGNOSTIC_FEATURES = BASIC_CLINICAL_FEATURES + [
    "amh",
    "follicle_no_l",
    "follicle_no_r",
    "avg_f_size_l",
    "avg_f_size_r",
    "endometrium",
]

MODEL_FEATURES = {
    "history": HISTORY_FEATURES,
    "basic": BASIC_CLINICAL_FEATURES,
    "full": FULL_DIAGNOSTIC_FEATURES,
}


@dataclass(frozen=True)
class DataProfile:
    row_count: int
    positive_count: int
    negative_count: int
    cycle_counts: dict[str, int]
    missing_counts: dict[str, int]
    excluded_columns: list[str]
    feature_sets: dict[str, list[str]]


def slugify_column(name: str) -> str:
    cleaned = name.strip().lower()
    cleaned = cleaned.replace("β", "beta")
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return COLUMN_RENAMES.get(cleaned, cleaned)


def load_raw_pcos(path: Path = PCOS_WORKBOOK) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=1, engine="openpyxl")


def load_clean_pcos(path: Path = PCOS_WORKBOOK) -> pd.DataFrame:
    raw = load_raw_pcos(path)
    raw.columns = [slugify_column(str(column)) for column in raw.columns]

    df = raw[raw[TARGET].notna()].copy()
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")
    df = df[df[TARGET].isin([0, 1])].copy()
    df[TARGET] = df[TARGET].astype(int)

    for column in df.columns:
        if column == TARGET:
            continue
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Dataset audit showed Cycle(R/I): 2 is regular and 4 is irregular. The rare
    # value 5 is treated as missing to avoid creating a fake clinical category.
    df["cycle_raw"] = df["cycle"]
    df["cycle"] = df["cycle"].map({2: 0, 4: 1})

    for column in BINARY_COLUMNS:
        if column in df.columns:
            df[column] = df[column].where(df[column].isin([0, 1]), np.nan)

    if {"weight_kg", "height_cm"}.issubset(df.columns):
        height_m = df["height_cm"] / 100
        df["bmi_recomputed"] = df["weight_kg"] / (height_m**2)
        df["bmi_mismatch"] = (df["bmi"] - df["bmi_recomputed"]).abs()

    if {"fsh", "lh"}.issubset(df.columns):
        df["fsh_lh_recomputed"] = df["fsh"] / df["lh"].replace(0, np.nan)
        df["fsh_lh_mismatch"] = (df["fsh_lh_ratio"] - df["fsh_lh_recomputed"]).abs()

    if {"waist", "hip"}.issubset(df.columns):
        df["waist_hip_recomputed"] = df["waist"] / df["hip"].replace(0, np.nan)
        df["waist_hip_mismatch"] = (
            df["waist_hip_ratio"] - df["waist_hip_recomputed"]
        ).abs()

    return df


def build_data_profile(df: pd.DataFrame) -> DataProfile:
    missing_counts = {
        column: int(df[column].isna().sum())
        for column in sorted(set(sum(MODEL_FEATURES.values(), [])))
        if column in df.columns
    }
    cycle_counts = {
        str(key): int(value)
        for key, value in df["cycle_raw"].value_counts(dropna=False).sort_index().items()
    }
    excluded_columns = sorted(
        column
        for column in IDENTIFIER_COLUMNS.union(EXCLUDED_MODEL_COLUMNS)
        if column in df.columns
    )
    return DataProfile(
        row_count=int(len(df)),
        positive_count=int((df[TARGET] == 1).sum()),
        negative_count=int((df[TARGET] == 0).sum()),
        cycle_counts=cycle_counts,
        missing_counts=missing_counts,
        excluded_columns=excluded_columns,
        feature_sets=MODEL_FEATURES,
    )


def profile_to_markdown(profile: DataProfile, df: pd.DataFrame) -> str:
    lines = [
        "# PCOS Dataset Profile",
        "",
        "Generated from the second worksheet of `(Main_Dataset)_PCOS_data_without_infertility.xlsx`.",
        "",
        "## Row Counts",
        "",
        f"- Labeled rows: {profile.row_count}",
        f"- PCOS positive: {profile.positive_count}",
        f"- PCOS negative: {profile.negative_count}",
        "",
        "## Cycle Coding Audit",
        "",
        "Raw `Cycle(R/I)` values are preserved in `cycle_raw`; model input maps `2 -> regular/0` and `4 -> irregular/1`. Any other value is treated as missing.",
        "",
        "| Raw value | Count |",
        "|---|---:|",
    ]
    for value, count in profile.cycle_counts.items():
        lines.append(f"| {value} | {count} |")

    lines.extend(
        [
            "",
            "## Excluded Columns",
            "",
            ", ".join(f"`{column}`" for column in profile.excluded_columns),
            "",
            "## Feature Sets",
            "",
        ]
    )
    for tier, features in profile.feature_sets.items():
        lines.append(f"### {tier.title()}")
        lines.append("")
        lines.append(", ".join(f"`{feature}`" for feature in features))
        lines.append("")

    lines.extend(["## Missing Values In Model Features", "", "| Feature | Missing |", "|---|---:|"])
    for feature, missing in profile.missing_counts.items():
        lines.append(f"| `{feature}` | {missing} |")

    audit_columns = [
        ("bmi_mismatch", "BMI mismatch"),
        ("fsh_lh_mismatch", "FSH/LH ratio mismatch"),
        ("waist_hip_mismatch", "Waist:hip mismatch"),
    ]
    lines.extend(["", "## Derived Value Checks", "", "| Check | Median absolute mismatch | Max absolute mismatch |", "|---|---:|---:|"])
    for column, label in audit_columns:
        if column in df.columns:
            lines.append(
                f"| {label} | {df[column].median(skipna=True):.4f} | {df[column].max(skipna=True):.4f} |"
            )

    return "\n".join(lines) + "\n"


def available_model_tier(patient: dict[str, float | int | None]) -> str:
    def has_any(features: list[str]) -> bool:
        return any(patient.get(feature) is not None for feature in features)

    full_only = [feature for feature in FULL_DIAGNOSTIC_FEATURES if feature not in BASIC_CLINICAL_FEATURES]
    basic_only = [feature for feature in BASIC_CLINICAL_FEATURES if feature not in HISTORY_FEATURES]
    if has_any(full_only):
        return "full"
    if has_any(basic_only):
        return "basic"
    return "history"


def model_input_frame(patient: dict[str, float | int | None], tier: str) -> pd.DataFrame:
    return pd.DataFrame([{feature: patient.get(feature) for feature in MODEL_FEATURES[tier]}])
