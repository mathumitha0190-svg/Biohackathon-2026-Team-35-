from scripts.check_readiness import (
    REQUIRED_DOCS,
    RUBRIC_CATEGORIES,
    check_generated_artifacts,
    check_required_docs,
    readiness_to_markdown,
)
from pcos_navigator.config import SAFETY_STATEMENT


def test_required_docs_are_detected():
    results = check_required_docs()
    labels = {result.label for result in results}
    expected_judge_docs = {
        "docs/final_demo_rehearsal.md",
        "docs/judge_one_pager.md",
        "docs/judge_q_and_a.md",
        "docs/submission_manifest.md",
    }

    assert set(REQUIRED_DOCS).issubset(labels)
    assert expected_judge_docs.issubset(labels)
    assert all(result.status == "PASS" for result in results)


def test_missing_generated_artifacts_have_regeneration_messages(tmp_path):
    results = check_generated_artifacts(tmp_path)

    assert results
    assert all(result.status == "WARN" for result in results)
    assert any("uv run python scripts/train_models.py" in result.detail for result in results)
    assert any("uv run python scripts/profile_data.py" in result.detail for result in results)


def test_readiness_report_contains_safety_app_command_and_rubric():
    markdown = readiness_to_markdown([])

    assert SAFETY_STATEMENT in markdown
    assert "uv run streamlit run app.py" in markdown
    for category in RUBRIC_CATEGORIES:
        assert category in markdown
