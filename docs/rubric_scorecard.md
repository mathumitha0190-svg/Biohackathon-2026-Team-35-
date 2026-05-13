# PCOS Navigator Rubric Scorecard

| Rubric area | Weight | Evidence to show judges | Repo or app location |
|---|---:|---|---|
| Clinical & Scientific Validity | 30% | Guideline-aligned checklist, AMH caution, exclusion prompts, endometriosis overlap logic, cited clinical rationale | `3 Checklist`, `docs/evidence_dossier.md` |
| Diagnostic Accuracy | 20% | Three model tiers, AUROC, AUPRC, sensitivity, specificity, Brier score, bootstrap intervals, selected thresholds, calibration bins | `4 Evidence`, `reports/model_report.md` |
| Feasibility & Implementation | 20% | History-only, basic-clinic, and full diagnostic tiers; low-resource fallback; optional labs and ultrasound | `Incomplete Data` demo, README commands |
| Innovation & Creativity | 12% | Hybrid pathway assistant: model probability plus guideline checklist, missing-evidence logic, differential flags, and recommended next step | `5 Action`, demo script |
| Impact & Public Health Value | 10% | Earlier recognition, lean PCOS handling, metabolic risk prompts, endometriosis referral flags, underserved-setting pathway | `Lean PCOS` and `Endometriosis-like` demos |
| Methodology & Scientific Rigor | 10% | Split-before-imputation pipeline, generated data profile, confidence intervals, calibration, subgroup caveats, limitations plan | `reports/data_profile.md`, `docs/limitations_and_validation.md` |
| Code Quality & Technical Execution | 5% | Reproducible `uv` workflow, modular package, tests, generated reports, ignored artifacts, export script | README, `tests/`, `scripts/` |
| Presentation & Clarity | 3% | 5-minute script, case cards, slide outline, export bundle, fast judge-facing app flow | `docs/`, `exports/pcos_navigator_presentation/` |

## Final Judge Message

PCOS Navigator is strongest when presented as a diagnostic pathway assistant, not as an AI doctor. The model estimates triage risk; the clinical layer explains what evidence supports the pathway, what evidence is missing, and what next step is reasonable.

## Demo Proof Points

1. `Typical PCOS`: complete guideline and model pathway.
2. `Lean PCOS`: phenotype-aware triage that avoids BMI-based dismissal.
3. `Endometriosis-like`: differential red flags rather than forced PCOS classification.
4. `Incomplete Data`: low-resource fallback and missing-evidence prompts.

## What To Say If Asked About Deployment

This is a hackathon prototype using retrospective data. It is suitable for demonstrating workflow value, reproducible methodology, and clinical reasoning. It would require prospective external validation, local calibration, clinical governance review, and clinician training before real clinical use.
