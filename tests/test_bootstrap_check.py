from pathlib import Path

from scripts.bootstrap_check import ABORT_SENTINEL, check, list_worktrees


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


# --- list_worktrees ---

def test_list_worktrees_no_directory(tmp_path):
    assert list_worktrees(tmp_path) == []


def test_list_worktrees_empty_directory(tmp_path):
    (tmp_path / ".claude" / "worktrees").mkdir(parents=True)
    assert list_worktrees(tmp_path) == []


def test_list_worktrees_single_resumable(tmp_path):
    wt = tmp_path / ".claude" / "worktrees" / "wt"
    wt.mkdir(parents=True)
    (wt / "handoff.md").write_text("Phase: Execute in Worktree")
    result = list_worktrees(tmp_path)
    assert result == [(wt, "RESUMABLE")]


def test_list_worktrees_single_aborted(tmp_path):
    wt = tmp_path / ".claude" / "worktrees" / "wt"
    wt.mkdir(parents=True)
    (wt / "handoff.md").write_text(
        f"Aborted: something. {ABORT_SENTINEL}. Await a fresh user request."
    )
    result = list_worktrees(tmp_path)
    assert result == [(wt, "ABORTED")]


def test_list_worktrees_single_no_handoff(tmp_path):
    wt = tmp_path / ".claude" / "worktrees" / "wt"
    wt.mkdir(parents=True)
    result = list_worktrees(tmp_path)
    assert result == [(wt, "NO_HANDOFF")]


def test_list_worktrees_two_different_statuses(tmp_path):
    worktrees = tmp_path / ".claude" / "worktrees"
    wt_a = worktrees / "a"
    wt_b = worktrees / "b"
    wt_a.mkdir(parents=True)
    wt_b.mkdir()
    (wt_a / "handoff.md").write_text("Phase: Execute in Worktree")
    (wt_b / "handoff.md").write_text(
        f"Aborted: blocker. {ABORT_SENTINEL}. Await fresh request."
    )
    result = list_worktrees(tmp_path)
    assert result == [(wt_a, "RESUMABLE"), (wt_b, "ABORTED")]


def test_list_worktrees_skips_non_directory_entries(tmp_path):
    worktrees = tmp_path / ".claude" / "worktrees"
    wt = worktrees / "wt"
    wt.mkdir(parents=True)
    (wt / "handoff.md").write_text("Phase: Execute in Worktree")
    # A file in the worktrees dir should be skipped
    (worktrees / "not-a-dir.txt").write_text("ignored")
    result = list_worktrees(tmp_path)
    assert result == [(wt, "RESUMABLE")]
