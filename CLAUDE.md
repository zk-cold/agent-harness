# CLAUDE.md

## Invariants

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
