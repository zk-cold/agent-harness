# Invariants

## Delivery Loop
1. If the target repo has uncommitted changes, ask the user how to proceed. Otherwise, spawn an `impl` agent with the user's request verbatim.
2. When it finishes, spawn fresh `earn-its-place-critic`, `alignment-critic`, and `full-review-critic` agents in parallel. Their prompts contain only the target repo path.
3. If any critic rejects, send every rejection to the same `impl` agent and return to step 2 once it finishes.
4. When all three approve, apply the target repo's commit rules (default: commit only) and present the result to the user.
