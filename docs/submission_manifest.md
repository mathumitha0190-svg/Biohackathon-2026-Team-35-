# Submission Manifest

> This tool supports triage and investigation planning. It is not a diagnosis.

## Fast Review Path

1. `docs/judge_one_pager.md`
2. `exports/pcos_navigator_presentation/README.md`
3. `reports/preflight_submission_report.md`
4. `uv run streamlit run app.py`

## Committed Source Docs

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

## Generated Reports And Artifacts

- `reports/data_profile.md`
- `reports/model_metrics.json`
- `reports/model_report.md`
- `reports/readiness_report.md`
- `reports/visual_evidence_report.md`
- `reports/preflight_submission_report.md`
- `models/pcos_models.joblib`
- `exports/pcos_navigator_presentation/`

Generated reports, exports, screenshots, and model binaries are intentionally ignored by git.

## Screenshot Evidence

Expected screenshot files under `assets/screenshots/`:

- `01_intake_summary.png`
- `02_risk_result.png`
- `03_guideline_checklist.png`
- `04_model_evidence.png`
- `05_next_action_handoff.png`
- `06_readiness_export.png`

Final strict evidence command:

```powershell
uv run python scripts/preflight_submission.py --strict-screenshots
```

## Core Commands

```powershell
uv sync --dev
uv run python scripts/profile_data.py
uv run python scripts/train_models.py
uv run python scripts/check_readiness.py
uv run python scripts/check_visual_evidence.py
uv run python scripts/export_presentation.py
uv run pytest
uv run streamlit run app.py
```

## Demo Order

1. Typical PCOS
2. Lean PCOS
3. Endometriosis-like
4. Incomplete Data
5. Model Evidence

## Safety Wording

Use this exact wording in demo and slides:

> This tool supports triage and investigation planning. It is not a diagnosis.
