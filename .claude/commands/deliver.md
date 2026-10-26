# Invariants

## Terms
Use the definitions in `.agent/schemas/governance-schema.md`.

## Roadmap Item
Each delivery corresponds to exactly one item on the roadmap that the target repo's governance designates. Once step 1's checks pass and before dispatching any of the user's request, find the item whose request it is, otherwise add one holding it verbatim, and close any other item duplicating it. If the request slices an item, split that item into sub-items that together cover its request, this one among them.

## Delivery Loop
1. If the target repo's governance designates no roadmap, or the target repo has uncommitted changes or is not on its root branch, ask the user how to proceed. Otherwise, spawn an `impl` agent with the target repo path, its root branch, and the user's request verbatim.
2. When it finishes, spawn fresh `earn-its-place-critic`, `alignment-critic`, and `full-review-critic` agents in parallel. Their prompts contain only the path of the `impl` agent's worktree and the root branch.
3. If any critic rejects, send the round's rejection grounds together to the `impl` agent, requiring it to run the tests before finishing once any `earn-its-place-critic` has approved its work, and return to step 2 once it finishes. For each round with a rejecting critic response beyond the fifth in total, first make one choice yourself among:
   - Abort, when the agents cannot resolve it well among themselves: stop, work out a more viable objective, such as a slice of the request, with the user, and record it on the roadmap, splitting a sliced item as `## Roadmap Item` does, otherwise rewriting or closing the item as agreed.
   - Replace, where warranted, such as for an obvious invariant breach or oscillating findings: send the round's grounds to a fresh `impl` agent spawned as in step 1 instead.
   - Continue.
4. When every critic approves, require the `impl` agent to run the tests unless it already has since its last change, and return to step 2 if it changes anything. Then, following the target repo's commit rules, require it to commit, merge its branch into the root branch yourself once it has, and close its roadmap item with any sub-items, then each ancestor item once all its sub-items are closed. Present the result, with each finding from the final critic round, to the user.
