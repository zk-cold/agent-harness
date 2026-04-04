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
