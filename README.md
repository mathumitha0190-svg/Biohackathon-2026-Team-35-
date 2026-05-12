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

## Outputs

- `reports/data_profile.md`
- `reports/model_metrics.json`
- `models/pcos_models.joblib`

Generated reports and model artifacts are ignored by git.

## Dataset Limitations

- The main PCOS workbook has 541 labeled rows after blank rows are filtered.
- The labeled split is 177 PCOS-positive and 364 PCOS-negative.
- The main file is named `without_infertility`, so infertility is not used as a model feature.
- Endometriosis data is synthetic and is used only for symptom-overlap framing, not as a merged PCOS/endometriosis classifier.
- The model is trained on a limited hospital dataset and needs external prospective validation before clinical use.
