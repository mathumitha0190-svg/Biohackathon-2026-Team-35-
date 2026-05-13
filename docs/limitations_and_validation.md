# Limitations And Validation Plan

## Current Dataset Limitations

- The required PCOS dataset has 541 labeled rows after blank rows are filtered.
- The dataset comes from a limited hospital context and may not generalize to other geographies, ethnic groups, care settings, or age distributions.
- The file is named `without_infertility`, so infertility is not used as a PCOS model feature.
- Some variables are derived from others, such as BMI, waist:hip ratio, and FSH/LH ratio. The preprocessing audit records these checks.
- The dataset contains clinical and ultrasound variables that may be unavailable in primary care or low-resource settings.

## Endometriosis Dataset Limitation

The supplementary endometriosis dataset is synthetic and has a different feature space from the PCOS dataset. PCOS Navigator therefore does not merge the datasets into a single classifier. The endometriosis dataset supports symptom-overlap framing and red-flag logic only.

## Model Validation Already Implemented

- Stratified train/test split.
- Three resource tiers: history-only, basic clinical, and full diagnostic.
- Logistic regression with preprocessing pipelines for reproducibility.
- AUROC, AUPRC, sensitivity, specificity, F1, Brier score, and confusion matrix.
- Bootstrap confidence intervals.
- Calibration bins.
- Selected screening threshold per tier.
- Subgroup metrics by BMI group and age group, with small groups marked as insufficient.

## Subgroup Caveats

Subgroup results are descriptive only. Groups with small sample size or only one outcome class should not be used to claim fairness or clinical safety. They are included so judges can see that subgroup validity was considered transparently.

## Clinical Safety Boundaries

- The app supports triage and investigation planning. It is not a diagnosis.
- AMH is not used as a standalone PCOS answer.
- Adult ultrasound or AMH interpretation is flagged as inappropriate for adolescent-range age.
- Exclusion gaps are surfaced instead of hidden.
- Endometriosis-pattern pain prompts referral/evaluation logic rather than a forced PCOS label.

## Prospective Validation Plan

Before real-world deployment:

1. Validate on an external dataset from a different geography and care setting.
2. Prospectively collect primary-care intake data and compare app recommendations with clinician adjudication.
3. Recalibrate probability thresholds locally.
4. Evaluate performance across age, BMI, ethnicity, and resource-setting subgroups.
5. Conduct usability testing with primary care clinicians and gynecology specialists.
6. Add governance controls, audit logging, and clinical sign-off before use in patient care.

## Presentation Framing

The correct claim is:

> PCOS Navigator demonstrates a clinically grounded triage workflow that could reduce missed cases and improve investigation planning after external validation.

The claim to avoid is:

> The model diagnoses PCOS.
