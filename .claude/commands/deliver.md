# Invariants

## Lead Protocol
Follow `.agent/schemas/lead-protocol.md`.

## Delivery Loop
1. The target repo is the one the user names, otherwise the git repo of the working directory. Its root branch is the one the user names, otherwise its default branch. If it has uncommitted changes, ask the user how to proceed. Otherwise, switch to a new branch if it is on its root branch, then spawn an `impl` agent with the target repo path and the user's request verbatim.
2. When it finishes, spawn fresh `earn-its-place-critic`, `alignment-critic`, and `full-review-critic` agents in parallel. Their prompts contain only the target repo path and its root branch.
3. If any critic rejects, send every rejection's grounds to the same `impl` agent, requiring it to run the tests before finishing once any `earn-its-place-critic` has approved, and return to step 2 once it finishes. After five rejecting critic responses in total, judge each later rejection first and dismiss any you do not uphold.
4. When every critic approves or has its rejection dismissed, require the same `impl` agent to run the tests unless it already has since its last change, and return to step 2 if it changes anything. Then apply the target repo's commit rules (default: commit, then merge into the root branch) and present the result, with each dismissed rejection and why and each finding from the final critic round, to the user.
