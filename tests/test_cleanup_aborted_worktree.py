"""Tests for scripts/cleanup_aborted_worktree (mission invariants S1-S4)."""

import io
import subprocess
import sys
from pathlib import Path

from scripts.bootstrap_check import ABORT_SENTINEL
from scripts.cleanup_aborted_worktree import cleanup, main


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _make_main_repo(path: Path) -> Path:
    subprocess.run(["git", "init", "--initial-branch=main", str(path)], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=path, check=True, capture_output=True)
    (path / "seed.txt").write_text("seed\n")
    subprocess.run(["git", "add", "."], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "seed"], cwd=path, check=True, capture_output=True)
    return path


def _add_worktree(repo: Path, name: str, branch: str | None = None, start_point: str = "main") -> Path:
    wt_path = repo / ".claude" / "worktrees" / name
    wt_path.parent.mkdir(parents=True, exist_ok=True)
    branch = branch or f"wt/{name}"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "-b", branch, str(wt_path), start_point],
        check=True,
        capture_output=True,
    )
    return wt_path


def _write_handoff(wt: Path, aborted: bool) -> None:
    body = "## Next / Ongoing Step\n\n"
    if aborted:
        body += f"Aborted. {ABORT_SENTINEL}.\n"
    else:
        body += "Phase: Mission Creation - Interview\n"
    body += "\n## Known Failed Attempts\n\nNone\n"
    (wt / "handoff.md").write_text(body)


def _worktree_listed(repo: Path, wt: Path) -> bool:
    out = subprocess.run(
        ["git", "-C", str(repo), "worktree", "list", "--porcelain"],
        capture_output=True, text=True, check=True,
    ).stdout
    return str(wt.resolve()) in out


def _branches(repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# S1 — Aborted-Only Cleanup
# ---------------------------------------------------------------------------

def test_s1_refuses_when_worktree_is_resumable(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "resumable")
    _write_handoff(wt, aborted=False)

    result = cleanup(wt)

    assert result.exit_code != 0
    assert result.action == "REFUSED"
    assert result.reason == "NOT_ABORTED"
    assert _worktree_listed(repo, wt)
    assert wt.exists()


def test_s1_refuses_when_worktree_has_no_handoff(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "no-handoff")
    # Intentionally no handoff.md written.

    result = cleanup(wt)

    assert result.exit_code != 0
    assert result.action == "REFUSED"
    assert result.reason == "NOT_ABORTED"
    assert _worktree_listed(repo, wt)
    assert wt.exists()


def test_s1_succeeds_when_worktree_is_aborted_and_clean(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "aborted-clean")
    _write_handoff(wt, aborted=True)
    subprocess.run(["git", "-C", str(wt), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-m", "abort"], check=True, capture_output=True)

    result = cleanup(wt)

    assert result.exit_code == 0
    assert result.action == "REMOVED"


# ---------------------------------------------------------------------------
# S2 — Dirty Working Tree Refusal
# ---------------------------------------------------------------------------

def test_s2_refuses_when_dirty_without_force(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "dirty")
    _write_handoff(wt, aborted=True)
    # Leave handoff.md uncommitted (it is untracked from the parent's index) and add an extra untracked file.
    (wt / "scratch.txt").write_text("temp\n")

    result = cleanup(wt, force=False)

    assert result.exit_code != 0
    assert result.action == "REFUSED"
    assert result.reason == "DIRTY"
    # Must list the dirty paths
    assert any("handoff.md" in p for p in result.dirty_paths)
    assert any("scratch.txt" in p for p in result.dirty_paths)
    assert _worktree_listed(repo, wt)
    assert wt.exists()


def test_s2_proceeds_when_dirty_with_force(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "dirty-forced")
    _write_handoff(wt, aborted=True)
    (wt / "scratch.txt").write_text("temp\n")  # untracked, dirty

    result = cleanup(wt, force=True)

    assert result.exit_code == 0
    assert result.action == "REMOVED"
    assert not _worktree_listed(repo, wt)


def test_s2_cli_refusal_message_lists_dirty_paths(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "dirty-cli")
    _write_handoff(wt, aborted=True)
    (wt / "scratch.txt").write_text("temp\n")

    proc = subprocess.run(
        [sys.executable, "-m", "scripts.cleanup_aborted_worktree", str(wt)],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    combined = proc.stdout + proc.stderr
    assert "scratch.txt" in combined
    assert "handoff.md" in combined
    assert _worktree_listed(repo, wt)


# ---------------------------------------------------------------------------
# S3 — Worktree Removal
# ---------------------------------------------------------------------------

def test_s3_successful_run_removes_worktree(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "remove-me")
    _write_handoff(wt, aborted=True)
    subprocess.run(["git", "-C", str(wt), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-m", "abort"], check=True, capture_output=True)

    result = cleanup(wt)

    assert result.exit_code == 0
    assert result.action == "REMOVED"
    assert not _worktree_listed(repo, wt)
    assert not wt.exists()


# ---------------------------------------------------------------------------
# S4 — Branch Safe-Delete
# ---------------------------------------------------------------------------

def test_s4_deletes_branch_when_merged_into_main_and_no_other_checkouts(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "merged", branch="wt/merged")
    _write_handoff(wt, aborted=True)
    subprocess.run(["git", "-C", str(wt), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-m", "abort"], check=True, capture_output=True)
    # Merge the branch's work into main so it is fully merged.
    subprocess.run(["git", "-C", str(repo), "merge", "--no-ff", "-m", "merge", "wt/merged"], check=True, capture_output=True)

    assert "wt/merged" in _branches(repo)

    result = cleanup(wt)

    assert result.exit_code == 0
    assert result.action == "REMOVED"
    assert result.branch == "wt/merged"
    assert result.branch_action == "DELETED"
    assert "wt/merged" not in _branches(repo)


def test_s4_preserves_branch_when_not_merged_into_main(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "unmerged", branch="wt/unmerged")
    _write_handoff(wt, aborted=True)
    # Commit so the branch has work beyond main.
    subprocess.run(["git", "-C", str(wt), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-m", "diverge"], check=True, capture_output=True)

    result = cleanup(wt)

    assert result.exit_code == 0
    assert result.action == "REMOVED"
    assert result.branch == "wt/unmerged"
    assert result.branch_action == "PRESERVED"
    assert "wt/unmerged" in _branches(repo)


def test_s1_refuses_when_path_is_not_a_listed_worktree(tmp_path):
    # The main repo itself is not under .claude/worktrees/, so list_worktrees won't list it
    # and the status resolves to NOT_LISTED, which is not ABORTED.
    repo = _make_main_repo(tmp_path / "repo")

    result = cleanup(repo)

    assert result.exit_code != 0
    assert result.action == "REFUSED"
    assert result.reason == "NOT_ABORTED"


def test_s4_preserves_branch_when_root_branch_absent(tmp_path):
    # Repo whose default branch is not 'main' → _branch_is_merged_into_root returns False.
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "--initial-branch=master", str(repo)], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=repo, check=True, capture_output=True)
    (repo / "seed.txt").write_text("seed\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "seed"], cwd=repo, check=True, capture_output=True)
    wt = _add_worktree(repo, "no-main", branch="wt/no-main", start_point="master")
    _write_handoff(wt, aborted=True)
    subprocess.run(["git", "-C", str(wt), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-m", "abort"], check=True, capture_output=True)

    result = cleanup(wt)

    assert result.exit_code == 0
    assert result.action == "REMOVED"
    assert result.branch == "wt/no-main"
    assert result.branch_action == "PRESERVED"
    assert "wt/no-main" in _branches(repo)


def test_main_usage_error_on_no_args():
    out, err = io.StringIO(), io.StringIO()
    rc = main(argv=[], stdout=out, stderr=err)
    assert rc != 0
    assert "Usage" in err.getvalue()


def test_main_usage_error_on_multiple_paths():
    out, err = io.StringIO(), io.StringIO()
    rc = main(argv=["a", "b"], stdout=out, stderr=err)
    assert rc != 0


def test_main_success_writes_message_to_stdout(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "via-main", branch="wt/via-main")
    _write_handoff(wt, aborted=True)
    subprocess.run(["git", "-C", str(wt), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt), "commit", "-m", "abort"], check=True, capture_output=True)

    out, err = io.StringIO(), io.StringIO()
    rc = main(argv=[str(wt)], stdout=out, stderr=err)

    assert rc == 0
    assert "Removed worktree" in out.getvalue()
    assert err.getvalue() == ""


def test_main_refusal_writes_message_to_stderr(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "refuse-via-main")
    _write_handoff(wt, aborted=False)

    out, err = io.StringIO(), io.StringIO()
    rc = main(argv=[str(wt)], stdout=out, stderr=err)

    assert rc != 0
    assert "Refused" in err.getvalue()
    assert out.getvalue() == ""


def test_main_force_flag_proceeds_when_dirty(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    wt = _add_worktree(repo, "force-via-main")
    _write_handoff(wt, aborted=True)
    (wt / "extra.txt").write_text("x\n")

    out, err = io.StringIO(), io.StringIO()
    rc = main(argv=[str(wt), "--force"], stdout=out, stderr=err)

    assert rc == 0
    assert not _worktree_listed(repo, wt)


def test_s4_preserves_branch_when_other_worktree_has_it_checked_out(tmp_path):
    repo = _make_main_repo(tmp_path / "repo")
    # Aborted worktree A on branch wt/shared.
    wt_a = _add_worktree(repo, "shared-a", branch="wt/shared")
    _write_handoff(wt_a, aborted=True)
    subprocess.run(["git", "-C", str(wt_a), "add", "handoff.md"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(wt_a), "commit", "-m", "abort"], check=True, capture_output=True)
    # Merge wt/shared's tip into main so the merged-condition alone is satisfied.
    subprocess.run(["git", "-C", str(repo), "merge", "--no-ff", "-m", "merge", "wt/shared"], check=True, capture_output=True)
    # Add a second worktree sharing the same branch (git allows this with --force).
    wt_b = repo / ".claude" / "worktrees" / "shared-b"
    subprocess.run(
        ["git", "-C", str(repo), "worktree", "add", "--force", str(wt_b), "wt/shared"],
        check=True, capture_output=True,
    )

    result = cleanup(wt_a)

    assert result.exit_code == 0
    assert result.action == "REMOVED"
    assert result.branch == "wt/shared"
    assert result.branch_action == "PRESERVED"
    assert "wt/shared" in _branches(repo)
