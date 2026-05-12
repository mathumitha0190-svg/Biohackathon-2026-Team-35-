from pcos_navigator.data import EXCLUDED_MODEL_COLUMNS, IDENTIFIER_COLUMNS, MODEL_FEATURES, TARGET, build_data_profile, load_clean_pcos


def test_clean_data_counts_and_labels():
    df = load_clean_pcos()
    profile = build_data_profile(df)

    assert profile.row_count == 541
    assert profile.positive_count == 177
    assert profile.negative_count == 364
    assert set(df[TARGET].unique()) == {0, 1}


def test_excluded_columns_not_in_model_features():
    all_features = set(sum(MODEL_FEATURES.values(), []))
    assert all_features.isdisjoint(IDENTIFIER_COLUMNS)
    assert all_features.isdisjoint(EXCLUDED_MODEL_COLUMNS)


def test_cycle_recode_preserves_expected_values():
    df = load_clean_pcos()
    assert set(df["cycle"].dropna().unique()) == {0.0, 1.0}
    assert int((df["cycle"] == 1).sum()) == 150
    assert int((df["cycle"] == 0).sum()) == 390
