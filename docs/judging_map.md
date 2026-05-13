# Judging Map

| Rubric area | What PCOS Navigator shows | Where to show it |
|---|---|---|
| Clinical & Scientific Validity | Guideline checklist for ovulatory dysfunction, clinical hyperandrogenism, ovarian morphology / AMH, exclusions, and metabolic risk | Guideline Checklist tab, Slide 2, Slide 4 |
| Diagnostic Accuracy | Three model tiers, AUROC, AUPRC, sensitivity, specificity, Brier score, calibration, selected screening thresholds | Model Evidence tab, model report, Slide 6 |
| Feasibility & Implementation | History-only, basic clinical, and full diagnostic tiers; graceful fallback when labs or ultrasound are missing | Incomplete Data demo case, Slide 5, Slide 8 |
| Innovation & Creativity | Combines triage probability, guideline reasoning, differential red flags, and next-best-action recommendation | Solution slide, live demo, Next Action tab |
| Impact & Public Health Value | Supports earlier recognition, lean PCOS handling, low-resource triage, and pain-pattern red flags | Lean PCOS demo, Endometriosis-like demo, Slide 8 |
| Methodology & Scientific Rigor | Split-based evaluation, bootstrap confidence intervals, calibration bins, subgroup caveats, generated model report | Model Evidence tab, `reports/model_report.md` |
| Code Quality & Technical Execution | Reproducible `uv` commands, tests, modular package, generated reports, ignored artifacts | README, test output, repository structure |
| Presentation & Clarity | Prepared demo script, case cards, slide outline, and judging map | `docs/`, export bundle |

## Best Judge-Facing Message

PCOS Navigator is not an AI diagnosis product. It is a pathway assistant that helps clinicians decide what evidence is present, what is missing, which overlapping condition flags matter, and what the recommended next step should be.
