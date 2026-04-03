# Invariants
## Harness Centered Around Claude Code
Do not duplicate shared harness rules here. Update the shared docs instead.

# Considerations
## Read CLAUDE.md First
Treat it as the canonical source of repository instructions.

Compliance with `CLAUDE.md` Invariants before any other analysis or execution.

When repo-root `CLAUDE.md` or a repo-root command under `./.claude/commands/` requires spawning critic or other review agents, any Codex approval gate for that spawn is a blocker to surface to the user, not permission to skip the step.

## Locating Claude Commands
For Claude slash-commands, interpret `/name` as the repo-root `./.claude/commands/name.md` and follow that file.
