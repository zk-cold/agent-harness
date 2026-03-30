# AGENTS.md

Read `CLAUDE.md` first and treat it as the canonical source of repository instructions.

This file exists only because Codex reads `AGENTS.md`.

Codex-specific adapter: when `CLAUDE.md` or a command under `./.claude/commands/` requires spawning critic or other review agents, any Codex approval gate for that spawn is a blocker to surface to the user, not permission to skip the step.

When `CLAUDE.md` tells the agent to invoke a Claude slash-command, interpret `/name` as `./.claude/commands/name.md` and follow that file.

Do not duplicate shared harness rules here. Update the shared docs instead.
