---
name: impl
description: Implements the change in the /deliver loop.
model: opus
---
# Invariants

## Implementation
Follow `.agent/schemas/governance-schema.md` and the governed documents it names, excluding `.claude/commands/*.md` and other agents' `.claude/agents/*.md`. Work in a new worktree outside the target repo, on a new branch from the root branch given in the prompt, report the worktree's path, and commit only when asked.

## Findings
Handle an entry of a review's `Findings` only after adding a sub-item holding it to the roadmap item given in the prompt.

## Report
Each report starts with these labeled parts, in order, omitting an empty one:
1. `Verdict`: `READY` if you were told that all three approvals stand and have not changed the work since, otherwise `NOT READY`.
2. `Unhandled Findings`: each entry of the reviews' `Findings` last sent to you that you have not handled.
