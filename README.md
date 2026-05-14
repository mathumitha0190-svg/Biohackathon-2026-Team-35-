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

Run final readiness checks:

```powershell
uv run python scripts/check_readiness.py
```

Check optional screenshot evidence:

```powershell
uv run python scripts/check_visual_evidence.py
```

Run the full final judge dry run:

```powershell
uv run python scripts/preflight_submission.py
```

After capturing screenshots, run the strict final evidence gate:

```powershell
uv run python scripts/preflight_submission.py --strict-screenshots
```

## Outputs

- `reports/data_profile.md`
- `reports/model_metrics.json`
- `reports/model_report.md`
- `reports/readiness_report.md`
- `reports/visual_evidence_report.md`
- `reports/preflight_submission_report.md`
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

## For Judges

Fastest review path:

1. `docs/judge_one_pager.md`
2. `exports/pcos_navigator_presentation/README.md`
3. `reports/preflight_submission_report.md`
4. `uv run streamlit run app.py`

## Presentation Kit

Committed judge-facing materials live in `docs/`:

- `docs/demo_script.md`
- `docs/slide_outline.md`
- `docs/case_cards.md`
- `docs/judging_map.md`
- `docs/evidence_dossier.md`
- `docs/rubric_scorecard.md`
- `docs/limitations_and_validation.md`
- `docs/final_submission_checklist.md`
- `docs/visual_evidence_guide.md`
- `docs/final_demo_rehearsal.md`
- `docs/judge_one_pager.md`
- `docs/judge_q_and_a.md`
- `docs/submission_manifest.md`

Recommended live demo flow:

1. Start the app with `uv run streamlit run app.py`.
2. Demo `Typical PCOS` to show the complete pathway.
3. Demo `Lean PCOS` to show normal-BMI PCOS handling.
4. Demo `Endometriosis-like` to show differential red flags.
5. Demo `Incomplete Data` to show low-resource fallback.
6. End on the `4 Evidence` tab with calibration, thresholds, and subgroup caveats.

The export command creates an ignored bundle at `exports/pcos_navigator_presentation/` and intentionally excludes datasets and model binaries.

## Final Readiness

Use this sequence before presenting:

```powershell
uv run python scripts/profile_data.py
uv run python scripts/train_models.py
uv run python scripts/check_readiness.py
uv run python scripts/check_visual_evidence.py
uv run python scripts/export_presentation.py
uv run pytest
uv run python scripts/preflight_submission.py
uv run streamlit run app.py
```

The readiness command writes `reports/readiness_report.md`, which checks source docs, generated artifacts, export safety, the safety statement, app command, and rubric coverage.

Optional screenshot evidence can be saved under `assets/screenshots/` using the filenames in `docs/visual_evidence_guide.md`. Screenshot image files are ignored by git, and `uv run python scripts/check_visual_evidence.py` writes `reports/visual_evidence_report.md` with warnings for any missing screenshots.

For the final pre-demo pass, run `uv run python scripts/preflight_submission.py`. It executes the reproducibility commands, tests, app import check, export refresh, and writes `reports/preflight_submission_report.md`.

After all six screenshots are saved under `assets/screenshots/`, run `uv run python scripts/preflight_submission.py --strict-screenshots`. Strict mode makes missing screenshots blocking for the final local submission check; normal preflight keeps them as warnings.

## Dataset Limitations

- The main PCOS workbook has 541 labeled rows after blank rows are filtered.
- The labeled split is 177 PCOS-positive and 364 PCOS-negative.
- The main file is named `without_infertility`, so infertility is not used as a model feature.
- Endometriosis data is synthetic and is used only for symptom-overlap framing, not as a merged PCOS/endometriosis classifier.
- The model is trained on a limited hospital dataset and needs external prospective validation before clinical use.
