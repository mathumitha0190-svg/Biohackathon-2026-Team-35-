from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChecklistItem:
    name: str
    status: str
    notes: str


@dataclass(frozen=True)
class ClinicalAssessment:
    checklist: list[ChecklistItem]
    differential_flags: list[str]
    next_actions: list[str]
    confidence: str


def yes(value: object) -> bool:
    return value in (1, True, "Yes", "yes", "Y", "y")


def numeric(patient: dict, key: str) -> float | None:
    value = patient.get(key)
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def assess_guideline_evidence(patient: dict) -> list[ChecklistItem]:
    age = numeric(patient, "age")
    cycle = numeric(patient, "cycle")
    cycle_length = numeric(patient, "cycle_length")
    ovulatory = cycle == 1 or (cycle_length is not None and (cycle_length < 21 or cycle_length > 35))

    androgen_signs = [
        yes(patient.get("hair_growth")),
        yes(patient.get("pimples")),
        yes(patient.get("hair_loss")),
    ]
    hyperandrogenism = any(androgen_signs)

    amh = numeric(patient, "amh")
    follicle_l = numeric(patient, "follicle_no_l")
    follicle_r = numeric(patient, "follicle_no_r")
    has_ovarian_evidence = (
        (amh is not None and amh >= 4.0)
        or (follicle_l is not None and follicle_l >= 12)
        or (follicle_r is not None and follicle_r >= 12)
    )
    adolescent = age is not None and age < 18

    tsh = numeric(patient, "tsh")
    prl = numeric(patient, "prl")
    beta_hcg = numeric(patient, "i_beta_hcg")
    pregnant = yes(patient.get("pregnant"))
    exclusion_gaps = []
    if tsh is None:
        exclusion_gaps.append("TSH")
    if prl is None:
        exclusion_gaps.append("PRL")
    if beta_hcg is None and patient.get("pregnant") is None:
        exclusion_gaps.append("pregnancy/beta-HCG")
    exclusion_gaps.append("17-OH progesterone if clinically indicated")

    bmi = numeric(patient, "bmi")
    bp_systolic = numeric(patient, "bp_systolic")
    bp_diastolic = numeric(patient, "bp_diastolic")
    rbs = numeric(patient, "rbs")
    metabolic_flags = []
    if bmi is not None and bmi >= 25:
        metabolic_flags.append("BMI >= 25")
    if bp_systolic is not None and bp_systolic >= 130:
        metabolic_flags.append("systolic BP >= 130")
    if bp_diastolic is not None and bp_diastolic >= 80:
        metabolic_flags.append("diastolic BP >= 80")
    if rbs is not None and rbs >= 140:
        metabolic_flags.append("RBS/glucose elevated")

    ovarian_note = "AMH/ultrasound unavailable or not elevated"
    ovarian_status = "Missing"
    if adolescent:
        ovarian_status = "Caution"
        ovarian_note = "Adult AMH/ultrasound interpretation is not appropriate for adolescent-range age"
    elif has_ovarian_evidence:
        ovarian_status = "Supported"
        ovarian_note = "AMH or follicle count supports ovarian morphology evidence"

    return [
        ChecklistItem(
            "Ovulatory dysfunction",
            "Supported" if ovulatory else "Not established",
            "Irregular cycles or cycle length outside 21-35 days" if ovulatory else "Cycle evidence is regular, missing, or within usual range",
        ),
        ChecklistItem(
            "Clinical hyperandrogenism",
            "Supported" if hyperandrogenism else "Not established",
            "Hair growth, acne/pimples, or hair loss reported" if hyperandrogenism else "No clinical androgen sign reported",
        ),
        ChecklistItem("Ovarian morphology / AMH", ovarian_status, ovarian_note),
        ChecklistItem(
            "Exclusion checks",
            "Incomplete" if exclusion_gaps or pregnant else "Available",
            "Pregnancy context present; interpret PCOS pathway cautiously" if pregnant else "Missing: " + ", ".join(exclusion_gaps),
        ),
        ChecklistItem(
            "Metabolic risk",
            "Present" if metabolic_flags else "Not established",
            ", ".join(metabolic_flags) if metabolic_flags else "No BMI/BP/glucose metabolic flag from provided data",
        ),
    ]


def endometriosis_flags(patient: dict) -> list[str]:
    flags = []
    pain = numeric(patient, "chronic_pelvic_pain")
    if pain is not None and pain >= 7:
        flags.append("High chronic pelvic pain")
    if yes(patient.get("severe_menstrual_pain")):
        flags.append("Severe menstrual pain")
    if yes(patient.get("pain_with_intercourse")):
        flags.append("Pain with intercourse")
    if yes(patient.get("bowel_urinary_pain")):
        flags.append("Bowel or urinary pain around menstruation")
    if yes(patient.get("heavy_bleeding")):
        flags.append("Heavy bleeding")
    if yes(patient.get("bloating_nausea")):
        flags.append("Bloating or nausea")
    if yes(patient.get("difficulty_conceiving")):
        flags.append("Difficulty conceiving")
    return flags


def recommend_actions(patient: dict, probability: float, tier: str, checklist: list[ChecklistItem], differential_flags: list[str]) -> list[str]:
    actions = []
    high_risk = probability >= 0.65
    medium_risk = 0.35 <= probability < 0.65

    exclusions = next(item for item in checklist if item.name == "Exclusion checks")
    metabolic = next(item for item in checklist if item.name == "Metabolic risk")
    hyperandrogenism = next(item for item in checklist if item.name == "Clinical hyperandrogenism")
    ovulatory = next(item for item in checklist if item.name == "Ovulatory dysfunction")

    if high_risk and exclusions.status == "Incomplete":
        actions.append("Complete endocrine exclusion checks before confirming diagnosis.")
    if high_risk or medium_risk:
        actions.append("Use the guideline checklist to decide whether PCOS diagnostic criteria are sufficiently supported.")
    if metabolic.status == "Present":
        actions.append("Screen and manage metabolic risk: BP, glucose status, lipids if available, and lifestyle support.")
    if len(differential_flags) >= 2 or "High chronic pelvic pain" in differential_flags:
        actions.append("Consider gynecology referral or endometriosis evaluation because pain-pattern red flags are present.")
    if tier == "history":
        actions.append("Low-resource pathway used: prioritize the smallest useful lab set before ultrasound-dependent decisions.")

    bmi = numeric(patient, "bmi")
    if bmi is not None and bmi < 25 and ovulatory.status == "Supported" and hyperandrogenism.status == "Supported":
        actions.append("Lean PCOS alert: do not dismiss PCOS pathway because BMI is normal.")

    if not actions:
        actions.append("Collect missing clinical evidence and monitor symptoms rather than overdiagnosing from limited data.")

    return actions


def confidence_label(tier: str, probability: float, checklist: list[ChecklistItem]) -> str:
    missing_count = sum(item.status in {"Missing", "Incomplete", "Caution"} for item in checklist)
    if tier == "full" and missing_count <= 1 and probability >= 0.65:
        return "High"
    if tier in {"basic", "full"} and missing_count <= 2:
        return "Moderate"
    return "Low to moderate"


def assess_patient(patient: dict, probability: float, tier: str) -> ClinicalAssessment:
    checklist = assess_guideline_evidence(patient)
    differentials = endometriosis_flags(patient)
    actions = recommend_actions(patient, probability, tier, checklist, differentials)
    confidence = confidence_label(tier, probability, checklist)
    return ClinicalAssessment(checklist, differentials, actions, confidence)
