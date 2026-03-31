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
- `.claude/commands/enhance-harness.md`
- `.claude/commands/new-sdlc.md`

### Changed worktree proposal copies inspected
- None. Each discovered governance path was compared against the worktree copy at the same repo-relative path, and every comparison matched: `CLAUDE.md`, `AGENTS.md`, `.agent/schemas/abort-protocol.md`, `.agent/schemas/claude-schema.md`, `.agent/schemas/critic-protocol.md`, `.agent/schemas/handoff-protocol.md`, `.agent/schemas/mission-schema.md`, `.agent/schemas/tdd-protocol.md`, `.claude/commands/enhance-harness.md`, and `.claude/commands/new-sdlc.md` all matched their worktree copies, so no changed proposal copy required separate inspection.

## Contradictions

- Resolve the merge-policy conflict between `.agent/schemas/claude-schema.md:5,15,20,35` and `.claude/commands/enhance-harness.md:58-60`. The schema says `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` are MR-gated and require human approval before the change is effective, but `enhance-harness` Cleanup says the approved worktree branch should merge directly back to repo-root `main` without explicit human approval. Because `enhance-harness` is the flow used to edit those same governance files, the two rules currently point to different release gates for the same class of change.
- No other contradictions were identified in the reviewed file set.

## Ambiguities

- Define what `new-sdlc` means by `install or activate each discovered repo-local skill` in `.claude/commands/new-sdlc.md:40`. The command does not say what counts as activation, whether discovery should use the target repo root or worktree copy when they differ, or what to do when a discovered skill cannot be installed in the current runtime.
- Define the coverage surface used by `.agent/schemas/tdd-protocol.md:9,13-14,56,60` and `.claude/commands/new-sdlc.md:16`. Terms like `code being touched by the mission` and `target code` are not operationalized, so different agents could choose different file sets for the same change and reach different fast-path or regression outcomes.
- Define what `if eligible` means in `.claude/commands/enhance-harness.md:58`. The Cleanup handoff text uses that qualifier, but the skill body only says Cleanup `prefers` direct merge in line 60 and never enumerates the actual eligibility conditions.
- No additional ambiguities were identified in `CLAUDE.md`, `AGENTS.md`, `.agent/schemas/abort-protocol.md`, `.agent/schemas/claude-schema.md`, `.agent/schemas/critic-protocol.md`, `.agent/schemas/handoff-protocol.md`, or `.agent/schemas/mission-schema.md` beyond the cross-file issues above.

## Markdown to Script Conversions

- Add a `mission.md` linter driven by `.agent/schemas/mission-schema.md`, `.agent/schemas/tdd-protocol.md`, and `.agent/schemas/claude-schema.md` to catch missing acceptance-criterion coverage, invalid TDD-exempt assumptions, and invariant or consideration misuse before critic review.
- Add a critic-prompt validator driven by `.agent/schemas/critic-protocol.md` and the skill files under `.claude/commands/` to ensure only allowed artifact paths, worktree paths, and raw tool outputs reach critic agents.
- Add a cleanup or merge gate script driven by `CLAUDE.md` Invariant 4 and the Cleanup sections in `.claude/commands/enhance-harness.md` and `.claude/commands/new-sdlc.md` to detect non-trivial merges, regenerate the correct handoff phase reset, and refuse cleanup while the worktree is dirty.
- Add an automation or script for this governance review itself that enumerates the authoritative Markdown surface, flags changed worktree proposal copies, and rewrites `TODO.md` with the required sections on each run.
