# New SDLC

This skill handles requests to build new features or make changes in a target repo using the fast-path SDLC. For a fresh request, the lead agent must follow these phases in order. If a relevant `handoff.md` exists on session start, the lead agent may resume only from a recorded Next / Ongoing Step that clearly maps to one of the phases below or a substep within the current phase. If that handoff marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume it. Otherwise, if the recorded step does not clearly map to a phase or substep, the lead agent must ask the dev how to proceed instead of skipping required phases.

## Fast-Path Eligibility

A request qualifies for the fast path only when all three criteria are met:

1. **No invariant changes** — the mission does not propose new or modified invariants for `CLAUDE.md`. This includes modifications or deletions of existing test code (see CLAUDE.md). Adding new tests is not an invariant change.
2. **>80% test coverage around target code** — the code being changed is already covered by automated tests at >80% line coverage, providing a safety net for regressions.
3. **Clear scope, limited & safe change** — the change is well-defined, small in blast radius, and unlikely to introduce systemic risk.

If any criterion is not met, the lead agent must not proceed. Inform the user that the request does not qualify for the fast path and halt.

## Phase: Interview

**Actor:** Lead agent.
**Inputs:** User's request.
**Outputs:** Enough context to draft a mission.md.

On session start, inspect `.claude/worktrees/` and the main project root of the target repo before any interview questions. If `handoff.md` or `mission.md` exists at the main project root, stop and ask the dev how to proceed before continuing. Otherwise, if exactly one worktree exists and it contains `handoff.md` at its root, load that `handoff.md` and use it to orient before proceeding. If multiple worktrees exist, or if exactly one worktree exists but it does not contain `handoff.md`, stop and ask the dev how to proceed before continuing. If no worktree exists and no legacy root runtime artifacts exist, create one before any interview or execution work begins. If the loaded `handoff.md` marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, do not resume that mission. Summarize the blockers from the old handoff to the user, and confirm that the current prompt should be treated as fresh work before discarding or replacing that handoff. Otherwise, if it reflects a mission whose `mission.md` has already been approved and the current prompt changes that mission's scope or intent, do not resume that mission. Keep the approved `mission.md` unchanged and follow `.agent/schemas/abort-protocol.md` using the scope or intent change as the blocker summary. After surfacing that abort to the user, confirm that the new prompt should be treated as fresh work before discarding or replacing the old handoff. If the agent will treat the current prompt as fresh work instead of resuming the loaded `handoff.md`, confirm with the dev before discarding or replacing that handoff. If the handoff is relevant, resume from its recorded Next / Ongoing Step per `.agent/schemas/handoff-protocol.md` only when that step clearly continues the same mission without reopening approved work.

If no relevant `handoff.md` exists at the worktree root, begin the interview. If a relevant `handoff.md` resumes Phase: Interview, continue from the recorded next question or step rather than restarting from scratch. Probe the user's request to clarify scope, intent, and any underlying considerations only as needed to complete the interview. Assess fast-path eligibility during the interview. The interview is complete when the lead agent has enough information to draft a mission.md and is confident all three eligibility criteria are met.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Generate mission.md

**Actor:** Lead agent.
**Inputs:** Interview findings, `.agent/schemas/mission-schema.md`.
**Outputs:** `mission.md` at the worktree root.

Draft a `mission.md` at the worktree root following `.agent/schemas/mission-schema.md`. The mission must be self-contained: a critic with access to only `CLAUDE.md` and `mission.md` must be able to evaluate it. The mission must not contain an Invariants section (its presence would violate eligibility criterion 1).

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Single-Critic Review

**Actor:** One critic agent.
**Inputs:** `CLAUDE.md`, `.agent/schemas/mission-schema.md`, and `mission.md` from the worktree root.
**Outputs:** `APPROVE` with no additional text, or `REJECT` followed by reasons.

Spawn one critic agent. The critic performs two checks in order:

1. **Eligibility validation** — confirm all three fast-path criteria are met. If any criterion fails, the critic must REJECT with the reason "not eligible for fast path."
2. **Mission review** — evaluate the mission.md against the schema and acceptance criteria, exactly as in a normal review.

There is no "approval with comments" — if changes are needed, the critic must REJECT.

- If the critic approves: that exact `mission.md` becomes the approved mission for the rest of this fast-path run and must not be modified. Proceed to Phase: Execute in Worktree.
- If the critic rejects for fast-path ineligibility: rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Blocked: request does not qualify for the fast path; await user direction.` Then stop executing this skill, inform the user that the request does not qualify for the fast path, and halt.
- If the critic rejects for other reasons: the lead agent fixes the issues and resubmits to a fresh critic. Repeat until approved, or escalate to the user if stuck.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Execute in Worktree

**Actor:** Lead agent.
**Inputs:** Approved `mission.md`, target repo codebase.
**Outputs:** Implementation (code changes in worktree), passing unit tests.

Execute the approved mission in an isolated git worktree. The exact `mission.md` approved in Phase: Single-Critic Review is the execution contract for this phase and must remain unchanged. Produce only the deliverables specified in scope. If implementation reveals that the mission itself must change, follow `.agent/schemas/abort-protocol.md`. Run all unit tests related to the changed code before proceeding. If tests fail, fix the issues before moving to Phase: Post-Implementation Review.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Post-Implementation Review

**Actor:** One fresh critic agent (not the Phase: Single-Critic Review critic).
**Inputs:** The diff (worktree changes), the exact `mission.md` approved in Phase: Single-Critic Review, and `CLAUDE.md` from the target repo. The critic also has access to the full target repo codebase on demand.
**Outputs:** `APPROVE` with no additional text, or `REJECT` followed by reasons.

Spawn a fresh critic agent. The critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the exact `mission.md` approved in Phase: Single-Critic Review, and does not violate any invariants in `CLAUDE.md`. There is no "approval with comments" — if changes are needed, the critic must REJECT. If the diff modifies or deletes existing test code, the critic must REJECT — the change is not eligible for fast path.

- If the critic approves: proceed to Phase: Cleanup.
- If the critic rejects because the change is no longer eligible for fast path: rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Blocked: request no longer qualifies for the fast path; await user direction.` Then stop this fast-path run, keep the approved `mission.md` unchanged, inform the user that the request no longer qualifies for the fast path, and halt. Do not continue this skill.
- If the critic rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree, re-runs related unit tests, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh critic. Repeat until approved, or escalate to the user if stuck.
- If the critic rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Cleanup

Before deleting any files, rewrite `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Phase: Cleanup - ensure mission.md is absent, then delete handoff.md last, then immediately present results to the user in the same turn.` Then remove `mission.md` if it still exists and `handoff.md` last from the worktree root. If cleanup is interrupted or any deletion fails before `handoff.md` is removed, leave that latest `handoff.md` state in place so the next session can resume cleanup deterministically. After both runtime artifacts are removed, remove the worktree via `git worktree remove --force`. If worktree removal fails, leave the worktree in place and report the failure to the user. Cleanup completion is the end of the mission lifecycle. Immediately after cleanup succeeds, present results to the user.
