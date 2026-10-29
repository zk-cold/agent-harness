# Definitions

## Governed Documents
`CLAUDE.md`, `.agent/schemas/*.md`, `.claude/commands/*.md`, and `.claude/agents/*.md` in this harness and the target repo.

## Categories
- Definitions: meanings of terms, containing no rules.
- Invariants: always-binding rules.
- Considerations: default-binding rules.

## Target Repo
The repo the prompt identifies, including by the path of one of its worktrees, otherwise the git repo of the working directory.

## Root Branch
The target repo's branch the prompt names, otherwise its default branch.

## Roadmap
The roadmap the target repo's governance designates.

## Roadmap Operations
Running `.agent/scripts/roadmap <backend> <target repo path>`, with the roadmap's backend, followed by one of:
- `add <title> <body> [<parent>]`: adding a roadmap item, as a sub-item of `<parent>` if given, and printing its ID.
- `close <item>`: closing an item and its open sub-items as not delivered.
- `complete <item>`: completing an item, closing its open sub-items as not delivered, then completing each ancestor whose sub-items are all closed.
- `edit <item> <title> [<body>]`: replacing an item's title, and its body if given.
- `show <item>`: showing an item, printing only its content written by the target repo's owner, members or collaborators.
- `list`: listing the open items authored by the target repo's owner, members or collaborators.
- `candidates`: listing candidates, the items `list` lists that have no open sub-items.

# Invariants

## Document Structure
`.agent/scripts/check` must accept this harness and the target repo, and each section of a governed document hold only its category's content.

## Overriding Considerations
A consideration may be overridden only by explicitly referencing it with a justification that withstands adversarial review.

## Target Repo Governance
Target repo governance must designate a roadmap and its backend, and not conflict with this harness's definitions or invariants.

## Roadmap Backends
Each `.agent/scripts/roadmap-<backend>` must implement `## Roadmap Operations`.

## Binding Version
Governance binds as it stands in the working tree.
