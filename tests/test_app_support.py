from types import SimpleNamespace

from app import CASE_EXPLANATIONS, optional_number, optional_number_args, driver_chart, grouped_actions, top_summary
from pcos_navigator.clinical import assess_patient
from pcos_navigator.data import available_model_tier, load_clean_pcos
from pcos_navigator.demo_cases import DEMO_CASES
from pcos_navigator.modeling import predict_patient, train_models


def test_driver_chart_uses_prediction_contributions():
    df = load_clean_pcos()
    artifact, _ = train_models(df)
    patient = DEMO_CASES["Typical PCOS"]
    prediction = predict_patient(artifact, patient, available_model_tier(patient))
    figure = driver_chart(prediction.top_drivers)

    assert prediction.top_drivers
    assert figure.data
    assert len(figure.data[0].x) == len(prediction.top_drivers)


def test_case_explanations_cover_all_demo_cases():
    assert set(CASE_EXPLANATIONS) == set(DEMO_CASES)


def test_optional_number_args_normalizes_mixed_numeric_types_to_float():
    min_value, value, step = optional_number_args(value=120, min_value=70, step=1)

    assert (min_value, value, step) == (70.0, 120.0, 1.0)
    assert all(isinstance(item, float) for item in (min_value, value, step))


def test_optional_number_passes_consistent_float_types_to_streamlit(monkeypatch):
    captured = {}

    def fake_checkbox(_label, value):
        assert value is True
        return True

    def fake_number_input(label, min_value, value, step):
        captured.update(
            {
                "label": label,
                "min_value": min_value,
                "value": value,
                "step": step,
            }
        )
        return value

    monkeypatch.setattr("app.st.checkbox", fake_checkbox)
    monkeypatch.setattr("app.st.number_input", fake_number_input)

    result = optional_number("BP systolic", 120, min_value=70, step=1)

    assert result == 120.0
    assert captured == {
        "label": "BP systolic",
        "min_value": 70.0,
        "value": 120.0,
        "step": 1.0,
    }
    assert all(isinstance(captured[key], float) for key in ("min_value", "value", "step"))


def test_top_summary_returns_judge_facing_fields():
    prediction = SimpleNamespace(risk_tier="High", probability=0.82, tier="full")
    assessment = SimpleNamespace(confidence="High", next_actions=["Complete endocrine exclusion checks."])

    summary = top_summary(prediction, assessment)

    assert summary == {
        "risk_tier": "High",
        "probability": "82%",
        "model_tier": "full",
        "confidence": "High",
        "recommended_next_step": "Complete endocrine exclusion checks.",
    }


def test_grouped_actions_separates_pathway_flags_missing_and_next_step():
    patient = DEMO_CASES["Endometriosis-like"]
    assessment = assess_patient(patient, probability=0.22, tier="history")

    grouped = grouped_actions(assessment)

    assert grouped["Differential flags"]
    assert any("endometriosis" in item.lower() or "pelvic pain" in item.lower() for item in grouped["Differential flags"])
    assert grouped["Missing evidence"]
    assert grouped["Recommended next step"]
