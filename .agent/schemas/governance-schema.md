# Definitions

## Governed Documents
`AGENTS.md`, `.agent/schemas/*.md`, `.claude/commands/*.md`, and `.claude/agents/*.md` in this harness and the target repo.

## This Harness
The directory whose `.agent/schemas/` holds this file.

## `${CLAUDE_PLUGIN_ROOT}`
This harness.

## Categories
- Definitions: meanings of terms, containing no rules.
- Invariants: always-binding rules.
- Considerations: default-binding rules.

## Target Repo
The repo the prompt identifies, other than as `${CLAUDE_PLUGIN_ROOT}`, including by one of its worktrees, otherwise the working directory's repo.

## Root Branch
The target repo's branch the prompt names, otherwise its default branch.

# Invariants

## Path Resolution
`.agent/` paths in this harness's governed documents resolve against this harness.

## Document Structure
Each section of a governed document must hold only its category's content.

## One Rule Per Section
Each Invariants or Considerations section must hold exactly one rule, an ordered procedure counting as one.

## Overriding Considerations
A consideration may be overridden only by explicitly referencing it with a justification that withstands adversarial review.

## No Conflicting Governance
Target repo governance must not conflict with this harness's definitions or invariants.

## Binding Version
Governance binds as it stands in the working tree.
