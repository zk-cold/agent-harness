# Enhance Harness

This skill handles requests to modify or improve the agent harness itself. The lead agent must follow these phases in order.

## Phase: Interview

Check for an existing `handoff.md` at the project root. If one exists, load it and use its contents to orient before proceeding, per `.agent/schemas/handoff-protocol.md`.

Probe the user's request to clarify scope, intent, and any underlying invariants or considerations. Ask targeted questions — do not assume. The interview is complete when the lead agent has enough information to draft a mission.md.

Write/update `handoff.md` at the project root per `.agent/schemas/handoff-protocol.md`.

## Phase: Generate mission.md

Draft a `mission.md` at the project root following `.agent/schemas/mission-schema.md`. The mission must be self-contained: a critic with access to only `CLAUDE.md` and `mission.md` must be able to evaluate it.

Write/update `handoff.md` at the project root per `.agent/schemas/handoff-protocol.md`.

## Phase: 2-Critic Review

Spawn two independent critic agents. Each critic reads only `CLAUDE.md`, `.agent/schemas/mission-schema.md`, and `mission.md`. Each returns APPROVE or REJECT (with reasons). There is no "approval with comments" — if changes are needed, the critic must REJECT.

- If both approve: proceed to Phase: Execute in Worktree.
- If either rejects: the lead agent fixes the issues and resubmits to two fresh critics. Repeat until both approve, or escalate to the user if stuck.

Write/update `handoff.md` at the project root per `.agent/schemas/handoff-protocol.md`.

## Phase: Execute in Worktree

Execute the approved mission in an isolated git worktree. Produce only the deliverables specified in scope. On completion, verify all acceptance criteria are met before presenting results to the user.

Write/update `handoff.md` at the project root per `.agent/schemas/handoff-protocol.md`.

## Phase: Cleanup

Remove both `mission.md` and `handoff.md` from the project root per `.agent/schemas/handoff-protocol.md`.
