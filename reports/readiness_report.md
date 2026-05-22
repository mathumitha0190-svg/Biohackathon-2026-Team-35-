# PCOS Navigator Readiness Report

> This tool supports triage and investigation planning. It is not a diagnosis.

## App Command

```powershell
uv run streamlit run app.py
```

## Rubric Categories Covered

- Clinical & Scientific Validity
- Diagnostic Accuracy
- Feasibility & Implementation
- Innovation & Creativity
- Impact & Public Health Value
- Methodology and Scientific Rigor
- Code Quality & Technical Execution
- Presentation & Clarity

## Readiness Checks

| Item | Status | Detail |
|---|---|---|
| `docs/evidence_dossier.md` | PASS | present |
| `docs/rubric_scorecard.md` | PASS | present |
| `docs/limitations_and_validation.md` | PASS | present |
| `docs/final_submission_checklist.md` | PASS | present |
| `docs/demo_script.md` | PASS | present |
| `docs/slide_outline.md` | PASS | present |
| `docs/case_cards.md` | PASS | present |
| `docs/judging_map.md` | PASS | present |
| `docs/visual_evidence_guide.md` | PASS | present |
| `docs/final_demo_rehearsal.md` | PASS | present |
| `docs/judge_one_pager.md` | PASS | present |
| `docs/judge_q_and_a.md` | PASS | present |
| `docs/submission_manifest.md` | PASS | present |
| `reports/data_profile.md` | PASS | present |
| `reports/model_report.md` | PASS | present |
| `models/pcos_models.joblib` | PASS | present |
| `reports/visual_evidence_report.md` | PASS | present |
| `export safety` | PASS | no datasets or model binaries found |

## Recommended Final Sequence

```powershell
uv run python scripts/profile_data.py
uv run python scripts/train_models.py
uv run python scripts/check_readiness.py
uv run python scripts/check_visual_evidence.py
uv run python scripts/export_presentation.py
uv run pytest
uv run streamlit run app.py
```
