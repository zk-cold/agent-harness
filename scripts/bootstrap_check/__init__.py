#!/usr/bin/env python3
"""Session-start bootstrap checker for the agent harness.

Prints exactly one status value to stdout and exits 0 on success.

Status values:
  ROOT_ARTIFACTS        handoff.md or mission.md found at repo root
  MULTIPLE_WORKTREES    two or more worktrees under .claude/worktrees/
  ONE_WORKTREE_NO_HANDOFF  one worktree, no handoff.md at its root
  ONE_WORKTREE_ABORTED  one worktree, handoff.md contains the abort sentinel
  ONE_WORKTREE_RESUMABLE   one worktree, handoff.md present and resumable
  NO_WORKTREE           no worktrees and no root runtime artifacts
"""

import sys
from pathlib import Path

ABORT_SENTINEL = "This mission is already aborted and must not be resumed"


def check(repo_root: Path) -> str:
    """Return the bootstrap status for the given repo root."""
    # AC3/AC9: root artifacts take priority over worktree state
    if (repo_root / "handoff.md").exists() or (repo_root / "mission.md").exists():
        return "ROOT_ARTIFACTS"

    worktrees_dir = repo_root / ".claude" / "worktrees"
    if not worktrees_dir.exists():
        return "NO_WORKTREE"

    worktrees = [d for d in worktrees_dir.iterdir() if d.is_dir()]

    if len(worktrees) == 0:
        return "NO_WORKTREE"
    if len(worktrees) >= 2:
        return "MULTIPLE_WORKTREES"

    # Exactly one worktree
    worktree = worktrees[0]
    handoff = worktree / "handoff.md"
    if not handoff.exists():
        return "ONE_WORKTREE_NO_HANDOFF"
    if ABORT_SENTINEL in handoff.read_text():
        return "ONE_WORKTREE_ABORTED"
    return "ONE_WORKTREE_RESUMABLE"


def main() -> None:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    print(check(repo_root))


if __name__ == "__main__":
    main()
