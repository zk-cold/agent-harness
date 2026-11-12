# Definitions

## Governed Documents
`AGENTS.md`, `.agent/schemas/*.md`, `.claude/commands/*.md`, and `.claude/agents/*.md` in this harness and the target repo.

## This Harness
The directory whose `.agent/schemas/` holds this file, against which `.agent/` paths in its governed documents resolve.

## Categories
- Definitions: meanings of terms, containing no rules.
- Invariants: always-binding rules.
- Considerations: default-binding rules.

## Target Repo
The repo the prompt identifies, including by the path of one of its worktrees, otherwise the git repo of the working directory.

## Root Branch
The target repo's branch the prompt names, otherwise its default branch.

# Invariants

## Document Structure
Each section of a governed document must hold only its category's content.

## One Rule Per Section
Each Invariants or Considerations section must hold exactly one rule, an ordered procedure counting as one.

## Overriding Considerations
A consideration may be overridden only by explicitly referencing it with a justification that withstands adversarial review.

## Target Repo Governance
Target repo governance must not conflict with this harness's definitions or invariants.

## Binding Version
Governance binds as it stands in the working tree.
