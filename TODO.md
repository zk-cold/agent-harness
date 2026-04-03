# Repository Governance Review TODO

## Reviewed Files

### Authoritative files inspected
- `CLAUDE.md`
- `AGENTS.md`
- `.agent/schemas/abort-protocol.md`
- `.agent/schemas/claude-schema.md`
- `.agent/schemas/critic-protocol.md`
- `.agent/schemas/handoff-protocol.md`
- `.agent/schemas/mission-schema.md`
- `.agent/schemas/tdd-protocol.md`
- `.claude/commands/new-sdlc.md`

### Changed worktree proposal copies inspected
- None. Each discovered governance path was compared against the worktree copy at the same repo-relative path, and every comparison matched: `CLAUDE.md`, `AGENTS.md`, `.agent/schemas/abort-protocol.md`, `.agent/schemas/claude-schema.md`, `.agent/schemas/critic-protocol.md`, `.agent/schemas/handoff-protocol.md`, `.agent/schemas/mission-schema.md`, `.agent/schemas/tdd-protocol.md`, and `.claude/commands/new-sdlc.md` all matched their worktree copies, so no changed proposal copy required separate inspection.

## Contradictions

- No open contradictions.

## Ambiguities

- Define what `new-sdlc` means by `install or activate each discovered repo-local skill` in `.claude/commands/new-sdlc.md:40`. The command does not say what counts as activation, whether discovery should use the target repo root or worktree copy when they differ, or what to do when a discovered skill cannot be installed in the current runtime.
- Define the coverage surface used by `.agent/schemas/tdd-protocol.md:9,13-14,56,60` and `.claude/commands/new-sdlc.md:16`. Terms like `code being touched by the mission` and `target code` are not operationalized, so different agents could choose different file sets for the same change and reach different fast-path or regression outcomes.
- No additional ambiguities were identified in `CLAUDE.md`, `AGENTS.md`, `.agent/schemas/abort-protocol.md`, `.agent/schemas/claude-schema.md`, `.agent/schemas/critic-protocol.md`, `.agent/schemas/handoff-protocol.md`, or `.agent/schemas/mission-schema.md` beyond the cross-file issues above.

## Markdown to Script Conversions

- Add a critic-prompt validator driven by `.agent/schemas/critic-protocol.md` and the skill files under `.claude/commands/` to ensure only allowed artifact paths, worktree paths, and raw tool outputs reach critic agents.
- Add an automation or script for this governance review itself that enumerates the authoritative Markdown surface, flags changed worktree proposal copies, and rewrites `TODO.md` with the required sections on each run.
