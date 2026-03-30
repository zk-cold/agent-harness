# New SDLC

This skill handles requests to build new features or make changes in a target repo. It supports two flows: the **fast path** for small, safe, well-covered changes, and the **normal flow** for everything else. For a fresh request, the lead agent must follow the shared phases and then the flow-specific phases in order. When operating inside a target repo, that repo's `CLAUDE.md` invariants and important considerations govern ahead of this harness's generic defaults, and any target-repo-specific dependencies or assumptions recorded in the mission govern execution decisions unless doing so would violate the target repo's own invariants. If a relevant `handoff.md` exists on session start, the lead agent may resume only from a recorded Next / Ongoing Step that clearly maps to one of the phases below or a substep within the current phase. If that handoff marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume it. Otherwise, if the recorded step does not clearly map to a phase or substep, the lead agent must ask the dev how to proceed instead of skipping required phases.

## Required Critic Availability

Any phase in this skill that requires critic agents is blocking. If the environment requires explicit user approval before spawning a required critic, the user declines, or the critic tool is otherwise unavailable, the lead agent must fully rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Blocked: awaiting user approval or tool availability to spawn the required critic agent(s) for <phase name>. Do not resume past this phase without that review.` Then stop, surface the blocker to the dev, and await direction. The lead agent must not skip the blocked review phase, continue execution, or proceed to Cleanup past it.

For this skill, harness-side references to `CLAUDE.md`, files under `.agent/schemas/`, and harness skill-definition files under `.claude/commands/` mean the harness repo-root copies until the relevant change is merged. For the target repo, `CLAUDE.md` and any skill-definition files it directs the agent to use are resolved from the target repo root until merged. Matching worktree files and unstaged changes are proposals only; when a review phase exposes those changed files through diff output or repository access, the reviewer inspects the proposal while the corresponding repo-root copy remains authoritative.

## Fast-Path Eligibility

A request qualifies for the fast path only when all three criteria are met:

1. **No invariant changes** — the mission does not propose new or modified invariants for `CLAUDE.md`. This includes modifications or deletions of existing test code (see CLAUDE.md). Adding new tests is not an invariant change.
2. **>80% test coverage around target code** — the code being changed is already covered by automated tests at the coverage threshold defined in `.agent/schemas/tdd-protocol.md`, providing a safety net for regressions. If no coverage tool is available and the mission does not include coverage tool setup as in-scope, the request is ineligible for fast path.
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

On session start, the lead agent must inspect `.claude/worktrees/` and the main project root of the target repo before any interview questions. If `handoff.md` or `mission.md` exists at the main project root, the lead agent must stop and ask the dev how to proceed before continuing. Otherwise, if exactly one worktree exists and it contains `handoff.md` at its root, the lead agent must load that `handoff.md` and use it to orient before proceeding. If multiple worktrees exist, or if exactly one worktree exists but it does not contain `handoff.md`, the lead agent must stop and ask the dev how to proceed before continuing. If no worktree exists and no legacy root runtime artifacts exist, the lead agent must create a worktree before any interview or execution work begins. If the loaded `handoff.md` marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume that mission. Summarize the blockers from the old handoff to the user, then either follow the Recovery Protocol in `.agent/schemas/handoff-protocol.md` or confirm that the current prompt should be treated as fresh work before discarding or replacing that handoff. Any mission recovered from abort is ineligible for fast path: it restarts from Phase: Interview under the Recovery Protocol and then routes to normal flow. Otherwise, if it reflects a mission whose `mission.md` has already been approved and the current prompt changes that mission's scope or intent, the lead agent must not resume that mission. Keep the approved `mission.md` unchanged and follow `.agent/schemas/abort-protocol.md` using the scope or intent change as the blocker summary. After surfacing that abort to the user, confirm that the new prompt should be treated as fresh work before discarding or replacing the old handoff. If the lead agent will treat the current prompt as fresh work instead of resuming the loaded `handoff.md`, confirm with the dev before discarding or replacing that handoff. If the handoff is relevant, the lead agent may resume from its recorded Next / Ongoing Step per `.agent/schemas/handoff-protocol.md` only when that step clearly continues the same mission without reopening approved work. Spawned non-lead agents operate only on the role-specific inputs granted by their phase and do not rerun this bootstrap discovery unless that phase explicitly requires it.

If no relevant `handoff.md` exists at the worktree root, begin the interview. If a relevant `handoff.md` resumes Phase: Interview, continue from the recorded next question or step rather than restarting from scratch. Probe the user's request to clarify scope, intent, and any underlying considerations only as needed to complete the interview. First determine which repo is the target repo, and if that is not automatically clear, ask the user to clarify before proceeding. Once the target repo is identified, read and follow that repo's `CLAUDE.md` before any repo-specific analysis or execution begins, then search the target repo for `SKILL.md` files and install or activate each discovered repo-local skill before continuing mission work there unless no `SKILL.md` files are found. Assess fast-path eligibility during the interview. The interview is complete when the lead agent has enough information to draft a mission.md and has determined which flow applies.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Generate mission.md

**Actor:** Lead agent.
**Inputs:** Interview findings, `.agent/schemas/mission-schema.md`.
**Outputs:** `mission.md` at the worktree root.

Draft a `mission.md` at the worktree root following the harness repo-root `.agent/schemas/mission-schema.md`. The mission must be self-contained: a critic with access to only the target repo-root `CLAUDE.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, and `mission.md` must be able to evaluate it. If the request qualifies for the fast path, the mission must not contain an Invariants section (its presence would violate eligibility criterion 1).

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Fast-Path Flow

## Phase: Single-Critic Review

**Actor:** One critic agent.
**Inputs:** The target repo-root `CLAUDE.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, the harness repo-root `.agent/schemas/mission-schema.md`, `mission.md` from the worktree root, and any raw eligibility tool outputs explicitly relied on during interview, such as coverage report output.
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
**Outputs:** Implementation (code changes in worktree), passing unit tests, no coverage regression.

Execute the approved mission in an isolated git worktree. The exact `mission.md` approved in Phase: Single-Critic Review is the execution contract for this phase and must remain unchanged. Produce only the deliverables specified in scope. If implementation reveals that the mission itself must change, follow `.agent/schemas/abort-protocol.md`.

If the mission declares a TDD exemption per `.agent/schemas/tdd-protocol.md`, verify the exemption is valid (all deliverables are non-executable artifacts), then execute without the TDD loop. Otherwise, follow the TDD Execution Loop defined in `.agent/schemas/tdd-protocol.md`. This includes: setup/verify coverage tool, measure baseline, fill coverage gaps to threshold, per-AC red-green cycle, and final verification (full suite + coverage regression check).

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Post-Implementation Review (Fast Path)

**Actor:** One fresh critic agent (not the Phase: Single-Critic Review critic).
**Inputs:** The exact `mission.md` approved in Phase: Single-Critic Review, the target repo-root `CLAUDE.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, and read-only tool access to the worktree and repository. The critic is a tool-capable critic per `.agent/schemas/critic-protocol.md`.
**Outputs:** Response per `.agent/schemas/critic-protocol.md`.

Before spawning the critic, the lead agent must write any heavy verification outputs (test suite results, coverage reports) as runtime artifact files at the worktree root per the Completion-Review Tool Access section of `.agent/schemas/critic-protocol.md`.

Spawn a fresh critic agent with read-only tool access and the worktree path. The critic uses its granted tools (Read, Grep, Glob, `git diff`, `git log`, `git show`) to inspect the changes and codebase directly. The critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the exact `mission.md` approved in Phase: Single-Critic Review, and does not violate any invariants in the target repo-root `CLAUDE.md`. The critic must follow the harness repo-root `.agent/schemas/critic-protocol.md`. The critic prompt must contain only the governing artifact references and the worktree path, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If changed target-repo governance or skill-definition files are discoverable through the critic's tool access, the critic reviews them as proposals while the corresponding repo-root copies remain authoritative until merge. If review would require information outside the approved mission, the phase-allowed artifacts, or tool-accessible data, do not brief the critic; follow `.agent/schemas/abort-protocol.md` or the applicable escalation flow instead. If the critic cannot be spawned, follow Required Critic Availability before taking any other action. If the diff modifies or deletes existing test code, the critic must REJECT — the change is not eligible for fast path.

- If the critic approves: proceed to Phase: Cleanup.
- If the critic rejects because the change is no longer eligible for fast path: escalate to normal flow per Escalation: Fast Path to Normal Flow.
- If the critic rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree, re-runs related unit tests, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh critic. Repeat until approved, or escalate to the user if stuck.
- If the critic rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Escalation: Fast Path to Normal Flow

When fast-path eligibility is lost during or after implementation (e.g., the post-implementation critic rejects for eligibility), the lead agent must evaluate whether the approved `mission.md` can be submitted intact to normal-flow review:

- **If `mission.md` can be submitted intact** (no fast-path-specific language that would need removal): The lead agent submits it to one additional critic for mission review, following the same critic-prompt constraints as normal-flow Phase: 2-Critic Mission Review. This brings the total mission-review approvals to two (one from the fast-path Single-Critic Review, one from this escalation review). If this critic approves, the mission remains the approved mission and the lead agent proceeds to normal-flow Phase: Dev Agent Execution, handing the dev subagent the approved `mission.md` and the unstaged work from the fast-path attempt. If this critic rejects, the lead agent fixes the issues and resubmits to a fresh critic. Repeat until approved, or escalate to the user if stuck.

- **If `mission.md` requires modification** (e.g., contains fast-path-specific language): The lead agent aborts per `.agent/schemas/abort-protocol.md`, keeping the approved `mission.md` unchanged. Then follow the Recovery Protocol in `.agent/schemas/handoff-protocol.md`: restart from Phase: Interview, draft a new `mission.md` only after the recovery interview is complete, submit it to full 2-Critic Mission Review, and proceed through normal-flow execution. Unstaged work from the fast-path attempt is preserved in the worktree for the dev agent.

If the escalation critic cannot be spawned, follow Required Critic Availability before taking any other action.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Normal Flow

## Phase: 2-Critic Mission Review

**Actor:** Two independent critic agents.
**Inputs:** The target repo-root `CLAUDE.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, the harness repo-root `.agent/schemas/mission-schema.md`, `mission.md` from the worktree root.
**Outputs:** Response per `.agent/schemas/critic-protocol.md` from each critic.

Spawn two independent critic agents for `mission.md` review. Each critic reads only the target repo-root `CLAUDE.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, the harness repo-root `.agent/schemas/mission-schema.md`, and `mission.md`, and must follow the harness repo-root `.agent/schemas/critic-protocol.md`. The critic prompt must contain only those artifact references, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If anything needs to be included before approval, put it in `mission.md` or another phase-allowed artifact first, then rerun review. If the critics cannot be spawned, follow Required Critic Availability before taking any other action.

- If both approve: that exact `mission.md` becomes the approved mission for the rest of this mission and must not be modified. Proceed to normal-flow Phase: Dev Agent Execution.
- If either rejects: the lead agent fixes the issues and resubmits to two fresh critic agents. Repeat until both approve, or escalate to the user if stuck.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: Dev Agent Execution

**Actor:** Dev subagent (spawned by the lead agent via the Agent tool).
**Inputs:** Approved `mission.md`, target repo codebase (in worktree). If escalated from fast path, any unstaged work from the fast-path attempt is present in the worktree.
**Outputs:** Implementation (code changes in worktree), passing full regression suite, clean formatter/linter results.

The lead agent spawns a dev subagent and hands it the approved `mission.md`. The dev agent executes the approved mission in the worktree from that handed-off context and must not rerun session-start bootstrap discovery of `.claude/worktrees/`, the main project root, `handoff.md`, or `mission.md` unless a later phase explicitly requires it. The exact `mission.md` approved in the preceding review phase is the execution contract and must remain unchanged. The dev agent must produce only the deliverables specified in scope. If implementation reveals that the mission itself must change, the dev agent must stop and report the blocker to the lead agent, who then follows `.agent/schemas/abort-protocol.md`.

If the mission declares a TDD exemption per `.agent/schemas/tdd-protocol.md`, the dev agent verifies the exemption is valid (all deliverables are non-executable artifacts), then executes without the TDD loop. Otherwise, the dev agent must follow the TDD Execution Loop defined in `.agent/schemas/tdd-protocol.md`. This includes: setup/verify coverage tool, measure baseline, fill coverage gaps to threshold, per-AC red-green cycle, and final verification (full suite + coverage regression check + formatter/linter).

Only after the TDD loop's final verification passes (or, for TDD-exempt missions, after all deliverables are produced and acceptance criteria verified) does the dev agent report completion to the lead agent.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Phase: 2-Critic Post-Implementation Review

**Actor:** Two fresh critic agents (not any previously used critics in this mission).
**Inputs:** The exact approved `mission.md`, the target repo-root `CLAUDE.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, and read-only tool access to the worktree and repository. Each critic is a tool-capable critic per `.agent/schemas/critic-protocol.md`.
**Outputs:** Response per `.agent/schemas/critic-protocol.md` from each critic.

Before spawning the critics, the lead agent must write any heavy verification outputs (full test suite results, coverage reports, linter output) as runtime artifact files at the worktree root per the Completion-Review Tool Access section of `.agent/schemas/critic-protocol.md`.

Spawn two fresh critic agents, each with read-only tool access and the worktree path. Each critic uses its granted tools (Read, Grep, Glob, `git diff`, `git log`, `git show`) to inspect the changes and codebase directly. Each critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the approved `mission.md`, and does not violate any invariants in the target repo-root `CLAUDE.md`. Each critic must follow the harness repo-root `.agent/schemas/critic-protocol.md`. The critic prompt must contain only the governing artifact references and the worktree path, with no lead-agent context briefing, summary, hidden rationale, "things to keep in mind," or extra "mentions." If changed target-repo governance or skill-definition files are discoverable through each critic's tool access, the critic reviews them as proposals while the corresponding repo-root copies remain authoritative until merge. If review would require information outside the approved mission, the phase-allowed artifacts, or tool-accessible data, do not brief the critics; follow `.agent/schemas/abort-protocol.md` instead. If the critics cannot be spawned, follow Required Critic Availability before taking any other action.

- If both approve: proceed to Phase: Cleanup.
- If either rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree (or instructs the dev subagent to fix them), re-runs the full regression suite, re-verifies all acceptance criteria, and resubmits the updated diff to two fresh critics. Repeat until both approve, or escalate to the user if stuck.
- If either rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

---

# Phase: Cleanup

Before deleting any files, rewrite `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Phase: Cleanup - ensure mission.md is absent, then delete handoff.md last, then immediately present results to the user in the same turn.` Then remove `mission.md` if it still exists and `handoff.md` last from the worktree root. If cleanup is interrupted or any deletion fails before `handoff.md` is removed, leave that latest `handoff.md` state in place so the next session can resume cleanup deterministically. After both runtime artifacts are removed, verify that the worktree has no uncommitted changes before removing it. Run `git status` in the worktree and check for unstaged modifications, staged-but-uncommitted changes, and untracked files. If any uncommitted changes are detected, do not remove the worktree — stop, report the uncommitted state to the user (listing the affected files), and leave the worktree in place. Only when the worktree is clean (all changes committed to the branch) proceed to remove the worktree via `git worktree remove --force`. If worktree removal fails, leave the worktree in place and report the failure to the user. Cleanup completion is the end of the mission lifecycle. Immediately after cleanup succeeds, present results to the user.
