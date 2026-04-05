from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text()


def test_new_sdlc_prefers_fast_path_attempts_with_explicit_assumptions():
    text = _read(".claude/commands/new-sdlc.md")

    assert "Mission Creation should make a good-faith attempt to keep a request on fast path" in text
    assert "These assumptions are provisional" in text
    assert "no eligibility criterion is already known to fail" in text


def test_mission_schema_allows_later_validation_of_fast_path_assumptions():
    text = _read(".agent/schemas/mission-schema.md")

    assert "Assumptions may provisionally carry plausible fast-path claims forward" in text
    assert "Assumptions must not hide already-known fast-path disqualifiers." in text


def test_mission_schema_requires_persisted_governed_artifacts():
    text = _read(".agent/schemas/mission-schema.md")

    assert "Each non-persistence AC maps to one or more in-scope items." in text
    assert "Each persistence AC maps to the governed artifact it persists." in text
    assert (
        "Every governed artifact captured in `Invariants`, `External Constraints`, `Beliefs`, or `Considerations` "
        "must have at least one acceptance criterion that requires the artifact to be persisted."
    ) in text
    assert (
        "When a governed artifact is not persisted as automated tests, its persistence acceptance criterion must "
        "require the same text in the governed file and matching top-level governance section where the artifact will "
        "live after the mission completes."
    ) in text
    assert "For hard constraints, prefer automated tests when the constraint can naturally be enforced there." in text


def test_tdd_protocol_requires_execution_to_validate_coverage_assumption():
    text = _read(".agent/schemas/tdd-protocol.md")

    assert "Mission Creation may carry forward a plausible assumption" in text
    assert "execution step 1 must confirm it" in text


def test_tdd_protocol_uses_baseline_only_for_threshold_gating():
    text = _read(".agent/schemas/tdd-protocol.md")

    assert "The coverage threshold is **>80% line coverage on the code being touched by the mission**." in text
    assert "This baseline is used in step 3" in text
    assert "Verify the touched code still meets the coverage threshold (>80% line coverage)." in text
    assert "Verify no coverage regression compared to the baseline recorded in step 2." not in text


def test_new_sdlc_execution_mentions_threshold_check_not_regression_gate():
    text = _read(".claude/commands/new-sdlc.md")

    assert "touched code remains above the >80% coverage threshold" in text
    assert "final verification (full suite + coverage threshold check)" in text
    assert "final verification (full suite + coverage threshold check + formatter/linter)" in text
    assert "coverage regression check" not in text
    assert "no coverage regression" not in text


# ---------------------------------------------------------------------------
# AC1 — AGENTS.md Bootstrap reclassified to # Invariants
# ---------------------------------------------------------------------------

def test_agents_md_bootstrap_under_invariants():
    text = _read("AGENTS.md")
    # Bootstrap must be under # Invariants (the section must begin with "# Invariants")
    assert text.strip().startswith("# Invariants")
    assert "## Bootstrap" in text
    assert "Unless you are a sub-agent, follow `.claude/commands/new-sdlc.md` in response to any prompt." in text


def test_agents_md_no_considerations_section():
    text = _read("AGENTS.md")
    assert "# Considerations" not in text


# ---------------------------------------------------------------------------
# AC2 — CLAUDE.md reclassification
# ---------------------------------------------------------------------------

def test_claude_md_invariants_include_completion_review_artifacts():
    text = _read("CLAUDE.md")
    # All these must be present as ## headings under # Invariants
    for heading in [
        "## Critic Spawning Blockers",
        "## Abort Protocol",
        "## Completion-Review Merge Base",
        "## Completion-Review Merge Requirement",
        "## Trivial Merge Qualification",
        "## Non-Trivial Merge Phase Reset",
        "## Non-Trivial Merge Submission Gate",
        "## Completion-Review Runtime Inputs",
        "## Cleanup Merge Reset",
        "## Post-Approval Merge-Back Gate",
        "## Template Files",
        "## Codex Sub-Agent Boundary",
    ]:
        assert heading in text, f"Missing heading: {heading}"


def test_claude_md_considerations_only_has_codex_boundary_rationale():
    text = _read("CLAUDE.md")
    # Considerations section must exist with Codex Sub-Agent Boundary Rationale
    assert "# Considerations" in text
    assert "## Codex Sub-Agent Boundary Rationale" in text
    # Old Considerations entries must be gone
    assert "## Completion-Review Detailed Workflow" not in text


def test_claude_md_trivial_merge_qualification_exact_text():
    text = _read("CLAUDE.md")
    assert (
        "A completion-review or cleanup merge counts as trivial only when Git reports "
        "`Already up to date.` or performs a clean fast-forward with no manual conflict resolution."
    ) in text


def test_claude_md_no_old_considerations_entries():
    text = _read("CLAUDE.md")
    # The old Considerations copies must be gone
    # Check that these items are NOT appearing in Considerations (they should be in Invariants)
    # We verify by checking the file doesn't have the old prose form in Considerations
    assert "Completion-Review Detailed Workflow" not in text


# ---------------------------------------------------------------------------
# AC3 — new-sdlc.md section reclassification
# ---------------------------------------------------------------------------

def test_new_sdlc_invariants_has_flow_order():
    text = _read(".claude/commands/new-sdlc.md")
    assert "## Flow Order" in text
    assert "For a fresh request, the lead agent must follow the shared phases and then the applicable flow-specific phases in order." in text


def test_new_sdlc_invariants_has_target_repo_governance_precedence():
    text = _read(".claude/commands/new-sdlc.md")
    assert "## Target Repo Governance Precedence" in text
    assert (
        "When operating inside a target repo, that repo's `CLAUDE.md` invariants, beliefs, and considerations govern "
        "ahead of this harness's generic defaults."
    ) in text


def test_new_sdlc_invariants_has_handoff_resumption():
    text = _read(".claude/commands/new-sdlc.md")
    assert "## Handoff Resumption" in text
    assert (
        "If a relevant `handoff.md` exists on session start, the lead agent may resume only from a recorded "
        "Next / Ongoing Step that clearly maps to one of the phases below or a substep within the current phase."
    ) in text


def test_new_sdlc_beliefs_has_fast_path_preference():
    text = _read(".claude/commands/new-sdlc.md")
    assert "# Beliefs" in text
    assert "## Fast-Path Preference" in text
    assert "Mission Creation should make a good-faith attempt to keep a request on fast path" in text


def test_new_sdlc_no_old_monolithic_opening_paragraph():
    text = _read(".claude/commands/new-sdlc.md")
    # The old monolithic paragraph started with "This skill handles requests..."
    # It should no longer appear directly under # Invariants as a paragraph
    assert "This skill handles requests to build new features" not in text


# ---------------------------------------------------------------------------
# AC4 — critic-protocol.md reclassification
# ---------------------------------------------------------------------------

def test_critic_protocol_no_overview_section():
    text = _read(".agent/schemas/critic-protocol.md")
    assert "## Overview" not in text


def test_critic_protocol_prompt_construction_under_invariants():
    text = _read(".agent/schemas/critic-protocol.md")
    assert "## Prompt Construction" in text
    # The key text from the Prompt Construction invariant
    assert "A critic prompt must follow the applicable template exactly" in text
    assert "`.agent/schemas/governance-schema.md` must appear first among the governance artifacts in every critic prompt." in text


def test_critic_protocol_no_duplicate_prompt_construction_in_input_discipline():
    text = _read(".agent/schemas/critic-protocol.md")
    # The "## Input Discipline" section should no longer contain the rule that was
    # extracted into Prompt Construction. Specifically, item 1 from Input Discipline
    # that duplicates the Prompt Construction invariant should be gone.
    # Verify the section still exists but the duplication is gone:
    assert "## Input Discipline" in text
    # The prompt-construction rule should only appear once (under ## Prompt Construction)
    count = text.count("A critic prompt must follow the applicable template exactly")
    assert count == 1, f"Prompt construction rule appears {count} times; expected 1"


# ---------------------------------------------------------------------------
# AC5 — handoff-protocol.md reclassification
# ---------------------------------------------------------------------------

def test_handoff_protocol_no_overview_section():
    text = _read(".agent/schemas/handoff-protocol.md")
    assert "## Overview" not in text


def test_handoff_protocol_location_under_invariants():
    text = _read(".agent/schemas/handoff-protocol.md")
    assert "## Location" in text
    assert "The canonical location of `handoff.md` is the worktree root." in text


# ---------------------------------------------------------------------------
# AC6 — mission-schema.md reclassification
# ---------------------------------------------------------------------------

def test_mission_schema_no_overview_section():
    text = _read(".agent/schemas/mission-schema.md")
    assert "## Overview" not in text


def test_mission_schema_self_containment_under_invariants():
    text = _read(".agent/schemas/mission-schema.md")
    assert "## Self-Containment" in text
    assert (
        "Every `mission.md` must be self-contained: a critic sub-agent with access to only the harness "
        "repo-root `.agent/schemas/governance-schema.md`"
    ) in text


def test_mission_schema_section_ordering_under_invariants():
    text = _read(".agent/schemas/mission-schema.md")
    assert "## Section Ordering" in text
    assert (
        "When present, sections appear in this order: Invariants, External Constraints, Beliefs, "
        "Considerations, Scope, Assumptions, Acceptance Criteria."
    ) in text


def test_mission_schema_self_containment_not_in_considerations():
    text = _read(".agent/schemas/mission-schema.md")
    # These items should not appear as ## headings under # Considerations
    # The old Considerations had "## Overview" and "## Section Ordering" - those must be gone
    # Ensure no second copy of Section Ordering in Considerations
    lines = text.splitlines()
    in_considerations = False
    for line in lines:
        if line.strip() == "# Considerations":
            in_considerations = True
        elif line.startswith("# ") and line.strip() != "# Considerations":
            in_considerations = False
        if in_considerations and line.strip() == "## Self-Containment":
            raise AssertionError("Self-Containment found in # Considerations; should only be in # Invariants")
        if in_considerations and line.strip() == "## Section Ordering":
            raise AssertionError("Section Ordering found in # Considerations; should only be in # Invariants")


# ---------------------------------------------------------------------------
# AC7 — tdd-protocol.md reclassification
# ---------------------------------------------------------------------------

def test_tdd_protocol_no_overview_section():
    text = _read(".agent/schemas/tdd-protocol.md")
    assert "## Overview" not in text


def test_tdd_protocol_fast_path_assumption_validation_under_invariants():
    text = _read(".agent/schemas/tdd-protocol.md")
    assert "## Fast-Path Assumption Validation" in text
    assert (
        "Fast-path assumptions recorded during Mission Creation stay provisional until this protocol's "
        "execution checks validate them."
    ) in text


# ---------------------------------------------------------------------------
# AC8 — abort-protocol.md no standalone overview sentence
# ---------------------------------------------------------------------------

def test_abort_protocol_no_standalone_overview_sentence():
    text = _read(".agent/schemas/abort-protocol.md")
    # The old overview sentence was:
    # "This document defines the required behavior when a mission or fast-path run must stop..."
    assert "This document defines the required behavior when a mission or fast-path run must stop" not in text


# ---------------------------------------------------------------------------
# AC9 — new-sdlc.md replacement merge-classification paragraphs; no CLAUDE.md Invariant 4
# ---------------------------------------------------------------------------

def test_new_sdlc_no_invariant_4_reference():
    text = _read(".claude/commands/new-sdlc.md")
    assert "CLAUDE.md Invariant 4" not in text


def test_new_sdlc_references_trivial_merge_qualification():
    text = _read(".claude/commands/new-sdlc.md")
    assert "CLAUDE.md` `Trivial Merge Qualification`" in text


def test_new_sdlc_fast_path_merge_paragraph():
    text = _read(".claude/commands/new-sdlc.md")
    expected = (
        "Before writing heavy verification outputs or spawning the critic, the lead agent must merge "
        "the latest applicable target-repo root branch state into the current worktree and reconcile "
        "the implementation against that merged state. The applicable branch is the integration branch "
        "named by the target repo's governing artifacts; if those artifacts name none, it is the branch "
        "from which the worktree was created. If Git reports `Already up to date.` or performs a clean "
        "fast-forward, continue this phase on the merged state. Otherwise the merge is non-trivial per "
        "the harness repo-root `CLAUDE.md` `Trivial Merge Qualification` invariant: re-run the related "
        "unit tests and re-verify all acceptance criteria against the merged state, rewrite `handoff.md` "
        "with Next / Ongoing Step set to `Phase: Post-Implementation Review (Fast Path) - rerun "
        "verification on the merged state, rewrite completion-review runtime artifacts, and submit that "
        "state to a fresh critic.`, and restart this phase from its beginning with a fresh critic."
    )
    assert expected in text


def test_new_sdlc_normal_flow_merge_paragraph():
    text = _read(".claude/commands/new-sdlc.md")
    expected = (
        "Before writing heavy verification outputs or spawning the critics, the lead agent must merge "
        "the latest applicable target-repo root branch state into the current worktree and reconcile "
        "the implementation against that merged state. The applicable branch is the integration branch "
        "named by the target repo's governing artifacts; if those artifacts name none, it is the branch "
        "from which the worktree was created. If Git reports `Already up to date.` or performs a clean "
        "fast-forward, continue this phase on the merged state. Otherwise the merge is non-trivial per "
        "the harness repo-root `CLAUDE.md` `Trivial Merge Qualification` invariant: re-run the full "
        "regression suite, re-verify all acceptance criteria against the merged state, rewrite "
        "`handoff.md` with Next / Ongoing Step set to `Phase: 2-Critic Post-Implementation Review - "
        "rerun verification on the merged state, rewrite completion-review runtime artifacts, submit "
        "that state to the first fresh critic, and if it approves then to a second fresh critic.`, and "
        "restart this phase from its beginning with two fresh critics."
    )
    assert expected in text


def test_new_sdlc_cleanup_merge_sentence():
    text = _read(".claude/commands/new-sdlc.md")
    expected = (
        "Cleanup follows the target repo's commit/merge rules. If the target repo's governing artifacts "
        "require or permit merging the approved worktree branch before worktree removal, apply those "
        "rules. If the target repo defines no merge rule, default to commit-only and do not auto-merge. "
        "Any cleanup-phase merge attempted before worktree removal that is non-trivial per the harness "
        "repo-root `CLAUDE.md` `Trivial Merge Qualification` invariant must reset the mission to the "
        "applicable completion-review phase: do not continue Cleanup, rewrite `handoff.md` so Next / "
        "Ongoing Step names the applicable completion-review phase for the merged state, and resume from "
        "that review phase with fresh critic approval before any further cleanup. If a required or "
        "permitted cleanup merge fails for any other reason, leave the worktree in place and report the "
        "failure to the user."
    )
    assert expected in text


# ---------------------------------------------------------------------------
# AC10 — template updates: role-specific-input boundary and no-bootstrap rule
# ---------------------------------------------------------------------------

def test_template_critic_prompts_have_role_specific_input_statement():
    text = _read(".agent/templates/new-sdlc-subagents.prompt.template")
    assert "Operate only on the role-specific inputs granted by the invoking phase." in text


def test_template_critic_prompts_have_no_bootstrap_statement():
    text = _read(".agent/templates/new-sdlc-subagents.prompt.template")
    assert "Do not perform session-start bootstrap discovery unless the invoking phase explicitly requires it." in text


def test_template_mission_creation_lite_review_critic():
    text = _read(".agent/templates/new-sdlc-subagents.prompt.template")
    expected = (
        "You are a critic sub-agent.\n"
        "Operate only on the role-specific inputs granted by the invoking phase.\n"
        "Do not perform session-start bootstrap discovery unless the invoking phase explicitly requires it.\n"
        "\n"
        "Review the mission. Governing documents:\n"
        "- `{{GOVERNANCE_SCHEMA_PATH}}`\n"
        "- `{{CRITIC_PROTOCOL_PATH}}`\n"
        "- `{{MISSION_SCHEMA_PATH}}`\n"
        "\n"
        "The mission: `{{MISSION_PATH}}`\n"
        "Worktree path: `{{WORKTREE_PATH}}`\n"
        "\n"
        "{{RAW_ELIGIBILITY_OUTPUTS_BLOCK}}"
    )
    assert expected in text


def test_template_fast_path_post_implementation_critic():
    text = _read(".agent/templates/new-sdlc-subagents.prompt.template")
    expected = (
        "You are a critic sub-agent.\n"
        "Operate only on the role-specific inputs granted by the invoking phase.\n"
        "Do not perform session-start bootstrap discovery unless the invoking phase explicitly requires it.\n"
        "\n"
        "Review the implementation. Governing documents:\n"
        "- `{{GOVERNANCE_SCHEMA_PATH}}`\n"
        "- `{{CRITIC_PROTOCOL_PATH}}`\n"
        "- `{{MISSION_PATH}}`\n"
        "\n"
        "Worktree path: `{{WORKTREE_PATH}}`"
    )
    assert expected in text
