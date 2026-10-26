# Definitions

## Governed Documents
`CLAUDE.md`, `.agent/schemas/*.md`, `.claude/commands/*.md`, and `.claude/agents/*.md` in this harness and the target repo.

## Categories
- **Definitions**: meanings of terms across all governed documents, containing no rules.
- **Invariants**: always-binding rules.
- **Considerations**: default-binding rules.

## Target Repo
The repo the prompt identifies, by name or by the path of the repo or one of its worktrees, otherwise the git repo of the working directory.

## Root Branch
The target repo's branch the prompt names, otherwise its default branch.

## Covered Content
Content git does not ignore in this harness and the target repo, other than `.gitignore` and `LICENSE`.

# Invariants

## Document Structure
After any frontmatter, a governed document consists only of top-level (`#`) sections, each named for a category and holding only that category's content.

## Overriding Considerations
A consideration may be overridden only when it is explicitly referenced and the justification is stated clearly enough to withstand adversarial review.

## Target Repo Governance
Target repo governance must designate a roadmap and must not conflict with this harness's definitions or invariants.

## Binding Version
Governance binds as it stands in the working tree.

## No Unsanctioned Prose
Prose of Covered Content outside governed documents may be written or kept only if governance sanctions it.

## Earn Its Place
A token of Covered Content may be written or kept only if it directly shapes or governs production behavior, it cannot be derived from other content in this harness or the target repo, and the work could not be equal or better without it.
