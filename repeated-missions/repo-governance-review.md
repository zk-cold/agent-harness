# Mission: Review repository governance Markdown into TODO.md

## Scope

### In scope:
- Create or overwrite `TODO.md` at the active worktree's repo root so it reviews repository governance Markdown discovered at execution time.
- Discover the review surface at execution time using this rule: always include repo-root `CLAUDE.md`; include repo-root `AGENTS.md` if it exists; include every Markdown file that is directly inside repo-root `.agent/schemas/`; include every Markdown file that is directly inside repo-root `.claude/commands/`; do not recurse into nested subdirectories.
- If any path discovered by that rule also has a changed worktree copy in the active worktree, inspect that changed worktree copy as a proposal while still treating the repo-root copy as authoritative.
- Identify contradictions across the review surface discovered by that rule.
- Identify ambiguities across the review surface discovered by that rule.
- Suggest concrete candidates for converting Markdown-described procedures in the discovered review surface into scripts, checks, or automations.

### Out of scope:
- Modifying any existing repository file, including governance artifacts and schemas, except overwriting `TODO.md` if it already exists.
- Implementing any suggested scripts, checks, or process changes.
- Creating or scheduling an automation from this mission.
- Reviewing non-Markdown files, generated files, or editor metadata.
- Reviewing Git internals except for the minimal read-only diff or status data needed to determine whether a discovered governance path also has a changed worktree copy that must be inspected as a proposal.

## Dependencies & Assumptions

- Dependency: The executing agent has read access to the repo-root files selected by the review-surface discovery rule in Scope and to the minimal read-only Git data needed to detect changed worktree proposal copies for those same paths.
- Dependency: Repo-root `CLAUDE.md` exists, and any repo-root `AGENTS.md`, `.agent/schemas/*.md`, or `.claude/commands/*.md` files discovered by the rule are readable at execution time.
- Assumption: This mission evaluates the repository state that exists when execution begins rather than a preapproved snapshot, and `TODO.md` will record the exact authoritative files reviewed plus any changed worktree proposal copies inspected so the run remains auditable and reusable.
- Assumption: This mission is TDD exempt because every in-scope deliverable is a non-executable Markdown artifact; if any executable code, script, or runtime-affecting configuration becomes necessary, the mission is blocked.

## Acceptance Criteria

1. `TODO.md` is present under the active worktree's repo root when this mission is complete, and no other files are added inside the repository worktree by this mission.
2. `TODO.md` contains a `Reviewed Files` section that lists the exact repo-relative authoritative files inspected during the run and separately lists any changed worktree proposal copies inspected for those same paths.
3. `TODO.md` contains a `Contradictions` section that covers every path listed in `Reviewed Files` and either lists concrete contradictions with enough artifact references to locate each issue or explicitly states that no contradictions were found in the reviewed file set.
4. `TODO.md` contains an `Ambiguities` section that covers every path listed in `Reviewed Files` and either lists concrete unclear or underspecified areas with enough artifact references to locate each issue or explicitly states that no ambiguities were found in the reviewed file set.
5. `TODO.md` contains a `Markdown to Script Conversions` section that covers the reviewed file set and either names specific procedures or rules and proposes how each could become an executable script, check, or automation or explicitly states that no such conversion candidates were found.
6. `TODO.md` remains a review artifact describing follow-up tasks only and does not present edits to existing files as completed work.
