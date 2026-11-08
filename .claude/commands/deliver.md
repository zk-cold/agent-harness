---
description: Delivers a request through the impl and critic loop.
---
# Invariants

## Terms
Use the definitions in `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/governance-schema.md` and `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/roadmap.md`.

## Roadmap Item
Each delivery corresponds to exactly one item on the roadmap: once step 1's checks pass and before dispatching any of the user's request, find the item whose request it is, otherwise add one holding it verbatim.

## Duplicate Items
Once step 1's checks pass and before dispatching any of the user's request, close any other item duplicating the delivery's roadmap item.

## Sliced Items
If the request slices an item, split that item into sub-items that together cover its request, the delivery's roadmap item among them.

## Removing Worktrees
Remove an `impl` agent's worktree and branch once its branch is merged or Abort or Replace is chosen.

## Voided Approvals
Any change to the `impl` agent's work, other than a conflict-free merge of the root branch into its branch, voids every approval.

## Delivery Loop
1. If the target repo's governance designates no roadmap or backend, or the target repo has uncommitted changes or is not on its root branch, ask the user how to proceed. Otherwise, spawn an `impl` agent with the target repo path, its root branch, the delivery's roadmap item, and the user's request verbatim.
2. When it finishes, have its work reviewed by `earn-its-place-critic`, then `alignment-critic`, then `full-review-critic`, one at a time. Each review is by a fresh agent whose prompt contains only the path of the `impl` agent's worktree and the root branch, and its verdict is what its response's first line states, otherwise the review fails and is repeated.
3. If a critic rejects, send its agent ID to the `impl` agent, requiring it to run the tests before finishing once any `earn-its-place-critic` has ever approved its work, and once it finishes, return to step 2. For each rejection, failed review, and each `NOT READY` verdict in step 4 not reported for its sub-step 3, beyond the fifth in total, first make one choice yourself among:
   - Abort, when the agents cannot resolve it well among themselves: stop, close the sub-items `impl` agents added to the delivery's roadmap item (found by listing its descendants), work out a more viable objective, such as a slice of the request, with the user, and record it on the roadmap, splitting a sliced item as `## Sliced Items` does, otherwise rewriting or closing the item as agreed.
   - Replace, e.g. for an obvious invariant breach or oscillating findings: close the sub-items Abort closes and send any rejecting critic's agent ID to a fresh `impl` agent spawned as in step 1.
   - Continue.
4. When all three approvals stand, send the `impl` agent the approving critics' agent IDs and tell it all three approvals stand, requiring it to run the tests unless it already has since its last change. Then, following the target repo's rules, repeat the sub-steps below until its branch is merged into the root branch, and complete the sub-items of its handled findings (found by listing its roadmap item's descendants), then its roadmap item. Present the result, with its unhandled findings, to the user, and for each unhandled finding that warrants follow-up work, add a roadmap item holding it.
   1. Return to step 2 yourself unless its verdict is `READY`.
   2. Require it to commit.
   3. If its branch holds the root branch's tip, merge it into the root branch yourself. Otherwise, require it to merge the root branch into its branch, resolving any conflict and committing the merge, and run the tests and `${CLAUDE_PLUGIN_ROOT}/.agent/scripts/check` on its worktree, fixing any failure.
