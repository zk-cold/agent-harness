import subprocess
import sys
from pathlib import Path

import pytest

from scripts.mission_generator import (
    BLOCK_TERMINATOR,
    ESCAPED_BLOCK_TERMINATOR,
    MissionDraft,
    GoverningArtifact,
    ScopeItem,
    collect_draft,
    render_mission,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
MISSION_GENERATOR_MAIN = REPO_ROOT / "scripts" / "mission_generator" / "__main__.py"
HARD_CONSTRAINT_PERSISTENCE_MODE = "automated tests"
NATURAL_HOME_PERSISTENCE_MODE = (
    "same text in the governed file and matching top-level governance section "
    "where the artifact will live after the mission completes"
)


def _write_input_file(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "mission.md"
    path.write_text(content)
    return path


def test_package_exports():
    from scripts.mission_generator import main as main_fn

    assert callable(main_fn)
    assert callable(collect_draft)
    assert callable(render_mission)


def test_main_module_uses_package_entrypoint():
    src = MISSION_GENERATOR_MAIN.read_text()
    assert "from scripts.mission_generator import main" in src
    assert "main()" in src


def test_render_mission_orders_sections_and_formats_ga_criteria():
    draft = MissionDraft(
        title="Test mission",
        invariants=[GoverningArtifact("Invariants", "Invariant one\nwith second line", HARD_CONSTRAINT_PERSISTENCE_MODE, 1)],
        external_constraints=[GoverningArtifact("External Constraints", "Constraint two", HARD_CONSTRAINT_PERSISTENCE_MODE, 2)],
        beliefs=[GoverningArtifact("Beliefs", "Belief three", NATURAL_HOME_PERSISTENCE_MODE, 3)],
        considerations=[GoverningArtifact("Considerations", "Consideration four", NATURAL_HOME_PERSISTENCE_MODE, 4)],
        in_scope=[ScopeItem("Deliverable one", ["Scope AC one"])],
        out_of_scope=["Excluded one"],
        assumptions=["Assumption one"],
    )

    rendered = render_mission(draft)
    headings = [line for line in rendered.splitlines() if line.startswith("## ") or line.startswith("# Mission:")]
    assert headings == [
        "# Mission: Test mission",
        "## Invariants",
        "## External Constraints",
        "## Beliefs",
        "## Considerations",
        "## Scope",
        "## Assumptions",
        "## Acceptance Criteria",
    ]
    assert "- [GA1] Invariant one" in rendered
    assert "  with second line" in rendered
    assert f"Persist [GA1] as {HARD_CONSTRAINT_PERSISTENCE_MODE}." in rendered
    assert f"Persist [GA2] as {HARD_CONSTRAINT_PERSISTENCE_MODE}." in rendered
    assert f"Persist [GA3] as {NATURAL_HOME_PERSISTENCE_MODE}." in rendered
    assert f"Persist [GA4] as {NATURAL_HOME_PERSISTENCE_MODE}." in rendered


def test_cli_preserves_multiline_text_and_special_characters(tmp_path):
    mission_path = tmp_path / "mission.md"
    input_text = "\n".join(
        [
            "Test mission",
            "y",
            'Invariant line 1 with "quotes" and [brackets]',
            "Invariant line 2 with colon: and backslash \\",
            BLOCK_TERMINATOR,
            HARD_CONSTRAINT_PERSISTENCE_MODE,
            "n",
            "n",
            "n",
            "n",
            "y",
            "In scope item with []:{} and \\",
            BLOCK_TERMINATOR,
            "Scope AC with \"quotes\"",
            BLOCK_TERMINATOR,
            "n",
            "y",
            "Out of scope item",
            BLOCK_TERMINATOR,
            "n",
            "n",
        ]
    ) + "\n"

    completed = subprocess.run(
        [sys.executable, "-m", "scripts.mission_generator", str(mission_path)],
        input=input_text,
        text=True,
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    rendered = mission_path.read_text()
    assert "# Mission: Test mission" in rendered
    assert 'Invariant line 1 with "quotes" and [brackets]' in rendered
    assert "Invariant line 2 with colon: and backslash \\" in rendered
    assert "- [GA1] Invariant line 1 with \"quotes\" and [brackets]" in rendered
    assert f"Persist [GA1] as {HARD_CONSTRAINT_PERSISTENCE_MODE}." in rendered
    assert "## Scope" in rendered
    assert "## Acceptance Criteria" in rendered
    assert "1. Scope AC with \"quotes\"" in rendered


def test_collect_draft_does_not_duplicate_scope_acceptance_criteria():
    responses = iter(
        [
            "Test mission",
            "n",
            "n",
            "n",
            "n",
            "y",
            "In scope item",
            BLOCK_TERMINATOR,
            "Scope AC",
            BLOCK_TERMINATOR,
            "n",
            "y",
            "Out of scope item",
            BLOCK_TERMINATOR,
            "n",
            "n",
        ]
    )

    def input_fn(_prompt: str) -> str:
        return next(responses)

    draft = collect_draft(input_fn=input_fn, output_fn=lambda _msg: None)

    assert len(draft.in_scope) == 1
    assert draft.in_scope[0].acceptance_criteria == ["Scope AC"]


def test_collect_draft_allows_literal_terminator_line():
    responses = iter(
        [
                "Test mission",
                "y",
                "Line before terminator",
                ESCAPED_BLOCK_TERMINATOR,
                BLOCK_TERMINATOR,
                HARD_CONSTRAINT_PERSISTENCE_MODE,
                "n",
                "n",
                "n",
                "n",
            "y",
            "In scope item",
            BLOCK_TERMINATOR,
            "Scope AC",
            BLOCK_TERMINATOR,
            "n",
            "y",
            "Out of scope item",
            BLOCK_TERMINATOR,
            "n",
            "n",
        ]
    )

    def input_fn(_prompt: str) -> str:
        return next(responses)

    draft = collect_draft(input_fn=input_fn, output_fn=lambda _msg: None)

    assert draft.invariants[0].text == f"Line before terminator\n{BLOCK_TERMINATOR}"


def test_collect_draft_rejects_invalid_persistence_mode_for_non_hard_constraints():
    responses = iter(
        [
            "Test mission",
            "n",
            "n",
            "y",
            "Belief one",
            BLOCK_TERMINATOR,
            HARD_CONSTRAINT_PERSISTENCE_MODE,
            NATURAL_HOME_PERSISTENCE_MODE,
            "n",
            "n",
            "y",
            "In scope item",
            BLOCK_TERMINATOR,
            "Scope AC",
            BLOCK_TERMINATOR,
            "n",
            "y",
            "Out of scope item",
            BLOCK_TERMINATOR,
            "n",
            "n",
        ]
    )
    messages: list[str] = []

    def input_fn(_prompt: str) -> str:
        return next(responses)

    def output_fn(message: str) -> None:
        messages.append(message)

    draft = collect_draft(input_fn=input_fn, output_fn=output_fn)

    assert draft.beliefs[0].persistence_mode == NATURAL_HOME_PERSISTENCE_MODE
    assert messages.count(f"Enter exactly one of: {NATURAL_HOME_PERSISTENCE_MODE}") == 1


def test_read_block_raises_on_unterminated_eof():
    responses = iter(["Test mission", "y", "unterminated"])

    def input_fn(_prompt: str) -> str:
        try:
            return next(responses)
        except StopIteration as exc:
            raise EOFError from exc

    with pytest.raises(ValueError, match="Unexpected end of input"):
        collect_draft(input_fn=input_fn, output_fn=lambda _msg: None)


def test_render_mission_preserves_trailing_blank_lines():
    draft = MissionDraft(
        title="Trailing newline mission",
        invariants=[GoverningArtifact("Invariants", "Line one\n", HARD_CONSTRAINT_PERSISTENCE_MODE, 1)],
        in_scope=[ScopeItem("Deliverable", ["Scope AC"])],
        out_of_scope=["Excluded"],
    )

    rendered = render_mission(draft)

    assert "- [GA1] Line one\n  \n" in rendered
