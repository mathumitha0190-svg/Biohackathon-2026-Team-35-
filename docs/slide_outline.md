# PCOS Navigator Slide Outline

## Slide 1 - The Problem

Message: PCOS is common, heterogeneous, and often delayed or missed.

Show:

- PCOS affects many reproductive-age women.
- Symptoms vary across metabolic, hormonal, and reproductive patterns.
- Missed diagnosis can delay fertility, metabolic, and quality-of-life support.

Rubric link: clinical validity, public health impact.

## Slide 2 - Why Diagnosis Is Hard

Message: PCOS is a pathway problem, not a single-test problem.

Show:

- no single diagnostic test
- overlapping symptoms with endometriosis and endocrine causes
- atypical and lean phenotypes
- incomplete exclusions in routine care

Rubric link: clinical validity, diagnostic accuracy.

## Slide 3 - Our Solution

Message: PCOS Navigator supports structured triage and investigation planning.

Show the four outputs:

- PCOS triage risk
- guideline checklist
- differential red flags
- recommended next step

Rubric link: innovation, feasibility.

## Slide 4 - Data And Safety Boundaries

Message: The project uses the required PCOS dataset responsibly.

Show:

- 541 labeled PCOS rows after filtering
- 177 positive and 364 negative labels
- synthetic endometriosis data used only for symptom-overlap framing
- safety statement: triage support, not diagnosis

Rubric link: methodology, clinical validity.

## Slide 5 - Methodology

Message: Three resource tiers make the tool usable across care settings.

Show:

- history-only model
- basic clinical model
- full diagnostic model
- logistic regression with coefficient explanations
- bootstrap CIs, calibration bins, threshold tradeoffs, subgroup checks

Rubric link: methodology, feasibility, diagnostic accuracy.

## Slide 6 - Results

Message: The full model performs best, but lower-resource tiers remain useful.

Show:

- AUROC and AUPRC by tier
- selected screening threshold by tier
- calibration plot screenshot or table
- subgroup caveat: small groups are descriptive only

Rubric link: diagnostic accuracy, scientific rigor.

## Slide 7 - Live Demo

Message: The app handles real clinical workflow patterns.

Demo order:

1. Typical PCOS
2. Lean PCOS
3. Endometriosis-like
4. Incomplete data

Rubric link: presentation clarity, implementation.

## Slide 8 - Impact And Next Steps

Message: The prototype shows a practical route to earlier recognition and safer triage.

Show:

- primary care and telehealth workflow
- low-resource fallback
- clinician handoff summary
- external prospective validation needed before deployment

Rubric link: public health impact, feasibility, code quality.
