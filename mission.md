# Mission: Define the mission.md Schema

## Invariants (Founding)

These are the founding invariants for this project, established simultaneously with CLAUDE.md as part of the bootstrap. They are not proposals requiring gating — they are the initial state.

1. **CLAUDE.md is the sole source of truth for project-level invariants.**
2. **CLAUDE.md changes are always part of an MR** — never applied directly by an agent without review.
3. **handoff.md is always current.** It must be updated at every checkpoint and before any session abort. It is always rewritten in full, never appended.
4. **Session files are session-scoped.** `journal.md` and `errors.md` are append-only during a session and never modified retroactively.
5. **Every task runs in an isolated worktree.** There is no rollback mechanism; abort is the recovery strategy.
6. **Abort on blocker.** If lead agent identifies a blocker, it must: create a Jira ticket, update handoff.md, and halt. No self-resolution of blockers.
7. **Pseudo-invariants are rejected.** Any proposed invariant that is actually a preference or historical habit must be identified and excluded during critic review.

## Important Considerations

- CLAUDE.md has two sections: **Invariants** (strict gatekeeping, rarely modified) and **Important Considerations** (explicit derivations from invariants to compensate for current model limitations). Considerations may be pruned as model capability improves.
- handoff.md stores current state only. Historical detail belongs in `journal.md`.
- A new lead agent instance reads handoff.md first. If relevance to the current task is unclear, it must confirm with dev before proceeding — no autonomous inference of relevance.
- Critic agents operate with fresh context: they read CLAUDE.md, mission.md, and any code they choose to browse. They do not read journal or errors files.
- "No approval with comments" is enforced. A critic either approves cleanly or rejects with reasons. Ambiguous approvals are not valid outputs.
- Fast path rejection by a critic automatically escalates to normal flow — lead agent does not re-evaluate.
- Coverage reports are provided to critics directly; critics do not re-run coverage tooling.
- If a dev decision materially affects at least one proposed AC during interview, lead agent must probe for the underlying invariant or consideration.

## Scope

**In scope:**
- mission.md schema definition: required sections, their purpose, and constraints on each
- Guidance for when each section applies (e.g., when "Invariants (New)" is empty vs populated)

**Out of scope:**
- `.agent/` directory structure and other file schemas (handoff, journal, errors)
- Pre-execution flow, critic design, session lifecycle
- Abort/escalation protocol specifications
- Lead agent orchestration and sub-agent design
- MR/PR tooling, Jira integration, harness infrastructure

## Dependencies & Assumptions

- CLAUDE.md exists at project root with Invariants and Important Considerations sections.
- The mission.md schema will be consumed by lead agents (to generate) and critic agents (to review).

## Acceptance Criteria

1. mission.md schema is defined with required sections (Scope, Acceptance Criteria) and optional sections (Invariants, Important Considerations, Dependencies & Assumptions).
2. Each section has a clear description of its purpose and constraints (e.g., what qualifies as an invariant vs a consideration, what "testable" means for an AC).
3. Guidance is provided for when optional sections should be included or omitted.
4. Fast path eligibility can be determined from the presence or absence of the Invariants section.
