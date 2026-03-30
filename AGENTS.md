# AGENTS.md

Read the repo-root `CLAUDE.md` first and treat it as the canonical source of repository instructions. Until the relevant change is merged, do not treat a matching `CLAUDE.md` inside the active worktree as authoritative.

Compliance with `CLAUDE.md` Invariants 1 and 2 is mandatory before any other analysis or execution.

When `CLAUDE.md` tells the agent to invoke a Claude slash-command, interpret `/name` as the repo-root `./.claude/commands/name.md` and follow that file. Until the relevant change is merged, do not treat a matching command file inside the active worktree as authoritative.

When repo-root `CLAUDE.md` or a repo-root command under `./.claude/commands/` requires spawning critic or other review agents, any Codex approval gate for that spawn is a blocker to surface to the user, not permission to skip the step.

Do not duplicate shared harness rules here. Update the shared docs instead.
