# Invariants

## AGENTS File Scope
This file only governs runtimes that read `AGENTS.md`.

## Project-Level Governance Source
For project-level invariants, follow `CLAUDE.md`.

## Slash Command Resolution
Interpret `/name` commands as repo-root `./.claude/commands/name.md` and follow that file.

# Considerations

## AGENTS Audience
This file is intentionally specific to Codex in this harness. It is a routing artifact for runtimes that read `AGENTS.md`, not a generic project-governance entrypoint.

## AGENTS Scope
This file does not redefine the audience or scope of any other governance artifact. References to other files identify routing targets for Codex runtimes only.

## Codex Sub-Agent Behavior
Codex runtimes in this harness may continue using `AGENTS.md` even when later routing decisions require them to ignore `CLAUDE.md`. This note explains the file's practical usefulness without altering any other artifact's scope.
