# Invariants

## Terms
Use the definitions in `.agent/schemas/governance-schema.md`.

## Roadmap Item
Each delivery corresponds to exactly one item on the roadmap that the target repo's governance designates. Once step 1's checks pass and before dispatching any of the user's request, find the item whose request it is, otherwise add one holding it verbatim, and close any other item duplicating it. If the request slices an item, split that item into sub-items that together cover its request, this one among them.

## Removing Worktrees
Remove an `impl` agent's worktree and branch once its branch is merged or Abort or Replace is chosen.

## Delivery Loop
1. If the target repo's governance designates no roadmap or backend, or the target repo has uncommitted changes or is not on its root branch, ask the user how to proceed. Otherwise, spawn an `impl` agent with the target repo path, its root branch, the delivery's roadmap item, and the user's request verbatim.
2. When it finishes, have its work reviewed by one critic at a time, cycling through `earn-its-place-critic`, `alignment-critic`, and `full-review-critic` in that order. Each review is by a fresh agent whose prompt contains only the path of the `impl` agent's worktree and the root branch. Any change to the `impl` agent's work voids every approval.
3. If a critic rejects, send its rejection grounds to the `impl` agent, requiring it to run the tests before finishing once any `earn-its-place-critic` has ever approved its work, and once it finishes, have the same critic review again before proceeding to the next. For each rejection, and each `NOT READY` verdict in step 4, beyond the fifth in total, first make one choice yourself among:
   - Abort, when the agents cannot resolve it well among themselves: stop, close the sub-items `impl` agents added to the delivery's roadmap item, work out a more viable objective, such as a slice of the request, with the user, and record it on the roadmap, splitting a sliced item as `## Roadmap Item` does, otherwise rewriting or closing the item as agreed.
   - Replace, e.g. for an obvious invariant breach or oscillating findings: close the sub-items Abort closes and send any rejection grounds to a fresh `impl` agent spawned as in step 1.
   - Continue.
4. When all three approvals stand, send the `impl` agent each finding from those reviews and tell it all three approvals stand, requiring it to run the tests unless it already has since its last change, and return to step 2 unless its verdict is `READY`. Then, following the target repo's commit rules, require it to commit, merge its branch into the root branch yourself once it has, and complete the sub-items of its handled findings, then its roadmap item. Present the result, with its unhandled findings, to the user, and for each unhandled finding that warrants follow-up work, add a roadmap item holding it.
