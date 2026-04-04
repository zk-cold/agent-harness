from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text()


def test_new_sdlc_prefers_fast_path_attempts_with_explicit_assumptions():
    text = _read(".claude/commands/new-sdlc.md")

    assert "Mission Creation should make a good-faith attempt to keep a request on fast path" in text
    assert "These assumptions are provisional" in text
    assert "no eligibility criterion is already known to fail" in text


def test_mission_schema_allows_later_validation_of_fast_path_assumptions():
    text = _read(".agent/schemas/mission-schema.md")

    assert "Assumptions may provisionally carry plausible fast-path claims forward" in text
    assert "Assumptions must not hide already-known fast-path disqualifiers." in text


def test_tdd_protocol_requires_execution_to_validate_coverage_assumption():
    text = _read(".agent/schemas/tdd-protocol.md")

    assert "Mission Creation may carry forward a plausible assumption" in text
    assert "execution step 1 must confirm it" in text


def test_tdd_protocol_uses_baseline_only_for_threshold_gating():
    text = _read(".agent/schemas/tdd-protocol.md")

    assert "The coverage threshold is **>80% line coverage on the code being touched by the mission**." in text
    assert "This baseline is used in step 3" in text
    assert "Verify the touched code still meets the coverage threshold (>80% line coverage)." in text
    assert "Verify no coverage regression compared to the baseline recorded in step 2." not in text


def test_new_sdlc_execution_mentions_threshold_check_not_regression_gate():
    text = _read(".claude/commands/new-sdlc.md")

    assert "touched code remains above the >80% coverage threshold" in text
    assert "final verification (full suite + coverage threshold check)" in text
    assert "final verification (full suite + coverage threshold check + formatter/linter)" in text
    assert "coverage regression check" not in text
    assert "no coverage regression" not in text
