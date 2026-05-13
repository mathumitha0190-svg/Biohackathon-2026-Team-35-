# PCOS Navigator Evidence Dossier

## Project Claim

PCOS Navigator is a clinical decision-support prototype for triage and investigation planning. It does not diagnose PCOS. It helps clinicians structure the pathway from symptoms and available tests to:

- PCOS triage risk
- guideline evidence checklist
- differential red flags
- recommended next step

## Clinical Rationale

### PCOS Diagnostic Framework

The 2023 International Evidence-Based Guideline for PCOS builds on Rotterdam-style criteria. Adult PCOS assessment considers clinical or biochemical hyperandrogenism, ovulatory dysfunction, and polycystic ovarian morphology by ultrasound or adult AMH, while excluding other causes.

How the app reflects this:

- `3 Checklist` separates ovulatory dysfunction, clinical hyperandrogenism, ovarian morphology / AMH, exclusions, and metabolic risk.
- The app treats irregular cycles plus clinical androgen signs as clinically meaningful pathway evidence.
- The app does not present the model score as a diagnosis.

Source: 2023 International Evidence-Based Guideline for PCOS, JCEM: https://academic.oup.com/jcem/article/108/10/2447/7242360

### AMH And Ultrasound Caution

The 2023 guideline allows adult AMH to support ovarian morphology evidence in the diagnostic algorithm, but AMH should not be used as a standalone PCOS test. AMH or adult ultrasound interpretation is also not appropriate as a simple adolescent diagnostic shortcut.

How the app reflects this:

- AMH and follicle counts are used only in the full diagnostic tier.
- The checklist warns when age is adolescent-range.
- The app still supports history-only and basic-clinic triage when AMH or ultrasound are unavailable.

Source: 2023 International Evidence-Based Guideline for PCOS, JCEM: https://academic.oup.com/jcem/article/108/10/2447/7242360

### Exclusion Logic

PCOS-like features can overlap with thyroid disease, hyperprolactinemia, nonclassic congenital adrenal hyperplasia, pregnancy-related contexts, and other endocrine causes. The Endocrine Society guideline specifically emphasizes excluding common mimics such as thyroid disease, hyperprolactinemia, and nonclassic congenital adrenal hyperplasia.

How the app reflects this:

- The checklist shows exclusion gaps rather than hiding missing workup.
- TSH, PRL, beta-HCG/pregnancy context, and 17-OH progesterone prompts are surfaced as investigation planning items.
- The handoff summary frames these as next-step evidence needs.

Source: Endocrine Society PCOS guideline, JCEM: https://academic.oup.com/jcem/article/98/12/4565/2833703

### Public Health Need

WHO reports PCOS as a common hormonal condition affecting an estimated 10-13% of reproductive-age women globally, with many affected people undiagnosed. WHO also describes PCOS as linked to infertility and cardiometabolic risks.

How the app reflects this:

- The app prioritizes early triage and missed-case reduction rather than definitive diagnosis.
- Metabolic risk is displayed in the checklist and next-action flow.
- Low-resource history-only and basic-clinic tiers are included for feasibility.

Source: WHO PCOS fact sheet: https://www.who.int/news-room/fact-sheets/detail/polycystic-ovary-syndrome

### Endometriosis Overlap

WHO describes endometriosis as associated with severe menstrual pain, pain with intercourse, bowel or urinary pain, chronic pelvic pain, bloating/nausea, fatigue, and infertility. WHO also notes that endometriosis can mimic other conditions and contribute to diagnostic delay.

How the app reflects this:

- Endometriosis-like pain features are collected separately from PCOS features.
- The app uses the supplementary synthetic endometriosis dataset only for symptom-overlap framing, not as a merged classifier.
- The `Endometriosis-like` demo case shows referral/red-flag logic instead of forcing symptoms into PCOS.

Source: WHO endometriosis fact sheet: https://www.who.int/news-room/fact-sheets/detail/endometriosis

## Why This Is Clinically Safer Than A Generic Classifier

PCOS Navigator does not output "PCOS yes/no." It outputs:

- risk tier and probability
- clinical evidence checklist
- missing exclusions
- differential red flags
- next-step recommendation

This makes the project clinically interpretable, safer to present, and aligned with the challenge goal of improving diagnostic pathways rather than replacing clinicians.

## Source List

- 2023 International Evidence-Based Guideline for PCOS, JCEM: https://academic.oup.com/jcem/article/108/10/2447/7242360
- WHO PCOS fact sheet: https://www.who.int/news-room/fact-sheets/detail/polycystic-ovary-syndrome
- WHO endometriosis fact sheet: https://www.who.int/news-room/fact-sheets/detail/endometriosis
- Endocrine Society PCOS guideline, JCEM: https://academic.oup.com/jcem/article/98/12/4565/2833703
