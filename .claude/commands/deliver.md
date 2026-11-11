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

## Delivery Loop
1. If the target repo's governance designates no roadmap or backend, `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` is not at least 2, or the target repo has uncommitted changes or is not on its root branch, ask the user how to proceed. Otherwise, settle with the user each question the request leaves open, recording the answers on the delivery's roadmap item, then spawn an `impl` agent with the target repo path, its root branch, the delivery's roadmap item, and the user's request verbatim.
2. When it reports, if its verdict is `READY`, its worktree is clean, `${CLAUDE_PLUGIN_ROOT}/.agent/scripts/review approved <its worktree> <root branch> <its approvals>` accepts, and, following the target repo's rules, you merge its branch into the root branch without conflict, complete the sub-items of its handled findings (found by listing its roadmap item's descendants), then its roadmap item, present the result, with its unhandled findings, to the user, and for each unhandled finding that warrants follow-up work, add a roadmap item holding it. Otherwise, abort any conflicting merge and make one choice yourself among:
   - Abort, when the agents cannot resolve it well among themselves: stop, close the sub-items `impl` agents added to the delivery's roadmap item (found by listing its descendants), work out a more viable objective, such as a slice of the request, with the user, and record it on the roadmap, splitting a sliced item as `## Sliced Items` does, otherwise rewriting or closing the item as agreed.
   - Replace, e.g. for an obvious invariant breach or oscillating rejection grounds: close the sub-items Abort closes and send its escalation, if any, to a fresh `impl` agent spawned as in step 1.
   - Continue: require it to continue, sending it any rejection by that command or conflict.
