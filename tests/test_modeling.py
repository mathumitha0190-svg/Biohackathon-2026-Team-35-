from pcos_navigator.data import available_model_tier, load_clean_pcos
from pcos_navigator.demo_cases import DEMO_CASES
from pcos_navigator.modeling import predict_patient, train_models


def test_train_models_and_predict_demo_case():
    df = load_clean_pcos()
    artifact, metrics = train_models(df)

    assert set(artifact["models"]) == {"history", "basic", "full"}
    assert set(metrics["tiers"]) == {"history", "basic", "full"}
    for tier_metrics in metrics["tiers"].values():
        assert 0 <= tier_metrics["auroc"] <= 1
        assert 0 <= tier_metrics["auprc"] <= 1
        assert tier_metrics["threshold_table"]

    patient = DEMO_CASES["Typical PCOS"]
    tier = available_model_tier(patient)
    prediction = predict_patient(artifact, patient, tier)
    assert tier == "full"
    assert 0 <= prediction.probability <= 1
    assert prediction.top_drivers


def test_missing_optional_fields_fall_back_to_history_tier():
    patient = DEMO_CASES["Incomplete Data"]
    assert available_model_tier(patient) == "history"
