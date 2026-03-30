# New SDLC

This skill handles requests to build new features or make changes in a target repo. It supports two flows: the **fast path** for small, safe, well-covered changes, and the **normal flow** for everything else. For a fresh request, the lead agent must follow the shared phases and then the flow-specific phases in order. If a relevant `handoff.md` exists on session start, the lead agent may resume only from a recorded Next / Ongoing Step that clearly maps to one of the phases below or a substep within the current phase. If that handoff marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume it. Otherwise, if the recorded step does not clearly map to a phase or substep, the lead agent must ask the dev how to proceed instead of skipping required phases.

## Required Critic Availability

Any phase in this skill that requires critic agents is blocking. If the environment requires explicit user approval before spawning a required critic, the user declines, or the critic tool is otherwise unavailable, the lead agent must fully rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Blocked: awaiting user approval or tool availability to spawn the required critic agent(s) for <phase name>. Do not resume past this phase without that review.` Then stop, surface the blocker to the dev, and await direction. The lead agent must not skip the blocked review phase, continue execution, or proceed to Cleanup past it.

## Fast-Path Eligibility

A request qualifies for the fast path only when all three criteria are met:

1. **No invariant changes** — the mission does not propose new or modified invariants for `CLAUDE.md`. This includes modifications or deletions of existing test code (see CLAUDE.md). Adding new tests is not an invariant change.
2. **>80% test coverage around target code** — the code being changed is already covered by automated tests at >80% line coverage, providing a safety net for regressions.
3. **Clear scope, limited & safe change** — the change is well-defined, small in blast radius, and unlikely to introduce systemic risk.

If any criterion is not met, the request routes to the normal flow instead.

## Flow Routing

After the interview, the lead agent determines which flow applies:

- **Fast path:** All three eligibility criteria are met. Proceed to fast-path Phase: Single-Critic Review.
- **Normal flow:** Any eligibility criterion is not met. Proceed to normal-flow Phase: 2-Critic Mission Review.

---

# Shared Phases

## Phase: Interview

**Actor:** Lead agent.
**Inputs:** User's request.
**Outputs:** Enough context to draft a mission.md; flow determination (fast path or normal).

On session start, inspect `.claude/worktrees/` and the main project root of the target repo before any interview questions. If `handoff.md` or `mission.md` exists at the main project root, stop and ask the dev how to proceed before continuing. Otherwise, if exactly one worktree exists and it contains `handoff.md` at its root, load that `handoff.md` and use it to orient before proceeding. If multiple worktrees exist, or if exactly one worktree exists but it does not contain `handoff.md`, stop and ask the dev how to proceed before continuing. If no worktree exists and no legacy root runtime artifacts exist, create one before any interview or execution work begins. If the loaded `handoff.md` marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, do not resume that mission. Summarize the blockers from the old handoff to the user, and confirm that the current prompt should be treated as fresh work before discarding or replacing that handoff. Otherwise, if it reflects a mission whose `mission.md` has already been approved and the current prompt changes that mission's scope or intent, do not resume that mission. Keep the approved `mission.md` unchanged and follow `.agent/schemas/abort-protocol.md` using the scope or intent change as the blocker summary. After surfacing that abort to the user, confirm that the new prompt should be treated as fresh work before discarding or replacing the old handoff. If the agent will treat the current prompt as fresh work instead of resuming the loaded `handoff.md`, confirm with the dev before discarding or replacing that handoff. If the handoff is relevant, resume from its recorded Next / Ongoing Step per `.agent/schemas/handoff-protocol.md` only when that step clearly continues the same mission without reopening approved work.

If no relevant `handoff.md` exists at the worktree root, begin the interview. If a relevant `handoff.md` resumes Phase: Interview, continue from the recorded next question or step rather than restarting from scratch. Probe the user's request to clarify scope, intent, and any underlying considerations only as needed to complete the interview. Assess fast-path eligibility during the interview. The interview is complete when the lead agent has enough information to draft a mission.md and has determined which flow applies.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Generate mission.md

**Actor:** Lead agent.
**Inputs:** Interview findings, `.agent/schemas/mission-schema.md`.
**Outputs:** `mission.md` at the worktree root.

Draft a `mission.md` at the worktree root following `.agent/schemas/mission-schema.md`. The mission must be self-contained: a critic with access to only `CLAUDE.md`, `.agent/schemas/critic-protocol.md`, and `mission.md` must be able to evaluate it. If the request qualifies for the fast path, the mission must not contain an Invariants section (its presence would violate eligibility criterion 1).

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Fast-Path Flow

## Phase: Single-Critic Review

**Actor:** One critic agent.
**Inputs:** `CLAUDE.md` from the target repo, `.agent/schemas/critic-protocol.md`, `.agent/schemas/mission-schema.md`, `mission.md` from the worktree root, and any raw eligibility tool outputs explicitly relied on during interview, such as coverage report output.
**Outputs:** Response per `.agent/schemas/critic-protocol.md`.

Spawn one critic agent. The critic performs two checks in order. If the critic cannot be spawned, follow Required Critic Availability before taking any other action. The critic prompt must contain only those artifact references plus raw eligibility tool outputs, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If anything needs to be included before approval, put it in `mission.md` or another phase-allowed artifact first, then rerun review.

1. **Eligibility validation** — confirm all three fast-path criteria are met. If any criterion fails, the critic must REJECT with the reason "not eligible for fast path."
2. **Mission review** — evaluate the mission.md against the schema and acceptance criteria, exactly as in a normal review.

- If the critic approves: that exact `mission.md` becomes the approved mission for the rest of this fast-path run and must not be modified. Proceed to fast-path Phase: Execute in Worktree.
- If the critic rejects for fast-path ineligibility: route to normal flow. Proceed to normal-flow Phase: 2-Critic Mission Review with the current `mission.md`.
- If the critic rejects for other reasons: the lead agent fixes the issues and resubmits to a fresh critic. Repeat until approved, or escalate to the user if stuck.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Execute in Worktree (Fast Path)

**Actor:** Lead agent.
**Inputs:** Approved `mission.md`, target repo codebase.
**Outputs:** Implementation (code changes in worktree), passing unit tests.

Execute the approved mission in an isolated git worktree. The exact `mission.md` approved in Phase: Single-Critic Review is the execution contract for this phase and must remain unchanged. Produce only the deliverables specified in scope. If implementation reveals that the mission itself must change, follow `.agent/schemas/abort-protocol.md`. Run all unit tests related to the changed code before proceeding. If tests fail, fix the issues before moving to fast-path Phase: Post-Implementation Review.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Post-Implementation Review (Fast Path)

**Actor:** One fresh critic agent (not the Phase: Single-Critic Review critic).
**Inputs:** The diff (worktree changes), the exact `mission.md` approved in Phase: Single-Critic Review, `CLAUDE.md` from the target repo, `.agent/schemas/critic-protocol.md`, and any raw verification tool outputs explicitly relied on during execution, such as related test output or coverage output. The critic also has access to the full target repo codebase on demand.
**Outputs:** Response per `.agent/schemas/critic-protocol.md`.

Spawn a fresh critic agent. The critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the exact `mission.md` approved in Phase: Single-Critic Review, and does not violate any invariants in `CLAUDE.md`. The critic must follow `.agent/schemas/critic-protocol.md`. The critic prompt must contain only those artifact references plus raw tool outputs such as diff output, related test output, or coverage output, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If review would require information outside the approved mission and phase-allowed artifacts or raw tool outputs, do not brief the critic; follow `.agent/schemas/abort-protocol.md` or the applicable escalation flow instead. If the critic cannot be spawned, follow Required Critic Availability before taking any other action. If the diff modifies or deletes existing test code, the critic must REJECT — the change is not eligible for fast path.

- If the critic approves: proceed to Phase: Cleanup.
- If the critic rejects because the change is no longer eligible for fast path: escalate to normal flow per Escalation: Fast Path to Normal Flow.
- If the critic rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree, re-runs related unit tests, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh critic. Repeat until approved, or escalate to the user if stuck.
- If the critic rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Escalation: Fast Path to Normal Flow

When fast-path eligibility is lost during or after implementation (e.g., the post-implementation critic rejects for eligibility), the lead agent must evaluate whether the approved `mission.md` can be submitted intact to normal-flow review:

- **If `mission.md` can be submitted intact** (no fast-path-specific language that would need removal): The lead agent submits it to one additional critic for mission review, following the same critic-prompt constraints as normal-flow Phase: 2-Critic Mission Review. This brings the total mission-review approvals to two (one from the fast-path Single-Critic Review, one from this escalation review). If this critic approves, the mission remains the approved mission and the lead agent proceeds to normal-flow Phase: Dev Agent Execution, handing the dev subagent the approved `mission.md` and the unstaged work from the fast-path attempt. If this critic rejects, the lead agent fixes the issues and resubmits to a fresh critic. Repeat until approved, or escalate to the user if stuck.

- **If `mission.md` requires modification** (e.g., contains fast-path-specific language): The lead agent aborts per `.agent/schemas/abort-protocol.md`, keeping the approved `mission.md` unchanged. Then reinitialize `handoff.md` to Phase: Generate mission.md and start the normal flow from that phase — draft a new `mission.md`, submit it to full 2-Critic Mission Review, and proceed through normal-flow execution. Unstaged work from the fast-path attempt is preserved in the worktree for the dev agent.

If the escalation critic cannot be spawned, follow Required Critic Availability before taking any other action.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Normal Flow

## Phase: 2-Critic Mission Review

**Actor:** Two independent critic agents.
**Inputs:** `CLAUDE.md` from the target repo, `.agent/schemas/critic-protocol.md`, `.agent/schemas/mission-schema.md`, `mission.md` from the worktree root.
**Outputs:** Response per `.agent/schemas/critic-protocol.md` from each critic.

Spawn two independent critic agents for `mission.md` review. Each critic reads only `CLAUDE.md`, `.agent/schemas/critic-protocol.md`, `.agent/schemas/mission-schema.md`, and `mission.md`, and must follow `.agent/schemas/critic-protocol.md`. The critic prompt must contain only those artifact references, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If anything needs to be included before approval, put it in `mission.md` or another phase-allowed artifact first, then rerun review. If the critics cannot be spawned, follow Required Critic Availability before taking any other action.

- If both approve: that exact `mission.md` becomes the approved mission for the rest of this mission and must not be modified. Proceed to normal-flow Phase: Dev Agent Execution.
- If either rejects: the lead agent fixes the issues and resubmits to two fresh critic agents. Repeat until both approve, or escalate to the user if stuck.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Dev Agent Execution

**Actor:** Dev subagent (spawned by the lead agent via the Agent tool).
**Inputs:** Approved `mission.md`, target repo codebase (in worktree). If escalated from fast path, any unstaged work from the fast-path attempt is present in the worktree.
**Outputs:** Implementation (code changes in worktree), passing full regression suite, clean formatter/linter results.

The lead agent spawns a dev subagent and hands it the approved `mission.md`. The dev agent executes the approved mission in the worktree. The exact `mission.md` approved in the preceding review phase is the execution contract and must remain unchanged. The dev agent must produce only the deliverables specified in scope. If implementation reveals that the mission itself must change, the dev agent must stop and report the blocker to the lead agent, who then follows `.agent/schemas/abort-protocol.md`.

Before the dev agent reports completion, it must:

1. **Run the full regression suite** — all tests in the target repo, not just tests related to the changed code. All tests must pass. If tests fail, the dev agent must fix the issues and re-run the full suite until all tests pass.
2. **Check for coverage regressions** — if the target repo provides a coverage tool, the dev agent must run it and verify there are no coverage regressions compared to the baseline (pre-change coverage). If coverage has regressed, the dev agent must fix the regression before proceeding.
3. **Apply formatter and/or linter** — if the target repo provides a formatter and/or linter, the dev agent must run them and ensure all results are clean. If there are violations, the dev agent must fix them before proceeding.

Only after all three checks pass does the dev agent report completion to the lead agent.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: 2-Critic Post-Implementation Review

**Actor:** Two fresh critic agents (not any previously used critics in this mission).
**Inputs:** The diff (worktree changes), the exact approved `mission.md`, `CLAUDE.md` from the target repo, `.agent/schemas/critic-protocol.md`, and any raw verification tool outputs explicitly relied on for acceptance checks (such as full test suite output, coverage output, or linter output). Each critic also has access to the full target repo codebase on demand.
**Outputs:** Response per `.agent/schemas/critic-protocol.md` from each critic.

Spawn two fresh critic agents. Each critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the approved `mission.md`, and does not violate any invariants in `CLAUDE.md`. Each critic must follow `.agent/schemas/critic-protocol.md`. The critic prompt must contain only those artifact references plus raw tool outputs, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If review would require information outside the approved mission and phase-allowed artifacts or raw tool outputs, do not brief the critics; follow `.agent/schemas/abort-protocol.md` instead. If the critics cannot be spawned, follow Required Critic Availability before taking any other action.

- If both approve: proceed to Phase: Cleanup.
- If either rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree (or instructs the dev subagent to fix them), re-runs the full regression suite, re-verifies all acceptance criteria, and resubmits the updated diff to two fresh critics. Repeat until both approve, or escalate to the user if stuck.
- If either rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Phase: Cleanup

Before deleting any files, rewrite `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Phase: Cleanup - ensure mission.md is absent, then delete handoff.md last, then immediately present results to the user in the same turn.` Then remove `mission.md` if it still exists and `handoff.md` last from the worktree root. If cleanup is interrupted or any deletion fails before `handoff.md` is removed, leave that latest `handoff.md` state in place so the next session can resume cleanup deterministically. After both runtime artifacts are removed, remove the worktree via `git worktree remove --force`. If worktree removal fails, leave the worktree in place and report the failure to the user. Cleanup completion is the end of the mission lifecycle. Immediately after cleanup succeeds, present results to the user.
