# Invariants

## Governance Scope
This command applies only during governance audits.

## TODO Lifecycle
`TODO.md` is a transient governance-audit artifact. Before deleting `TODO.md` from the active worktree root, the active `mission.md` must account for every concrete item listed under `Contradictions`, `Ambiguities`, and `Markdown to Script Conversions` by either addressing it through a proposed governance artifact or explicitly naming it under `Out of scope`.

## Review Surface Discovery
Always include repo-root `CLAUDE.md`. Include repo-root `AGENTS.md` if it exists. Include every Markdown file directly inside repo-root `.agent/schemas/`. Include every Markdown file directly inside repo-root `.claude/commands/`. Do not recurse into nested subdirectories.

## Worktree Proposal Detection
If any path discovered by the review surface rule also has a changed worktree copy in the active worktree, inspect that changed worktree copy as a proposal while still treating the repo-root copy as authoritative.

## Deliverable
Create or overwrite `TODO.md` at the active worktree's repo root. No other files may be added inside the repository worktree by this command.

## Deliverable Structure
`TODO.md` must contain:
1. A `Contradictions` section covering every reviewed path, listing concrete contradictions with artifact references or explicitly stating none were found.
2. An `Ambiguities` section covering every reviewed path, listing concrete unclear or underspecified areas with artifact references or explicitly stating none were found.
3. A `Markdown to Script Conversions` section naming specific procedures and proposing how each could become an executable script, check, or automation, or explicitly stating no candidates were found.

## Read-Only
This command must not modify any existing repository file except overwriting `TODO.md` if it already exists.

## TDD Exemption
This command is TDD-exempt because every deliverable is a non-executable Markdown artifact.

# Considerations

## C4 — Meta Governance vs External Constraints
This harness supports SDLCs for itself and for other target repos. The External Constraints category in `governance-schema.md` exists for target repos to use. This harness itself cannot have External Constraints, so the Meta Governance invariant in `CLAUDE.md` is correct and non-contradictory with the schema definition.
