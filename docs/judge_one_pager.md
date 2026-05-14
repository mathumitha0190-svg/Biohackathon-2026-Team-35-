# PCOS Navigator Judge One-Pager

> This tool supports triage and investigation planning. It is not a diagnosis.

## Problem

PCOS is often evaluated through a fragmented pathway: cycle history, androgen signs, metabolic risk, endocrine exclusions, and ultrasound or AMH evidence may sit in different parts of the clinical record. A model score alone is not enough because the safer clinical question is what evidence is present, what is missing, and what should happen next.

## Solution

PCOS Navigator is a Streamlit clinical decision-support prototype that combines:

- three resource-tiered logistic-regression models
- guideline-style evidence checklist
- missing endocrine exclusion prompts
- endometriosis red-flag triage
- clinician-facing handoff summary

The workflow supports high-resource and low-resource settings because prediction falls back from full diagnostic data to basic clinical or history-only tiers when labs or ultrasound are missing.

## Clinical Safety

The app never claims diagnosis. It presents triage risk and investigation planning. AMH and ultrasound are not treated as standalone answers, adolescent-range interpretation is cautioned, and exclusion gaps are surfaced instead of hidden.

Clinical rationale is documented in `docs/evidence_dossier.md`, with sources including the 2023 International Evidence-Based Guideline for PCOS, WHO PCOS and endometriosis fact sheets, and the Endocrine Society PCOS guideline.

## Validation Evidence

The generated model report shows:

- 541 labeled rows after audit filtering
- 177 PCOS-positive and 364 PCOS-negative labels
- AUROC, AUPRC, sensitivity, specificity, F1, Brier score, and confusion matrix
- bootstrap 95% confidence intervals
- calibration bins and selected screening thresholds
- subgroup metrics by BMI and age groups with insufficient-data caveats

Fast evidence path: `reports/model_report.md`, `4 Evidence` tab, and `reports/preflight_submission_report.md`.

## Impact

PCOS Navigator demonstrates how a model can become a clinical pathway assistant rather than a black-box classifier. It supports earlier structured evaluation, avoids dismissing lean PCOS, flags pain-pattern differential concerns, and gives clinicians a concise next step.

## Exact Demo Path

1. `Typical PCOS`: complete pathway, high triage risk, guideline evidence, and next step.
2. `Lean PCOS`: normal BMI does not dismiss cycle and androgen evidence.
3. `Endometriosis-like`: differential red flags route toward gynecology evaluation.
4. `Incomplete Data`: missing labs and ultrasound fall back to history-only triage.
5. `4 Evidence`: metrics, calibration, thresholds, and subgroup caveats.

Run command:

```powershell
uv run streamlit run app.py
```
