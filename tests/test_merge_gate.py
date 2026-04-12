"""Tests for scripts/merge_gate — AC1–AC13."""

import subprocess
from pathlib import Path

import pytest

from scripts.merge_gate import (
    VARIANTS,
    check_dirty,
    classify_merge_output,
    do_merge,
    main,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_git_repo(path: Path) -> Path:
    """Initialise a minimal git repo with one commit at *path*."""
    subprocess.run(["git", "init", str(path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=path, check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=path, check=True, capture_output=True,
    )
    (path / "a.txt").write_text("initial\n")
    subprocess.run(["git", "add", "."], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "initial"],
        cwd=path, check=True, capture_output=True,
    )
    return path


def _commit(path: Path, filename: str, content: str, message: str) -> None:
    (path / filename).write_text(content)
    subprocess.run(["git", "add", filename], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=path, check=True, capture_output=True,
    )


def _current_branch(path: Path) -> str:
    r = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=path, capture_output=True, text=True, check=True,
    )
    return r.stdout.strip()


# ---------------------------------------------------------------------------
# AC7 — phase-reset texts remain stable
# ---------------------------------------------------------------------------

def test_variant_new_sdlc_fast_path():
    assert VARIANTS["new-sdlc-fast-path"] == (
        "Phase: Post-Implementation Review (Fast Path) - rerun verification on the merged state, "
        "rewrite completion-review runtime artifacts, and submit that state to a fresh critic."
    )


def test_variant_new_sdlc_normal():
    assert VARIANTS["new-sdlc-normal"] == (
        "Phase: 2-Critic Post-Implementation Review - rerun verification on the merged state, "
        "rewrite completion-review runtime artifacts, submit that state to the first fresh critic, "
        "and if it approves then to a second fresh critic."
    )


# ---------------------------------------------------------------------------
# classify_merge_output unit tests
# ---------------------------------------------------------------------------

def test_classify_already_up_to_date():
    assert classify_merge_output("Already up to date.\n", 0) == "TRIVIAL"


def test_classify_already_up_to_date_nonzero():
    # Even if returncode is somehow non-zero, the sentinel string wins
    assert classify_merge_output("Already up to date.\n", 1) == "TRIVIAL"


def test_classify_fast_forward():
    output = "Updating abc1234..def5678\nFast-forward\n a.txt | 1 +\n"
    assert classify_merge_output(output, 0) == "TRIVIAL"


def test_classify_fast_forward_with_conflict_markers_is_non_trivial():
    # Fast-forward text present but also CONFLICT → non-trivial
    output = "Fast-forward\nCONFLICT (content): Merge conflict in a.txt\n"
    assert classify_merge_output(output, 1) == "NON_TRIVIAL"


def test_classify_merge_commit():
    output = "Merge made by the 'ort' strategy.\n a.txt | 1 +\n"
    assert classify_merge_output(output, 0) == "NON_TRIVIAL"


def test_classify_conflict():
    output = "Auto-merging a.txt\nCONFLICT (content): Merge conflict in a.txt\n"
    assert classify_merge_output(output, 1) == "NON_TRIVIAL"


def test_classify_merge_error():
    output = "fatal: 'nonexistent' does not point at a commit\n"
    assert classify_merge_output(output, 128) == "MERGE_ERROR"


# ---------------------------------------------------------------------------
# AC1 — check-dirty clean
# ---------------------------------------------------------------------------

def test_check_dirty_clean(tmp_path):
    repo = _make_git_repo(tmp_path)
    status, paths = check_dirty(repo)
    assert status == "CLEAN"
    assert paths == []


# ---------------------------------------------------------------------------
# AC2 — check-dirty dirty variants
# ---------------------------------------------------------------------------

def test_check_dirty_unstaged_modification(tmp_path):
    repo = _make_git_repo(tmp_path)
    (repo / "a.txt").write_text("modified\n")
    status, paths = check_dirty(repo)
    assert status == "DIRTY"
    assert any("a.txt" in p for p in paths)


def test_check_dirty_staged_uncommitted(tmp_path):
    repo = _make_git_repo(tmp_path)
    (repo / "new.txt").write_text("staged\n")
    subprocess.run(["git", "add", "new.txt"], cwd=repo, check=True, capture_output=True)
    status, paths = check_dirty(repo)
    assert status == "DIRTY"
    assert any("new.txt" in p for p in paths)


def test_check_dirty_untracked(tmp_path):
    repo = _make_git_repo(tmp_path)
    (repo / "untracked.txt").write_text("untracked\n")
    status, paths = check_dirty(repo)
    assert status == "DIRTY"
    assert any("untracked.txt" in p for p in paths)


def test_check_dirty_returns_multiple_paths(tmp_path):
    repo = _make_git_repo(tmp_path)
    (repo / "a.txt").write_text("changed\n")
    (repo / "untracked.txt").write_text("new\n")
    status, paths = check_dirty(repo)
    assert status == "DIRTY"
    assert len(paths) >= 2


# ---------------------------------------------------------------------------
# AC3 — do-merge already-up-to-date
# ---------------------------------------------------------------------------

def test_do_merge_already_up_to_date(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    handoff_file = handoff_dir / "handoff.md"
    handoff_file.write_text("original")

    branch = _current_branch(repo)
    # Merge the same branch into itself → already up to date
    message, code = do_merge(repo, handoff_dir, "new-sdlc-normal", branch)
    assert message == "TRIVIAL"
    assert code == 0
    assert handoff_file.read_text() == "original"


# ---------------------------------------------------------------------------
# AC4 — do-merge clean fast-forward
# ---------------------------------------------------------------------------

def test_do_merge_fast_forward(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    handoff_file = handoff_dir / "handoff.md"
    handoff_file.write_text("original")

    # Create a feature branch with a new commit
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo, check=True, capture_output=True)
    _commit(repo, "b.txt", "new\n", "add b")

    # Back to main (or initial branch); feature is ahead
    main_branch = subprocess.run(
        ["git", "branch", "--list", "main", "master"],
        cwd=repo, capture_output=True, text=True,
    ).stdout.strip().lstrip("* ").strip()
    # Use symbolic ref to get original branch
    orig = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "checkout", orig if orig != "feature" else "HEAD~1"],
        cwd=repo, check=True, capture_output=True,
    )
    # Reset: checkout the pre-feature state
    subprocess.run(["git", "checkout", "-"], cwd=repo, check=True, capture_output=True)
    # We're back to main/initial; merge feature → fast-forward
    message, code = do_merge(repo, handoff_dir, "new-sdlc-normal", "feature")
    assert message == "TRIVIAL"
    assert code == 0
    assert handoff_file.read_text() == "original"


# ---------------------------------------------------------------------------
# AC5 — do-merge non-trivial merge commit (no conflict)
# ---------------------------------------------------------------------------

def test_do_merge_non_trivial_merge_commit(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    handoff_file = handoff_dir / "handoff.md"
    handoff_file.write_text("old handoff content")

    main_branch = _current_branch(repo)

    # Create feature branch with a unique commit
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo, check=True, capture_output=True)
    _commit(repo, "feature.txt", "feature work\n", "feature commit")

    # Back to main, add a diverging commit on a different file
    subprocess.run(["git", "checkout", main_branch], cwd=repo, check=True, capture_output=True)
    _commit(repo, "main_extra.txt", "main work\n", "main commit")

    # Merge feature into main → non-trivial merge commit (no conflict)
    message, code = do_merge(repo, handoff_dir, "new-sdlc-normal", "feature")
    assert message == "NON_TRIVIAL"
    assert code == 2


# ---------------------------------------------------------------------------
# AC6 — do-merge conflict
# ---------------------------------------------------------------------------

def test_do_merge_conflict(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    handoff_file = handoff_dir / "handoff.md"
    handoff_file.write_text("old handoff content")

    main_branch = _current_branch(repo)

    # Feature: modify a.txt
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo, check=True, capture_output=True)
    _commit(repo, "a.txt", "feature version\n", "feature modifies a")

    # Main: also modify a.txt differently
    subprocess.run(["git", "checkout", main_branch], cwd=repo, check=True, capture_output=True)
    _commit(repo, "a.txt", "main version\n", "main modifies a")

    # Merge feature → CONFLICT
    message, code = do_merge(repo, handoff_dir, "new-sdlc-normal", "feature")
    assert message == "NON_TRIVIAL"
    assert code == 2

    # Abort the conflicted merge so the repo is not left in a broken state
    subprocess.run(["git", "-C", str(repo), "merge", "--abort"], capture_output=True)


# ---------------------------------------------------------------------------
# AC8 — handoff.md rewrite format
# ---------------------------------------------------------------------------

def test_handoff_rewrite_format_all_variants(tmp_path):
    """For each variant, confirm the rewritten handoff.md has correct format."""
    repo = _make_git_repo(tmp_path)
    main_branch = _current_branch(repo)

    for i, variant in enumerate(VARIANTS):
        # Fresh handoff dir per variant
        handoff_dir = tmp_path / f"handoff_{i}"
        handoff_dir.mkdir()
        handoff_file = handoff_dir / "handoff.md"
        handoff_file.write_text("old content")

        # Build a fresh diverging-merge repo state in a sub-path
        sub = tmp_path / f"repo_{i}"
        sub.mkdir()
        sub_repo = _make_git_repo(sub)
        sub_main = _current_branch(sub_repo)

        subprocess.run(["git", "checkout", "-b", "feat"], cwd=sub_repo, check=True, capture_output=True)
        _commit(sub_repo, f"feat_{i}.txt", "feat\n", "feat")
        subprocess.run(["git", "checkout", sub_main], cwd=sub_repo, check=True, capture_output=True)
        _commit(sub_repo, f"main_{i}.txt", "main\n", "main")

        do_merge(sub_repo, handoff_dir, variant, "feat")

        content = handoff_file.read_text()
        expected = (
            "## Next / Ongoing Step\n\n"
            + VARIANTS[variant]
            + "\n\n## Known Failed Attempts\n\nNone\n"
        )
        assert content == expected, f"Variant {variant!r}: handoff content mismatch"
        assert "Dev Interview Transcript" not in content


# ---------------------------------------------------------------------------
# AC9 — HANDOFF_MISSING
# ---------------------------------------------------------------------------

def test_do_merge_handoff_missing_on_non_trivial(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    # handoff.md deliberately absent

    main_branch = _current_branch(repo)
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=repo, check=True, capture_output=True)
    _commit(repo, "feature.txt", "feat\n", "feat")
    subprocess.run(["git", "checkout", main_branch], cwd=repo, check=True, capture_output=True)
    _commit(repo, "main_extra.txt", "main\n", "main diverge")

    message, code = do_merge(repo, handoff_dir, "new-sdlc-normal", "feature")
    assert message == "HANDOFF_MISSING"
    assert code == 4
    assert not (handoff_dir / "handoff.md").exists()


# ---------------------------------------------------------------------------
# AC10 — MERGE_ERROR
# ---------------------------------------------------------------------------

def test_do_merge_error_nonexistent_branch(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    handoff_file = handoff_dir / "handoff.md"
    handoff_file.write_text("original")

    message, code = do_merge(repo, handoff_dir, "new-sdlc-normal", "nonexistent-branch-xyz")
    assert message.startswith("MERGE_ERROR")
    assert code == 3
    assert handoff_file.read_text() == "original"


# ---------------------------------------------------------------------------
# AC11 — unknown variant
# ---------------------------------------------------------------------------

def test_do_merge_unknown_variant(tmp_path):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()

    message, code = do_merge(repo, handoff_dir, "unknown-variant-xyz", "somebranch")
    assert "INVALID_VARIANT" in message
    assert code not in (2, 3, 4)
    assert code != 0


# ---------------------------------------------------------------------------
# main() direct tests (covers CLI dispatch paths for AC12 coverage)
# ---------------------------------------------------------------------------

def test_main_no_args(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["merge_gate"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_main_unknown_subcommand(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["merge_gate", "bogus"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_main_check_dirty_clean(tmp_path, monkeypatch, capsys):
    repo = _make_git_repo(tmp_path)
    monkeypatch.setattr("sys.argv", ["merge_gate", "check-dirty", str(repo)])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
    assert "CLEAN" in capsys.readouterr().out


def test_main_check_dirty_dirty(tmp_path, monkeypatch, capsys):
    repo = _make_git_repo(tmp_path)
    (repo / "untracked.txt").write_text("new\n")
    monkeypatch.setattr("sys.argv", ["merge_gate", "check-dirty", str(repo)])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1
    assert "DIRTY" in capsys.readouterr().out


def test_main_check_dirty_wrong_arg_count(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["merge_gate", "check-dirty"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_main_do_merge_trivial(tmp_path, monkeypatch, capsys):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    (handoff_dir / "handoff.md").write_text("original")
    branch = _current_branch(repo)

    monkeypatch.setattr(
        "sys.argv",
        ["merge_gate", "do-merge", str(repo), str(handoff_dir), "new-sdlc-normal", branch],
    )
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
    assert "TRIVIAL" in capsys.readouterr().out


def test_main_do_merge_wrong_arg_count(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["merge_gate", "do-merge", "only-one-arg"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_main_do_merge_non_trivial(tmp_path, monkeypatch, capsys):
    repo = _make_git_repo(tmp_path)
    handoff_dir = tmp_path / "handoff"
    handoff_dir.mkdir()
    (handoff_dir / "handoff.md").write_text("old")

    main_branch = _current_branch(repo)
    subprocess.run(["git", "checkout", "-b", "feat2"], cwd=repo, check=True, capture_output=True)
    _commit(repo, "feat2.txt", "feat\n", "feat")
    subprocess.run(["git", "checkout", main_branch], cwd=repo, check=True, capture_output=True)
    _commit(repo, "main2.txt", "main\n", "main diverge")

    monkeypatch.setattr(
        "sys.argv",
        ["merge_gate", "do-merge", str(repo), str(handoff_dir), "new-sdlc-normal", "feat2"],
    )
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2
    assert "NON_TRIVIAL" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# AC9 — merge_gate no longer references CLAUDE.md Invariant 4
# ---------------------------------------------------------------------------

def test_merge_gate_no_invariant_4_reference():
    """scripts/merge_gate/__init__.py must not reference CLAUDE.md Invariant 4."""
    repo_root = Path(__file__).resolve().parents[1]
    source = (repo_root / "scripts" / "merge_gate" / "__init__.py").read_text()
    assert "CLAUDE.md Invariant 4" not in source
    assert "Invariant 4" not in source


def test_merge_gate_references_trivial_merge_qualification():
    """scripts/merge_gate/__init__.py must reference CLAUDE.md Trivial Merge Qualification."""
    repo_root = Path(__file__).resolve().parents[1]
    source = (repo_root / "scripts" / "merge_gate" / "__init__.py").read_text()
    assert "Trivial Merge Qualification" in source


# ---------------------------------------------------------------------------
# AC9 — phase-reset texts stay usable as handoff next-step content
# ---------------------------------------------------------------------------

def test_variant_texts_are_single_paragraph_handoff_steps():
    for reset_text in VARIANTS.values():
        assert reset_text.startswith("Phase: ")
        assert "\n" not in reset_text
        assert reset_text.endswith(".")
