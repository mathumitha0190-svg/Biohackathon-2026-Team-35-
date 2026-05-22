# PCOS Navigator Preflight Submission Report

> This tool supports triage and investigation planning. It is not a diagnosis.

Generated: 2026-05-22T02:27:06+00:00

## Final Status: READY WITH WARNINGS

- Screenshot evidence: 0/6 screenshots present
- Strict screenshot mode: disabled

## What To Fix Before Judging

- WARN: `export screenshots` - no screenshots exported
- WARN: `01_intake_summary.png` - missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\01_intake_summary.png`
- WARN: `02_risk_result.png` - missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\02_risk_result.png`
- WARN: `03_guideline_checklist.png` - missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\03_guideline_checklist.png`
- WARN: `04_model_evidence.png` - missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\04_model_evidence.png`
- WARN: `05_next_action_handoff.png` - missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\05_next_action_handoff.png`
- WARN: `06_readiness_export.png` - missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\06_readiness_export.png`

## App Command

```powershell
uv run streamlit run app.py
```

## Command Results

| Step | Command | Status | Return code | Detail |
|---|---|---|---|---|
| Data profile | `uv run python scripts/profile_data.py` | PASS | 0 | completed in 0.8s |
| Model training and reports | `uv run python scripts/train_models.py` | PASS | 0 | completed in 4.5s |
| Readiness report | `uv run python scripts/check_readiness.py` | PASS | 0 | completed in 0.1s |
| Visual evidence report | `uv run python scripts/check_visual_evidence.py` | PASS | 0 | completed in 0.1s |
| Presentation export | `uv run python scripts/export_presentation.py` | PASS | 0 | completed in 0.1s |
| Test suite | `uv run pytest` | PASS | 0 | completed in 11.9s |
| App import | `uv run python -c "import app; print('app import ok')"` | PASS | 0 | completed in 1.6s |

## Generated Artifact Checklist

| Item | Status | Detail |
|---|---|---|
| `reports/data_profile.md` | PASS | present |
| `reports/model_metrics.json` | PASS | present |
| `reports/model_report.md` | PASS | present |
| `reports/readiness_report.md` | PASS | present |
| `reports/visual_evidence_report.md` | PASS | present |
| `reports/preflight_submission_report.md` | PASS | present |
| `models/pcos_models.joblib` | PASS | present |
| `exports/pcos_navigator_presentation/` | PASS | present with 18 files |

## Export Bundle Summary

| Item | Status | Detail |
|---|---|---|
| `export folder` | PASS | 18 files exported |
| `export blocked files` | PASS | none found |
| `export markdown files` | PASS | case_cards.md, demo_script.md, evidence_dossier.md, final_demo_rehearsal.md, final_submission_checklist.md, judge_one_pager.md, judge_q_and_a.md, judging_map.md, limitations_and_validation.md, model_report.md, preflight_submission_report.md, readiness_report.md, README.md, rubric_scorecard.md, slide_outline.md, submission_manifest.md, visual_evidence_guide.md, visual_evidence_report.md |
| `export screenshots` | WARN | no screenshots exported |

## Screenshot Evidence Status

Missing screenshots are warnings by default and blocking only when `--strict-screenshots` is used.

Summary: 0/6 screenshots present.

| Screenshot | Status | Rubric purpose | Detail |
|---|---|---|---|
| `01_intake_summary.png` | WARN | Feasibility, presentation clarity | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\01_intake_summary.png` |
| `02_risk_result.png` | WARN | Diagnostic accuracy, interpretability | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\02_risk_result.png` |
| `03_guideline_checklist.png` | WARN | Clinical and scientific validity | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\03_guideline_checklist.png` |
| `04_model_evidence.png` | WARN | Methodology, validation rigor | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\04_model_evidence.png` |
| `05_next_action_handoff.png` | WARN | Innovation, clinical workflow value | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\05_next_action_handoff.png` |
| `06_readiness_export.png` | WARN | Code quality, reproducibility, presentation readiness | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\06_readiness_export.png` |

## Final Demo Order

1. Typical PCOS
2. Lean PCOS
3. Endometriosis-like
4. Incomplete Data
5. Model Evidence

## Rubric-Facing Evidence

- Clinical validity: guideline checklist, exclusion gaps, and cited evidence dossier
- Diagnostic accuracy: tier metrics, confidence intervals, calibration, and thresholds
- Feasibility: Streamlit demo, uv workflow, export bundle, and reproducible scripts
- Innovation and impact: resource-tiered PCOS triage plus endometriosis red-flag handoff
- Methodology: dataset audit, subgroup caveats, and generated model report
- Code quality and presentation: tests, readiness checks, docs, and visual evidence guide
