# Enhance Harness

This skill handles requests to modify or improve the agent harness itself. For a fresh request, the lead agent must follow these phases in order. If a relevant `handoff.md` exists on session start, the lead agent may resume only from a recorded Next / Ongoing Step that clearly maps to one of the phases below or a substep within the current phase. If that handoff marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume it. Otherwise, if the recorded step does not clearly map to a phase or substep, the lead agent must ask the dev how to proceed instead of skipping required phases.

## Required Critic Availability

Any phase in this skill that requires critic agents is blocking. If the environment requires explicit user approval before spawning a required critic, the user declines, or the critic tool is otherwise unavailable, the lead agent must fully rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Blocked: awaiting user approval or tool availability to spawn the required critic agent(s) for <phase name>. Do not resume past this phase without that review.` Then stop, surface the blocker to the dev, and await direction. The lead agent must not skip the blocked review phase, continue execution, or proceed to Cleanup past it.

## Phase: Interview

On session start, inspect `.claude/worktrees/` and the main project root before any interview questions. If `handoff.md` or `mission.md` exists at the main project root, stop and ask the dev how to proceed before continuing. Otherwise, if exactly one worktree exists and it contains `handoff.md` at its root, load that `handoff.md` and use it to orient before proceeding. If multiple worktrees exist, or if exactly one worktree exists but it does not contain `handoff.md`, stop and ask the dev how to proceed before continuing. If no worktree exists and no legacy root runtime artifacts exist, create one before any interview or execution work begins. If the loaded `handoff.md` marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, do not resume that mission. Summarize the blockers from the old handoff to the user, and confirm that the current prompt should be treated as fresh work before discarding or replacing that handoff. Otherwise, if it reflects a mission whose `mission.md` has already been approved and the current prompt changes that mission's scope or intent, do not resume that mission. Keep the approved `mission.md` unchanged and follow `.agent/schemas/abort-protocol.md` using the scope or intent change as the blocker summary. After surfacing that abort to the user, confirm that the new prompt should be treated as fresh work before discarding or replacing the old handoff. If the agent will treat the current prompt as fresh work instead of resuming the loaded `handoff.md`, confirm with the dev before discarding or replacing that handoff. If the handoff is relevant, resume from its recorded Next / Ongoing Step per `.agent/schemas/handoff-protocol.md` only when that step clearly continues the same mission without reopening approved work.

If no relevant `handoff.md` exists at the worktree root, begin the interview. If a relevant `handoff.md` resumes Phase: Interview, continue from the recorded next question or step rather than restarting from scratch. Probe the user's request to clarify scope, intent, and any underlying invariants or considerations only as needed to complete the interview. The interview is complete when the lead agent has enough information to draft a mission.md.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Generate mission.md

Draft a `mission.md` at the worktree root following `.agent/schemas/mission-schema.md`. The mission must be self-contained: a critic with access to only `CLAUDE.md`, `.agent/schemas/critic-protocol.md`, and `mission.md` must be able to evaluate it.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: 2-Critic Review

Spawn two independent critic agents for `mission.md` review. Each critic reads only `CLAUDE.md`, `.agent/schemas/critic-protocol.md`, `.agent/schemas/mission-schema.md`, and `mission.md`, and must follow `.agent/schemas/critic-protocol.md`. If the critics cannot be spawned, follow Required Critic Availability before taking any other action.

- If both approve: that exact `mission.md` becomes the approved mission for the rest of this mission and must not be modified. Proceed to Phase: Execute in Worktree.
- If either rejects: the lead agent fixes the issues and resubmits to two fresh critic agents. Repeat until both approve, or escalate to the user if stuck.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Execute in Worktree

Execute the approved mission in an isolated git worktree. The exact `mission.md` approved in Phase: 2-Critic Review is the execution contract for this phase and must remain unchanged. Produce only the deliverables specified in scope. If implementation reveals that the mission itself must change, follow `.agent/schemas/abort-protocol.md`. On completion, verify all acceptance criteria are met before proceeding to Phase: Single-Critic Completion Review.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Single-Critic Completion Review

**Actor:** One fresh critic agent (not one of the Phase: 2-Critic Review critics).
**Inputs:** The diff (worktree changes), the exact `mission.md` approved in Phase: 2-Critic Review, `CLAUDE.md` from the target repo, and `.agent/schemas/critic-protocol.md`. The critic also has access to the full target repo codebase on demand.
**Outputs:** Response per `.agent/schemas/critic-protocol.md`.

Spawn a fresh critic agent. The critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the exact `mission.md` approved in Phase: 2-Critic Review, and does not violate any invariants in `CLAUDE.md`. The critic must follow `.agent/schemas/critic-protocol.md`. If the critic cannot be spawned, follow Required Critic Availability before taking any other action.

- If the critic approves: proceed to Phase: Cleanup.
- If the critic rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh critic. Repeat until approved, or escalate to the user if stuck.
- If the critic rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Cleanup

Before deleting any files, rewrite `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Phase: Cleanup - ensure mission.md is absent, then delete handoff.md last, then immediately present results to the user in the same turn.` Then remove `mission.md` if it still exists and `handoff.md` last from the worktree root. If cleanup is interrupted or any deletion fails before `handoff.md` is removed, leave that latest `handoff.md` state in place so the next session can resume cleanup deterministically. After both runtime artifacts are removed, remove the worktree via `git worktree remove --force`. If worktree removal fails, leave the worktree in place and report the failure to the user. Cleanup completion is the end of the mission lifecycle. Immediately after cleanup succeeds, present results to the user.
