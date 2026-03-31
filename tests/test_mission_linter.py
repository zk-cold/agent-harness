import subprocess
import sys
from pathlib import Path

import pytest

from scripts.mission_linter import lint

VALID = """\
# Mission: Test mission

## Scope

- **In scope:**
  - Some deliverable

- **Out of scope:**
  - Something excluded

## Dependencies & Assumptions

- coverage tool is available via pytest-cov

## Acceptance Criteria

1. The thing works.
"""


def write(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "mission.md"
    p.write_text(content)
    return p


# --- AC1: lint() signature ---

def test_lint_returns_list_for_valid(tmp_path):
    p = write(tmp_path, VALID)
    result = lint(p)
    assert isinstance(result, list)
    assert result == []


# --- AC3: TITLE_FORMAT ---

def test_title_format_missing(tmp_path):
    content = VALID.replace("# Mission: Test mission", "## Not a title")
    p = write(tmp_path, content)
    assert "TITLE_FORMAT" in lint(p)


def test_title_format_empty_title(tmp_path):
    content = VALID.replace("# Mission: Test mission", "# Mission:")
    p = write(tmp_path, content)
    assert "TITLE_FORMAT" in lint(p)


def test_title_format_whitespace_only(tmp_path):
    content = VALID.replace("# Mission: Test mission", "# Mission:   ")
    p = write(tmp_path, content)
    assert "TITLE_FORMAT" in lint(p)


def test_title_format_valid(tmp_path):
    p = write(tmp_path, VALID)
    assert "TITLE_FORMAT" not in lint(p)


# --- AC4: MISSING_SCOPE ---

def test_missing_scope(tmp_path):
    content = VALID.replace("## Scope", "## Something Else")
    p = write(tmp_path, content)
    assert "MISSING_SCOPE" in lint(p)


def test_no_missing_scope(tmp_path):
    p = write(tmp_path, VALID)
    assert "MISSING_SCOPE" not in lint(p)


# --- AC5: MISSING_AC ---

def test_missing_ac(tmp_path):
    content = VALID.replace("## Acceptance Criteria", "## Done When")
    p = write(tmp_path, content)
    assert "MISSING_AC" in lint(p)


def test_no_missing_ac(tmp_path):
    p = write(tmp_path, VALID)
    assert "MISSING_AC" not in lint(p)


# --- AC6: SCOPE_MISSING_IN_SCOPE ---

def test_scope_missing_in_scope_absent(tmp_path):
    content = VALID.replace("- **In scope:**\n  - Some deliverable\n", "")
    p = write(tmp_path, content)
    assert "SCOPE_MISSING_IN_SCOPE" in lint(p)


def test_scope_missing_in_scope_no_bullets(tmp_path):
    content = VALID.replace(
        "- **In scope:**\n  - Some deliverable",
        "- **In scope:**"
    )
    p = write(tmp_path, content)
    assert "SCOPE_MISSING_IN_SCOPE" in lint(p)


def test_scope_in_scope_present(tmp_path):
    p = write(tmp_path, VALID)
    assert "SCOPE_MISSING_IN_SCOPE" not in lint(p)


# --- AC7: SCOPE_MISSING_OUT_OF_SCOPE ---

def test_scope_missing_out_of_scope_absent(tmp_path):
    content = VALID.replace("- **Out of scope:**\n  - Something excluded\n", "")
    p = write(tmp_path, content)
    assert "SCOPE_MISSING_OUT_OF_SCOPE" in lint(p)


def test_scope_missing_out_of_scope_no_bullets(tmp_path):
    content = VALID.replace(
        "- **Out of scope:**\n  - Something excluded",
        "- **Out of scope:**"
    )
    p = write(tmp_path, content)
    assert "SCOPE_MISSING_OUT_OF_SCOPE" in lint(p)


def test_scope_out_of_scope_present(tmp_path):
    p = write(tmp_path, VALID)
    assert "SCOPE_MISSING_OUT_OF_SCOPE" not in lint(p)


# --- AC8: AC_EMPTY ---

def test_ac_empty(tmp_path):
    content = VALID.replace("1. The thing works.", "")
    p = write(tmp_path, content)
    assert "AC_EMPTY" in lint(p)


def test_ac_not_empty(tmp_path):
    p = write(tmp_path, VALID)
    assert "AC_EMPTY" not in lint(p)


# --- AC9: SECTION_ORDER ---

def test_section_order_violation(tmp_path):
    # Dependencies & Assumptions before Scope = wrong order
    content = """\
# Mission: Test mission

## Dependencies & Assumptions

- coverage available

## Scope

- **In scope:**
  - Deliverable

- **Out of scope:**
  - Excluded

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "SECTION_ORDER" in lint(p)


def test_section_order_optional_before_scope(tmp_path):
    # Invariants before Scope is correct
    content = """\
# Mission: Test mission

## Invariants

- Some invariant. Violation: if X then Y.

## Scope

- **In scope:**
  - Deliverable

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- coverage available

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "SECTION_ORDER" not in lint(p)


def test_section_order_ac_before_scope(tmp_path):
    content = """\
# Mission: Test mission

## Acceptance Criteria

1. Works.

## Scope

- **In scope:**
  - Deliverable

- **Out of scope:**
  - Excluded
"""
    p = write(tmp_path, content)
    assert "SECTION_ORDER" in lint(p)


def test_section_order_valid(tmp_path):
    p = write(tmp_path, VALID)
    assert "SECTION_ORDER" not in lint(p)


# --- AC10: EMPTY_OPTIONAL_SECTION ---

def test_empty_optional_invariants(tmp_path):
    content = """\
# Mission: Test mission

## Invariants

## Scope

- **In scope:**
  - Deliverable

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- coverage available

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "EMPTY_OPTIONAL_SECTION" in lint(p)


def test_empty_optional_considerations(tmp_path):
    content = """\
# Mission: Test mission

## Important Considerations

## Scope

- **In scope:**
  - Deliverable

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- coverage available

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "EMPTY_OPTIONAL_SECTION" in lint(p)


def test_empty_optional_deps(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - Deliverable

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "EMPTY_OPTIONAL_SECTION" in lint(p)


def test_no_empty_optional_sections(tmp_path):
    p = write(tmp_path, VALID)
    assert "EMPTY_OPTIONAL_SECTION" not in lint(p)


# --- AC11: COVERAGE_TOOL_MISSING ---

def test_coverage_tool_missing(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - Some deliverable

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- Something unrelated

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "COVERAGE_TOOL_MISSING" in lint(p)


def test_coverage_tool_in_scope(tmp_path):
    content = VALID.replace(
        "- **In scope:**\n  - Some deliverable",
        "- **In scope:**\n  - Some coverage tool setup"
    )
    p = write(tmp_path, content)
    assert "COVERAGE_TOOL_MISSING" not in lint(p)


def test_coverage_tool_in_deps(tmp_path):
    p = write(tmp_path, VALID)  # VALID has "coverage" in D&A
    assert "COVERAGE_TOOL_MISSING" not in lint(p)


def test_coverage_tool_tdd_exempt_in_deps(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - Some doc.md

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- TDD-exempt because all deliverables are non-executable.

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "COVERAGE_TOOL_MISSING" not in lint(p)


# --- AC12: TDD_EXEMPT_WRONG_SECTION ---

def test_tdd_exempt_in_scope(tmp_path):
    content = VALID.replace(
        "  - Some deliverable",
        "  - TDD-exempt documentation file"
    )
    p = write(tmp_path, content)
    assert "TDD_EXEMPT_WRONG_SECTION" in lint(p)


def test_tdd_exempt_in_ac(tmp_path):
    content = VALID.replace("1. The thing works.", "1. TDD-exempt check passes.")
    p = write(tmp_path, content)
    assert "TDD_EXEMPT_WRONG_SECTION" in lint(p)


def test_tdd_exempt_in_deps_no_violation(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - Some doc.md

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- TDD-exempt because all deliverables are non-executable.

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "TDD_EXEMPT_WRONG_SECTION" not in lint(p)


# --- AC13: TDD_EXEMPT_EXECUTABLE_ARTIFACTS ---

def test_tdd_exempt_with_py_in_scope(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - scripts/foo.py

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- TDD-exempt because all deliverables are non-executable.

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "TDD_EXEMPT_EXECUTABLE_ARTIFACTS" in lint(p)


def test_tdd_exempt_with_script_word_in_scope(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - A shell script for setup

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- TDD-exempt because all deliverables are non-executable.

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "TDD_EXEMPT_EXECUTABLE_ARTIFACTS" in lint(p)


def test_tdd_exempt_with_md_only_in_scope(tmp_path):
    content = """\
# Mission: Test mission

## Scope

- **In scope:**
  - docs/readme.md

- **Out of scope:**
  - Excluded

## Dependencies & Assumptions

- TDD-exempt because all deliverables are non-executable.

## Acceptance Criteria

1. Works.
"""
    p = write(tmp_path, content)
    assert "TDD_EXEMPT_EXECUTABLE_ARTIFACTS" not in lint(p)


def test_no_tdd_exempt_no_executable_check(tmp_path):
    # Even with .py in scope, no violation if TDD-exempt is not claimed
    p = write(tmp_path, VALID)
    assert "TDD_EXEMPT_EXECUTABLE_ARTIFACTS" not in lint(p)


# --- AC2: __main__ entry point ---

def test_main_exits_zero_for_valid(tmp_path):
    p = write(tmp_path, VALID)
    result = subprocess.run(
        [sys.executable, "-m", "scripts.mission_linter", str(p)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_main_exits_nonzero_for_invalid(tmp_path):
    p = write(tmp_path, "no title here")
    result = subprocess.run(
        [sys.executable, "-m", "scripts.mission_linter", str(p)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_main_prints_violations(tmp_path):
    p = write(tmp_path, "no title here")
    result = subprocess.run(
        [sys.executable, "-m", "scripts.mission_linter", str(p)],
        capture_output=True,
        text=True,
    )
    assert "TITLE_FORMAT" in result.stdout
