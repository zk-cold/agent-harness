# New SDLC

This skill handles requests to build new features or make changes in a target repo using the fast-path SDLC. The lead agent must follow these phases in order.

## Fast-Path Eligibility

A request qualifies for the fast path only when all three criteria are met:

1. **No invariant changes** — the mission does not propose new or modified invariants for `CLAUDE.md`.
2. **>80% test coverage around target code** — the code being changed is already covered by automated tests at >80% line coverage, providing a safety net for regressions.
3. **Clear scope, limited & safe change** — the change is well-defined, small in blast radius, and unlikely to introduce systemic risk.

If any criterion is not met, the lead agent must not proceed. Inform the user that the request does not qualify for the fast path and halt.

## Phase 1: Interview

**Actor:** Lead agent.
**Inputs:** User's request.
**Outputs:** Enough context to draft a mission.md.

Probe the user's request to clarify scope, intent, and any underlying considerations. Ask targeted questions — do not assume. Assess fast-path eligibility during the interview. The interview is complete when the lead agent has enough information to draft a mission.md and is confident all three eligibility criteria are met.

## Phase 2: Generate mission.md

**Actor:** Lead agent.
**Inputs:** Interview findings, `.agent/schemas/mission-schema.md`.
**Outputs:** `mission.md` at the target repo root.

Draft a `mission.md` following `.agent/schemas/mission-schema.md`. The mission must be self-contained: a critic with access to only `CLAUDE.md` and `mission.md` must be able to evaluate it. The mission must not contain an Invariants section (its presence would violate eligibility criterion 1).

## Phase 3: Single-Critic Review

**Actor:** One critic agent.
**Inputs:** `CLAUDE.md`, `.agent/schemas/mission-schema.md`, and `mission.md` from the target repo.
**Outputs:** APPROVE or REJECT (with reason).

Spawn one critic agent. The critic performs two checks in order:

1. **Eligibility validation** — confirm all three fast-path criteria are met. If any criterion fails, the critic must REJECT with the reason "not eligible for fast path."
2. **Mission review** — evaluate the mission.md against the schema and acceptance criteria, exactly as in a normal review.

There is no "approval with comments" — if changes are needed, the critic must REJECT.

- If the critic approves: proceed to Phase 4.
- If the critic rejects for fast-path ineligibility: the lead agent escalates to the normal flow (stop executing this skill and inform the user).
- If the critic rejects for other reasons: the lead agent fixes the issues and resubmits to a fresh critic. Repeat until approved, or escalate to the user if stuck.

## Phase 4: Execute in Worktree

**Actor:** Lead agent.
**Inputs:** Approved `mission.md`, target repo codebase.
**Outputs:** Implementation (code changes in worktree), passing unit tests.

Execute the approved mission in an isolated git worktree. Produce only the deliverables specified in scope. Run all unit tests related to the changed code before proceeding. If tests fail, fix the issues before moving to Phase 5.

## Phase 5: Post-Implementation Review

**Actor:** One fresh critic agent (not the Phase 3 critic).
**Inputs:** The diff (worktree changes), `mission.md`, and `CLAUDE.md` from the target repo. The critic also has access to the full target repo codebase on demand.
**Outputs:** APPROVE or REJECT (with reason).

Spawn a fresh critic agent. The critic evaluates whether the implementation satisfies all acceptance criteria in `mission.md` and does not violate any invariants in `CLAUDE.md`. There is no "approval with comments" — if changes are needed, the critic must REJECT.

- If the critic approves: present results to the user. The mission is complete.
- If the critic rejects: the lead agent fixes the issues in the worktree, re-runs related unit tests, and resubmits the updated diff to a fresh critic. Repeat until approved, or escalate to the user if stuck.
