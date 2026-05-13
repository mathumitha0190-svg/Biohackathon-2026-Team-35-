# PCOS Navigator

PCOS Navigator is a Streamlit demo MVP for evidence-based PCOS triage and diagnostic pathway support. It combines a resource-tiered logistic-regression model, guideline-style checklist, endometriosis red flags, and next-best-action recommendations.

> This tool supports triage and investigation planning. It is not a diagnosis.

## Setup

This repository uses `uv` because this machine does not currently have a working global Python installation.

```powershell
uv sync --dev
```

## Commands

Create the data audit:

```powershell
uv run python scripts/profile_data.py
```

Train the models and write metrics:

```powershell
uv run python scripts/train_models.py
```

Run the dashboard:

```powershell
uv run streamlit run app.py
```

Run tests:

```powershell
uv run pytest
```

Build a shareable presentation bundle:

```powershell
uv run python scripts/export_presentation.py
```

## Outputs

- `reports/data_profile.md`
- `reports/model_metrics.json`
- `reports/model_report.md`
- `models/pcos_models.joblib`
- `exports/pcos_navigator_presentation/`

Generated reports, model artifacts, and exports are ignored by git. Regenerate model evidence with:

```powershell
uv run python scripts/train_models.py
```

## Judge-Ready Evidence

The training command writes:

- bootstrap 95% confidence intervals for AUROC, AUPRC, sensitivity, specificity, F1, and Brier score
- calibration bins for the `4 Evidence` dashboard tab
- a selected screening threshold per model tier
- subgroup metrics by BMI group and age group, with small groups marked as insufficient
- `reports/model_report.md`, a human-readable model summary for presentation prep

## Presentation Kit

Committed judge-facing materials live in `docs/`:

- `docs/demo_script.md`
- `docs/slide_outline.md`
- `docs/case_cards.md`
- `docs/judging_map.md`

Recommended live demo flow:

1. Start the app with `uv run streamlit run app.py`.
2. Demo `Typical PCOS` to show the complete pathway.
3. Demo `Lean PCOS` to show normal-BMI PCOS handling.
4. Demo `Endometriosis-like` to show differential red flags.
5. Demo `Incomplete Data` to show low-resource fallback.
6. End on the `4 Evidence` tab with calibration, thresholds, and subgroup caveats.

The export command creates an ignored bundle at `exports/pcos_navigator_presentation/` and intentionally excludes datasets and model binaries.

## Dataset Limitations

- The main PCOS workbook has 541 labeled rows after blank rows are filtered.
- The labeled split is 177 PCOS-positive and 364 PCOS-negative.
- The main file is named `without_infertility`, so infertility is not used as a model feature.
- Endometriosis data is synthetic and is used only for symptom-overlap framing, not as a merged PCOS/endometriosis classifier.
- The model is trained on a limited hospital dataset and needs external prospective validation before clinical use.
