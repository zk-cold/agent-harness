from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = REPO_ROOT / ".agent" / "schemas" / "mission-critic-protocol.md"
EXPECTED_FAST_PATH_ELIGIBILITY = """## Fast-Path Eligibility
Apply this invariant only when the review context explicitly identifies the mission as a fast-path mission.
If the review context does not explicitly identify the mission as fast-path, do not reject under this invariant.
When this invariant applies, all criteria must be met:
- No more than one governed artifact change
- No consideration overrides
- Scope <5 files"""


def _trim_trailing_whitespace(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines())


def _extract_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = lines.index(heading)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("## ") or line.startswith("# "):
            end = index
            break
    return "\n".join(lines[start:end]).rstrip()


def test_fast_path_eligibility_section_matches_mission():
    section = _extract_section(PROTOCOL_PATH.read_text(), "## Fast-Path Eligibility")
    assert _trim_trailing_whitespace(section) == _trim_trailing_whitespace(
        EXPECTED_FAST_PATH_ELIGIBILITY
    )
