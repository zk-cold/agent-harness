"""mission.md structural linter.

Returns a list of violation strings (empty = no violations).
"""

import re
from pathlib import Path

# Prescribed section order from mission-schema.md
_SECTION_ORDER = [
    "Invariants",
    "Beliefs",
    "Considerations",
    "Scope",
    "Assumptions",
    "Acceptance Criteria",
]

_OPTIONAL_SECTIONS = {"Invariants", "Beliefs", "Considerations", "Assumptions"}

_EXECUTABLE_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".go", ".rb", ".rs"}


def _h2_sections(text: str) -> list[tuple[str, str]]:
    """Return list of (heading, body) for every ## section in text."""
    pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections = []
    for i, m in enumerate(matches):
        heading = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        sections.append((heading, body))
    return sections


def _section_body(sections: list[tuple[str, str]], name: str) -> str | None:
    for heading, body in sections:
        if heading == name:
            return body
    return None


def _has_bullet(text: str) -> bool:
    return bool(re.search(r"^\s*-\s+\S", text, re.MULTILINE))


def _in_scope_bullets(scope_body: str) -> str:
    """Return the text of the In scope subsection, or empty string."""
    m = re.search(r"\*\*In scope:\*\*(.*?)(?=\*\*Out of scope:|$)", scope_body, re.DOTALL)
    return m.group(1) if m else ""


def lint(path: Path) -> list[str]:
    text = path.read_text()
    violations: list[str] = []
    sections = _h2_sections(text)
    section_names = [h for h, _ in sections]

    # AC3: TITLE_FORMAT
    first_line = text.split("\n", 1)[0]
    m = re.match(r"^# Mission:\s*(.+)$", first_line)
    if not m or not m.group(1).strip():
        violations.append("TITLE_FORMAT")

    # AC4: MISSING_SCOPE
    scope_body = _section_body(sections, "Scope")
    if scope_body is None:
        violations.append("MISSING_SCOPE")

    # AC5: MISSING_AC
    ac_body = _section_body(sections, "Acceptance Criteria")
    if ac_body is None:
        violations.append("MISSING_AC")

    # AC6 & AC7: SCOPE subsections
    if scope_body is not None:
        in_scope_text = _in_scope_bullets(scope_body)
        if not _has_bullet(in_scope_text):
            violations.append("SCOPE_MISSING_IN_SCOPE")

        m_out = re.search(r"\*\*Out of scope:\*\*(.*?)$", scope_body, re.DOTALL)
        out_scope_text = m_out.group(1) if m_out else ""
        if not _has_bullet(out_scope_text):
            violations.append("SCOPE_MISSING_OUT_OF_SCOPE")

    # AC8: AC_EMPTY
    if ac_body is not None and not ac_body.strip():
        violations.append("AC_EMPTY")

    # AC9: SECTION_ORDER
    present_ordered = [s for s in _SECTION_ORDER if s in section_names]
    actual_ordered = [s for s in section_names if s in _SECTION_ORDER]
    if actual_ordered != present_ordered:
        violations.append("SECTION_ORDER")

    # AC10: EMPTY_OPTIONAL_SECTION
    for name in _OPTIONAL_SECTIONS:
        body = _section_body(sections, name)
        if body is not None and not body.strip():
            violations.append("EMPTY_OPTIONAL_SECTION")

    # AC11: COVERAGE_TOOL_MISSING
    deps_body = _section_body(sections, "Assumptions") or ""
    in_scope_text_for_coverage = _in_scope_bullets(scope_body) if scope_body is not None else ""
    has_coverage_in_scope = bool(re.search(r"\bcoverage\b", in_scope_text_for_coverage, re.IGNORECASE))
    has_coverage_in_deps = bool(re.search(r"\bcoverage\b", deps_body, re.IGNORECASE))
    has_tdd_exempt_in_deps = "TDD-exempt" in deps_body
    if not (has_coverage_in_scope or has_coverage_in_deps or has_tdd_exempt_in_deps):
        violations.append("COVERAGE_TOOL_MISSING")

    # AC12: TDD_EXEMPT_WRONG_SECTION
    # "TDD-exempt" is only allowed in the Assumptions section
    text_without_deps = text
    if deps_body:
        # Remove the deps section content from the text we check
        deps_start = text.find(deps_body)
        text_without_deps = text[:deps_start] + text[deps_start + len(deps_body):]
    if "TDD-exempt" in text_without_deps:
        violations.append("TDD_EXEMPT_WRONG_SECTION")

    # AC13: TDD_EXEMPT_EXECUTABLE_ARTIFACTS
    if has_tdd_exempt_in_deps and scope_body is not None:
        in_scope = _in_scope_bullets(scope_body)
        has_exec = any(ext in in_scope for ext in _EXECUTABLE_EXTENSIONS)
        has_script_word = bool(re.search(r"\bscript\b", in_scope, re.IGNORECASE))
        if has_exec or has_script_word:
            violations.append("TDD_EXEMPT_EXECUTABLE_ARTIFACTS")

    return violations
