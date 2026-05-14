# Final Submission Checklist

## Pre-Demo Command Sequence

Run these from the repository root:

```powershell
uv sync --dev
uv run python scripts/profile_data.py
uv run python scripts/train_models.py
uv run python scripts/check_readiness.py
uv run python scripts/check_visual_evidence.py
uv run python scripts/export_presentation.py
uv run pytest
uv run python scripts/preflight_submission.py
uv run streamlit run app.py
```

For the final one-command dry run before the demo:

```powershell
uv run python scripts/preflight_submission.py
```

Open the app:

```text
http://localhost:8501
```

## Expected Generated Artifacts

- `reports/data_profile.md`
- `reports/model_metrics.json`
- `reports/model_report.md`
- `reports/readiness_report.md`
- `reports/visual_evidence_report.md`
- `reports/preflight_submission_report.md`
- `models/pcos_models.joblib`
- `exports/pcos_navigator_presentation/`

Generated reports, models, and exports are ignored by git.

## Required Source Docs

- `docs/evidence_dossier.md`
- `docs/rubric_scorecard.md`
- `docs/limitations_and_validation.md`
- `docs/final_submission_checklist.md`
- `docs/demo_script.md`
- `docs/slide_outline.md`
- `docs/case_cards.md`
- `docs/judging_map.md`
- `docs/visual_evidence_guide.md`

## Demo Order

1. Typical PCOS
2. Lean PCOS
3. Endometriosis-like
4. Incomplete Data
5. Model Evidence

## Safety Statement

> This tool supports triage and investigation planning. It is not a diagnosis.

## Final Talking Points

- The project is guideline-grounded and clinically cautious.
- The app supports resource-tiered triage rather than replacing clinicians.
- The model is interpretable and validated with calibration, confidence intervals, and subgroup caveats.
- The endometriosis layer is a differential red-flag module, not a merged synthetic classifier.
- Real deployment would require external prospective validation.
