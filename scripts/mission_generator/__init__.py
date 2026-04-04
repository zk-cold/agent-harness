#!/usr/bin/env python3
"""Interactive mission.md generator for the agent harness."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Callable

HARD_CONSTRAINT_PERSISTENCE_MODE = "automated tests"
NATURAL_HOME_PERSISTENCE_MODE = (
    "same text in the governed file and matching top-level governance section "
    "where the artifact will live after the mission completes"
)
PERSISTENCE_MODES_BY_SECTION = {
    "Invariants": (HARD_CONSTRAINT_PERSISTENCE_MODE,),
    "External Constraints": (HARD_CONSTRAINT_PERSISTENCE_MODE,),
    "Beliefs": (NATURAL_HOME_PERSISTENCE_MODE,),
    "Considerations": (NATURAL_HOME_PERSISTENCE_MODE,),
}
GOVERNANCE_SECTIONS = (
    "Invariants",
    "External Constraints",
    "Beliefs",
    "Considerations",
)
BLOCK_TERMINATOR = "<<END>>"
ESCAPED_BLOCK_TERMINATOR = "\\" + BLOCK_TERMINATOR


@dataclass
class GoverningArtifact:
    section: str
    text: str
    persistence_mode: str
    ga_id: int


@dataclass
class ScopeItem:
    text: str
    acceptance_criteria: list[str] = field(default_factory=list)


@dataclass
class MissionDraft:
    title: str
    invariants: list[GoverningArtifact] = field(default_factory=list)
    external_constraints: list[GoverningArtifact] = field(default_factory=list)
    beliefs: list[GoverningArtifact] = field(default_factory=list)
    considerations: list[GoverningArtifact] = field(default_factory=list)
    in_scope: list[ScopeItem] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)

    def all_governing_artifacts(self) -> list[GoverningArtifact]:
        return [
            *self.invariants,
            *self.external_constraints,
            *self.beliefs,
            *self.considerations,
        ]

    def all_scope_acceptance_criteria(self) -> list[str]:
        return [criterion for item in self.in_scope for criterion in item.acceptance_criteria]


def _ask(input_fn: Callable[[str], str], prompt: str) -> str:
    return input_fn(prompt)


def _read_block(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    prompt: str,
) -> str:
    output_fn(prompt)
    lines: list[str] = []
    while True:
        try:
            line = _ask(input_fn, "")
        except EOFError as exc:
            raise ValueError("Unexpected end of input while reading a multiline block") from exc
        if line == BLOCK_TERMINATOR:
            break
        if line == ESCAPED_BLOCK_TERMINATOR:
            line = BLOCK_TERMINATOR
        lines.append(line)
    return "\n".join(lines)


def _read_yes_no(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    prompt: str,
) -> bool:
    while True:
        answer = _ask(input_fn, prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no", ""}:
            return False
        output_fn("Enter `y` or `n`.")


def _read_choice(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    prompt: str,
    choices: tuple[str, ...],
) -> str:
    while True:
        answer = _ask(input_fn, prompt).strip()
        if answer in choices:
            return answer
        output_fn(f"Enter exactly one of: {', '.join(choices)}")


def _persistence_modes_for_section(section: str) -> tuple[str, ...]:
    return PERSISTENCE_MODES_BY_SECTION[section]


def _persistence_prompt_for_section(section: str) -> str:
    return f"Persistence mode [{'/'.join(_persistence_modes_for_section(section))}]: "


def _read_required_block(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    prompt: str,
) -> str:
    while True:
        block = _read_block(input_fn, output_fn, prompt)
        if block:
            return block
        output_fn("This field cannot be empty.")


def _read_required_line(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    prompt: str,
) -> str:
    while True:
        value = _ask(input_fn, prompt).strip()
        if value:
            return value
        output_fn("This field cannot be empty.")


def _collect_governing_artifacts(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
    section: str,
    next_ga_id: int,
) -> tuple[list[GoverningArtifact], int]:
    artifacts: list[GoverningArtifact] = []
    while _read_yes_no(input_fn, output_fn, f"Add a {section} artifact? [y/N]: "):
        text = _read_required_block(
            input_fn,
            output_fn,
            (
                f"Enter {section} text. End with `{BLOCK_TERMINATOR}` on its own line. "
                f"To enter a literal `{BLOCK_TERMINATOR}` line, type `{ESCAPED_BLOCK_TERMINATOR}`."
            ),
        )
        mode = _read_choice(
            input_fn,
            output_fn,
            _persistence_prompt_for_section(section),
            _persistence_modes_for_section(section),
        )
        artifacts.append(GoverningArtifact(section, text, mode, next_ga_id))
        next_ga_id += 1
    return artifacts, next_ga_id


def _collect_scope_items(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> list[ScopeItem]:
    in_scope: list[ScopeItem] = []
    while True:
        add_item = _read_yes_no(input_fn, output_fn, "Add an in-scope item? [y/N]: ")
        if not add_item:
            if in_scope:
                break
            output_fn("At least one in-scope item is required.")
            continue
        item = _read_required_block(
            input_fn,
            output_fn,
            (
                f"Enter in-scope item text. End with `{BLOCK_TERMINATOR}` on its own line. "
                f"To enter a literal `{BLOCK_TERMINATOR}` line, type `{ESCAPED_BLOCK_TERMINATOR}`."
            ),
        )
        criterion = _read_required_block(
            input_fn,
            output_fn,
            (
                "Enter the corresponding acceptance criterion. "
                f"End with `{BLOCK_TERMINATOR}` on its own line. "
                f"To enter a literal `{BLOCK_TERMINATOR}` line, type `{ESCAPED_BLOCK_TERMINATOR}`."
            ),
        )
        in_scope.append(ScopeItem(item, [criterion]))
    return in_scope


def _collect_out_of_scope_items(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> list[str]:
    out_of_scope: list[str] = []
    while True:
        add_item = _read_yes_no(input_fn, output_fn, "Add an out-of-scope item? [y/N]: ")
        if not add_item:
            if out_of_scope:
                break
            output_fn("At least one out-of-scope item is required.")
            continue
        item = _read_required_block(
            input_fn,
            output_fn,
            (
                f"Enter out-of-scope item text. End with `{BLOCK_TERMINATOR}` on its own line. "
                f"To enter a literal `{BLOCK_TERMINATOR}` line, type `{ESCAPED_BLOCK_TERMINATOR}`."
            ),
        )
        out_of_scope.append(item)
    return out_of_scope


def _collect_assumptions(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> list[str]:
    assumptions: list[str] = []
    while _read_yes_no(input_fn, output_fn, "Add an assumption? [y/N]: "):
        assumptions.append(
            _read_required_block(
                input_fn,
                output_fn,
                (
                    f"Enter assumption text. End with `{BLOCK_TERMINATOR}` on its own line. "
                    f"To enter a literal `{BLOCK_TERMINATOR}` line, type `{ESCAPED_BLOCK_TERMINATOR}`."
                ),
            )
        )
    return assumptions


def collect_draft(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> MissionDraft:
    title = _read_required_line(input_fn, output_fn, "Enter the mission title: ")

    next_ga_id = 1
    sections: dict[str, list[GoverningArtifact]] = {}
    for section in GOVERNANCE_SECTIONS:
        artifacts, next_ga_id = _collect_governing_artifacts(input_fn, output_fn, section, next_ga_id)
        sections[section] = artifacts

    in_scope = _collect_scope_items(input_fn, output_fn)
    out_of_scope = _collect_out_of_scope_items(input_fn, output_fn)
    assumptions = _collect_assumptions(input_fn, output_fn)

    draft = MissionDraft(
        title=title,
        invariants=sections["Invariants"],
        external_constraints=sections["External Constraints"],
        beliefs=sections["Beliefs"],
        considerations=sections["Considerations"],
        in_scope=in_scope,
        out_of_scope=out_of_scope,
        assumptions=assumptions,
    )
    return draft


def _render_multiline_entry(prefix: str, text: str, continuation_indent: str) -> str:
    lines = text.split("\n")
    rendered = [f"{prefix}{lines[0]}"]
    rendered.extend(f"{continuation_indent}{line}" for line in lines[1:])
    return "\n".join(rendered)


def _render_governing_section(section: str, artifacts: list[GoverningArtifact]) -> str:
    if not artifacts:
        return ""
    body = "\n\n".join(
        _render_multiline_entry(f"- [GA{artifact.ga_id}] ", artifact.text, "  ")
        for artifact in artifacts
    )
    return f"## {section}\n\n{body}"


def _render_scope_section(in_scope: list[ScopeItem], out_of_scope: list[str]) -> str:
    in_scope_body = "\n\n".join(
        _render_multiline_entry("  - ", item.text, "    ") for item in in_scope
    )
    out_of_scope_body = "\n\n".join(
        _render_multiline_entry("  - ", item, "    ") for item in out_of_scope
    )
    return "\n".join(
        [
            "## Scope",
            "",
            "- **In scope:**",
            "",
            in_scope_body,
            "",
            "- **Out of scope:**",
            "",
            out_of_scope_body,
        ]
    )


def _render_assumptions_section(assumptions: list[str]) -> str:
    if not assumptions:
        return ""
    body = "\n\n".join(_render_multiline_entry("- ", item, "  ") for item in assumptions)
    return f"## Assumptions\n\n{body}"


def _render_acceptance_criteria(scope_criteria: list[str], artifacts: list[GoverningArtifact]) -> str:
    criteria = [
        *scope_criteria,
        *[f"Persist [GA{artifact.ga_id}] as {artifact.persistence_mode}." for artifact in artifacts],
    ]
    body = "\n\n".join(
        _render_multiline_entry(f"{index}. ", criterion, "   ")
        for index, criterion in enumerate(criteria, start=1)
    )
    return f"## Acceptance Criteria\n\n{body}"


def render_mission(draft: MissionDraft) -> str:
    sections = [f"# Mission: {draft.title}"]

    for section_name, artifacts in (
        ("Invariants", draft.invariants),
        ("External Constraints", draft.external_constraints),
        ("Beliefs", draft.beliefs),
        ("Considerations", draft.considerations),
    ):
        rendered = _render_governing_section(section_name, artifacts)
        if rendered:
            sections.append(rendered)

    sections.append(_render_scope_section(draft.in_scope, draft.out_of_scope))

    assumptions = _render_assumptions_section(draft.assumptions)
    if assumptions:
        sections.append(assumptions)

    sections.append(_render_acceptance_criteria(draft.all_scope_acceptance_criteria(), draft.all_governing_artifacts()))
    return "\n\n".join(sections) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactively generate a mission.md file.")
    parser.add_argument("path", nargs="?", default=None, help="Output path for mission.md")
    args = parser.parse_args()

    destination = Path(args.path) if args.path is not None else Path.cwd() / "mission.md"
    draft = collect_draft()
    content = render_mission(draft)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)
    print(f"Wrote {destination}")


if __name__ == "__main__":
    main()
