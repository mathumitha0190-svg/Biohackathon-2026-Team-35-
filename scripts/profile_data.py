from pcos_navigator.config import DATA_PROFILE_PATH, REPORTS_DIR
from pcos_navigator.data import build_data_profile, load_clean_pcos, profile_to_markdown


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_clean_pcos()
    profile = build_data_profile(df)
    DATA_PROFILE_PATH.write_text(profile_to_markdown(profile, df), encoding="utf-8")
    print(f"Wrote {DATA_PROFILE_PATH}")
    print(
        f"Labeled rows={profile.row_count}, positive={profile.positive_count}, negative={profile.negative_count}"
    )


if __name__ == "__main__":
    main()
