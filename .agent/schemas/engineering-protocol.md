# Invariants

## Governing Scope
This document governs engineering behavior for the target repo, including this harness only when it is the target repo. Its rules must not be written or interpreted as harness-specific unless that scope is stated explicitly.

## Tests Are Hard Constraints
They must either express an invariant or external constraint.
Unless explicitly anchored to a named source and version, tests are regarded as invariants.
Semantic modifications or deletions of existing test code must be reviewed with the same rigor as changes to such constraints.

# Beliefs

## Prefer Scripts for Deterministic Logic
When the target repo requires a deterministic task that demands no LLM capability and is expected to recur, require reviewable output, or otherwise benefit from repeatability (e.g. linting, formatting, git ops), prefer converting it into a script unless keeping it as an ad hoc command is clearly lower-maintenance.

# Considerations

## Prefer Automated Tests over Prose Rules
Where possible, use automated tests to express invariants.

## Governance Persistence
Persist new invariants, beliefs, and considerations only when a reviewed mission explicitly promotes them into the relevant governance artifact.
