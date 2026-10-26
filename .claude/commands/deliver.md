# Invariants

## Delivery Loop
1. The target repo is the one the user names, otherwise the git repo of the working directory. If it has uncommitted changes, ask the user how to proceed. Otherwise, spawn an `impl` agent with the target repo path and the user's request verbatim.
2. When it finishes, spawn fresh `earn-its-place-critic`, `alignment-critic`, and `full-review-critic` agents in parallel. Their prompts contain only the target repo path.
3. If any critic rejects, send every rejection to the same `impl` agent and return to step 2 once it finishes. After five rejecting critic responses in total, judge each later rejection first and dismiss any you do not uphold.
4. When every critic approves or has its rejection dismissed, apply the target repo's commit rules (default: commit only) and present the result, with each dismissed rejection and why, to the user.
