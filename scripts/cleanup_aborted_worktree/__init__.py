"""Cleanup script for permanently-aborted worktrees.

Removes the worktree via `git worktree remove` after enforcing two preconditions:
- The target worktree's bootstrap_check status must be ABORTED.
- The target worktree must be clean unless `--force` is passed.

After removal, the worktree's prior local branch is deleted only when it is
merged into the harness root branch (`main`) and has no other checkouts;
otherwise the branch is preserved.
"""

import dataclasses
import subprocess
import sys
from pathlib import Path

from scripts.bootstrap_check import list_worktrees

ROOT_BRANCH = "main"


@dataclasses.dataclass(frozen=True)
class CleanupResult:
    exit_code: int
    action: str  # "REMOVED" | "REFUSED"
    reason: str  # "OK" | "NOT_ABORTED" | "DIRTY"
    dirty_paths: tuple[str, ...] = ()
    branch: str | None = None
    branch_action: str = "NONE"  # "DELETED" | "PRESERVED" | "NONE"
    message: str = ""


def _parent_repo_root(worktree: Path) -> Path:
    out = subprocess.run(
        ["git", "-C", str(worktree), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return Path(out).parent


def _status_for(worktree: Path, parent: Path) -> str:
    target = worktree.resolve()
    for path, status in list_worktrees(parent):
        if path.resolve() == target:
            return status
    return "NOT_LISTED"


def _dirty_paths(worktree: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(worktree), "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [line[3:].strip() for line in out.splitlines() if line.strip()]


def _current_branch(worktree: Path) -> str | None:
    out = subprocess.run(
        ["git", "-C", str(worktree), "branch", "--show-current"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return out or None


def _branch_is_checked_out_elsewhere(parent: Path, branch: str) -> bool:
    out = subprocess.run(
        ["git", "-C", str(parent), "worktree", "list", "--porcelain"],
        capture_output=True, text=True, check=True,
    ).stdout
    target_ref = f"refs/heads/{branch}"
    return any(line.strip() == f"branch {target_ref}" for line in out.splitlines())


def _branch_is_merged_into_root(parent: Path, branch: str) -> bool:
    refs = subprocess.run(
        ["git", "-C", str(parent), "rev-parse", "--verify", "--quiet", ROOT_BRANCH],
        capture_output=True, text=True,
    )
    if refs.returncode != 0:
        return False
    r = subprocess.run(
        ["git", "-C", str(parent), "merge-base", "--is-ancestor", branch, ROOT_BRANCH],
        capture_output=True, text=True,
    )
    return r.returncode == 0


def cleanup(worktree_path: Path, force: bool = False) -> CleanupResult:
    wt = Path(worktree_path).resolve()
    parent = _parent_repo_root(wt)

    status = _status_for(wt, parent)
    if status != "ABORTED":
        return CleanupResult(
            exit_code=1,
            action="REFUSED",
            reason="NOT_ABORTED",
            message=f"Refused: worktree status is {status!r}, not 'ABORTED'.",
        )

    dirty = _dirty_paths(wt)
    if dirty and not force:
        listing = "\n  ".join(dirty)
        return CleanupResult(
            exit_code=1,
            action="REFUSED",
            reason="DIRTY",
            dirty_paths=tuple(dirty),
            message=f"Refused: working tree has uncommitted/untracked paths:\n  {listing}\nPass --force to override.",
        )

    branch = _current_branch(wt)

    remove_cmd = ["git", "-C", str(parent), "worktree", "remove", str(wt)]
    if force:
        remove_cmd.append("--force")
    subprocess.run(remove_cmd, check=True, capture_output=True)

    branch_action = "NONE"
    if branch:
        if _branch_is_checked_out_elsewhere(parent, branch) or not _branch_is_merged_into_root(parent, branch):
            branch_action = "PRESERVED"
        else:
            subprocess.run(
                ["git", "-C", str(parent), "branch", "-d", branch],
                check=True, capture_output=True,
            )
            branch_action = "DELETED"

    return CleanupResult(
        exit_code=0,
        action="REMOVED",
        reason="OK",
        branch=branch,
        branch_action=branch_action,
        message=f"Removed worktree {wt}; branch action: {branch_action}.",
    )


def main(argv: list[str] | None = None, stdout=None, stderr=None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    force = False
    positional: list[str] = []
    for a in args:
        if a == "--force":
            force = True
        else:
            positional.append(a)
    if len(positional) != 1:
        print("Usage: python -m scripts.cleanup_aborted_worktree <worktree-path> [--force]", file=err)
        return 2

    result = cleanup(Path(positional[0]), force=force)
    print(result.message, file=out if result.exit_code == 0 else err)
    return result.exit_code
