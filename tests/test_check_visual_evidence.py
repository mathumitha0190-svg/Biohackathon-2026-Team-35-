from scripts.check_visual_evidence import (
    EXPECTED_SCREENSHOTS,
    check_visual_evidence,
    visual_evidence_to_markdown,
)
from pcos_navigator.config import SAFETY_STATEMENT


def test_visual_evidence_checker_warns_for_missing_screenshots(tmp_path):
    results = check_visual_evidence(tmp_path)

    assert len(results) == len(EXPECTED_SCREENSHOTS)
    assert all(result.status == "WARN" for result in results)


def test_visual_evidence_checker_passes_for_expected_screenshots(tmp_path):
    for item in EXPECTED_SCREENSHOTS:
        (tmp_path / item["filename"]).write_bytes(b"not-a-real-png-but-present")

    results = check_visual_evidence(tmp_path)

    assert all(result.status == "PASS" for result in results)


def test_visual_evidence_report_lists_expected_files_and_rubric_purpose(tmp_path):
    results = check_visual_evidence(tmp_path)
    report = visual_evidence_to_markdown(results)

    assert SAFETY_STATEMENT in report
    for item in EXPECTED_SCREENSHOTS:
        assert item["filename"] in report
        assert item["rubric"] in report
