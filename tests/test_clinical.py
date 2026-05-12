from pcos_navigator.clinical import assess_patient
from pcos_navigator.demo_cases import DEMO_CASES


def action_text(assessment):
    return " ".join(assessment.next_actions)


def checklist_status(assessment, name):
    return next(item.status for item in assessment.checklist if item.name == name)


def test_typical_pcos_case_has_supported_guideline_evidence():
    assessment = assess_patient(DEMO_CASES["Typical PCOS"], probability=0.82, tier="full")
    assert checklist_status(assessment, "Ovulatory dysfunction") == "Supported"
    assert checklist_status(assessment, "Clinical hyperandrogenism") == "Supported"
    assert checklist_status(assessment, "Ovarian morphology / AMH") == "Supported"


def test_lean_pcos_case_triggers_lean_alert():
    assessment = assess_patient(DEMO_CASES["Lean PCOS"], probability=0.74, tier="full")
    assert "Lean PCOS alert" in action_text(assessment)


def test_endometriosis_like_case_triggers_referral_flag():
    assessment = assess_patient(DEMO_CASES["Endometriosis-like"], probability=0.22, tier="history")
    assert "High chronic pelvic pain" in assessment.differential_flags
    assert "endometriosis evaluation" in action_text(assessment)


def test_incomplete_data_case_recommends_more_evidence():
    assessment = assess_patient(DEMO_CASES["Incomplete Data"], probability=0.45, tier="history")
    assert "Low-resource pathway used" in action_text(assessment)
