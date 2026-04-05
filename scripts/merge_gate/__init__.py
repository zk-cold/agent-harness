"""Merge gate: detect non-trivial merges and check worktree dirty state."""

import subprocess
from pathlib import Path

# Exact phase-reset texts drawn verbatim from:
#   .claude/commands/new-sdlc.md (Phase: Post-Implementation Review, Phase: 2-Critic Post-Implementation Review)
VARIANTS: dict[str, str] = {
    "new-sdlc-fast-path": (
        "Phase: Post-Implementation Review (Fast Path) - rerun verification on the merged state, "
        "rewrite completion-review runtime artifacts, and submit that state to a fresh critic."
    ),
    "new-sdlc-normal": (
        "Phase: 2-Critic Post-Implementation Review - rerun verification on the merged state, "
        "rewrite completion-review runtime artifacts, submit that state to the first fresh critic, "
        "and if it approves then to a second fresh critic."
    ),
}

_HANDOFF_TEMPLATE = (
    "## Next / Ongoing Step\n\n{reset_text}\n\n## Known Failed Attempts\n\nNone\n"
)


def classify_merge_output(output: str, returncode: int) -> str:
    """Classify git merge output as TRIVIAL, NON_TRIVIAL, or MERGE_ERROR.

    Trivial (CLAUDE.md Trivial Merge Qualification): output contains "Already up to date." OR
    git exits 0 and output contains "Fast-forward" with no "CONFLICT" markers.
    Non-trivial: output contains "CONFLICT", or git exits 0 with no "Fast-forward".
    Merge error: git exits non-zero with no "CONFLICT" markers.
    """
    if "Already up to date." in output:
        return "TRIVIAL"
    if returncode == 0 and "Fast-forward" in output and "CONFLICT" not in output:
        return "TRIVIAL"
    if "CONFLICT" in output:
        return "NON_TRIVIAL"
    if returncode != 0:
        return "MERGE_ERROR"
    # Three-way merge commit: exits 0, no "Fast-forward", no "CONFLICT"
    return "NON_TRIVIAL"


def check_dirty(worktree_path: Path) -> tuple[str, list[str]]:
    """Return (status, affected_paths) for the worktree.

    status is "CLEAN" (exit 0) or "DIRTY" (exit 1).
    affected_paths lists every path with an uncommitted change.
    """
    result = subprocess.run(
        ["git", "-C", str(worktree_path), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if lines:
        paths = [line[3:].strip() for line in lines]
        return "DIRTY", paths
    return "CLEAN", []


def do_merge(
    git_work_dir: Path, handoff_dir: Path, variant: str, branch: str
) -> tuple[str, int]:
    """Run git merge and gate on the result.

    Returns (output_message, exit_code):
      "TRIVIAL", 0                      — trivial merge (already up to date or fast-forward)
      "NON_TRIVIAL", 2                  — non-trivial; handoff.md rewritten with phase-reset text
      "MERGE_ERROR\\n<stderr>", 3       — git failure other than conflicts
      "HANDOFF_MISSING", 4              — non-trivial but handoff.md absent in handoff_dir
      "INVALID_VARIANT: <variant>", 1   — unrecognised variant string
    """
    if variant not in VARIANTS:
        return f"INVALID_VARIANT: {variant}", 1

    result = subprocess.run(
        ["git", "-C", str(git_work_dir), "merge", branch],
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    classification = classify_merge_output(combined, result.returncode)

    if classification == "TRIVIAL":
        return "TRIVIAL", 0

    if classification == "MERGE_ERROR":
        return f"MERGE_ERROR\n{result.stderr.strip()}", 3

    # NON_TRIVIAL
    handoff = handoff_dir / "handoff.md"
    if not handoff.exists():
        return "HANDOFF_MISSING", 4

    handoff.write_text(_HANDOFF_TEMPLATE.format(reset_text=VARIANTS[variant]))
    return "NON_TRIVIAL", 2


def main() -> None:
    import sys

    args = sys.argv[1:]
    if not args:
        print(
            "Usage: python -m scripts.merge_gate <subcommand> [args...]",
            file=sys.stderr,
        )
        sys.exit(1)

    subcommand = args[0]

    if subcommand == "check-dirty":
        if len(args) != 2:
            print(
                "Usage: python -m scripts.merge_gate check-dirty <worktree_path>",
                file=sys.stderr,
            )
            sys.exit(1)
        status, paths = check_dirty(Path(args[1]))
        print(status)
        for p in paths:
            print(p)
        sys.exit(0 if status == "CLEAN" else 1)

    elif subcommand == "do-merge":
        if len(args) != 5:
            print(
                "Usage: python -m scripts.merge_gate do-merge "
                "<git_work_dir> <handoff_dir> <variant> <branch>",
                file=sys.stderr,
            )
            sys.exit(1)
        message, code = do_merge(
            Path(args[1]), Path(args[2]), args[3], args[4]
        )
        print(message)
        sys.exit(code)

    else:
        print(f"Unknown subcommand: {subcommand!r}", file=sys.stderr)
        sys.exit(1)
