from pathlib import Path

from scripts.bootstrap_check import ABORT_SENTINEL, check


# --- ROOT_ARTIFACTS (AC3, AC9) ---

def test_root_artifacts_handoff_only(tmp_path):
    (tmp_path / "handoff.md").write_text("content")
    assert check(tmp_path) == "ROOT_ARTIFACTS"


def test_root_artifacts_mission_only(tmp_path):
    (tmp_path / "mission.md").write_text("content")
    assert check(tmp_path) == "ROOT_ARTIFACTS"


def test_root_artifacts_both(tmp_path):
    (tmp_path / "handoff.md").write_text("content")
    (tmp_path / "mission.md").write_text("content")
    assert check(tmp_path) == "ROOT_ARTIFACTS"


def test_root_artifacts_priority_over_worktrees(tmp_path):
    """ROOT_ARTIFACTS is returned even when worktrees exist (AC9)."""
    (tmp_path / "handoff.md").write_text("content")
    worktree = tmp_path / ".claude" / "worktrees" / "some-worktree"
    worktree.mkdir(parents=True)
    assert check(tmp_path) == "ROOT_ARTIFACTS"


# --- NO_WORKTREE (AC8) ---

def test_no_worktree_directory_absent(tmp_path):
    assert check(tmp_path) == "NO_WORKTREE"


def test_no_worktree_directory_empty(tmp_path):
    (tmp_path / ".claude" / "worktrees").mkdir(parents=True)
    assert check(tmp_path) == "NO_WORKTREE"


# --- MULTIPLE_WORKTREES (AC4) ---

def test_multiple_worktrees_two(tmp_path):
    worktrees = tmp_path / ".claude" / "worktrees"
    (worktrees / "a").mkdir(parents=True)
    (worktrees / "b").mkdir()
    assert check(tmp_path) == "MULTIPLE_WORKTREES"


def test_multiple_worktrees_three(tmp_path):
    worktrees = tmp_path / ".claude" / "worktrees"
    for name in ("a", "b", "c"):
        (worktrees / name).mkdir(parents=True)
    assert check(tmp_path) == "MULTIPLE_WORKTREES"


# --- ONE_WORKTREE_NO_HANDOFF (AC5) ---

def test_one_worktree_no_handoff(tmp_path):
    (tmp_path / ".claude" / "worktrees" / "wt").mkdir(parents=True)
    assert check(tmp_path) == "ONE_WORKTREE_NO_HANDOFF"


# --- ONE_WORKTREE_ABORTED (AC6) ---

def test_one_worktree_aborted(tmp_path):
    worktree = tmp_path / ".claude" / "worktrees" / "wt"
    worktree.mkdir(parents=True)
    (worktree / "handoff.md").write_text(
        f"## Next / Ongoing Step\n\nAborted: something. {ABORT_SENTINEL}. Await a fresh user request."
    )
    assert check(tmp_path) == "ONE_WORKTREE_ABORTED"


# --- ONE_WORKTREE_RESUMABLE (AC7) ---

def test_one_worktree_resumable(tmp_path):
    worktree = tmp_path / ".claude" / "worktrees" / "wt"
    worktree.mkdir(parents=True)
    (worktree / "handoff.md").write_text(
        "## Next / Ongoing Step\n\nPhase: Execute in Worktree\n\n## Known Failed Attempts\n\nNone"
    )
    assert check(tmp_path) == "ONE_WORKTREE_RESUMABLE"


def test_one_worktree_resumable_only_handoff_no_sentinel(tmp_path):
    worktree = tmp_path / ".claude" / "worktrees" / "wt"
    worktree.mkdir(parents=True)
    (worktree / "handoff.md").write_text("Phase: 2-Critic Review")
    assert check(tmp_path) == "ONE_WORKTREE_RESUMABLE"
