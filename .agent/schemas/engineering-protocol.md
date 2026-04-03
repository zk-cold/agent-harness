# Invariants

## Existing Test Changes Carry Invariant-Level Review Weight
When review or fast-path eligibility depends on whether a proposal changes governed behavior, modifications or deletions of existing test code must be treated with the same review weight as invariant changes. Violation: a mission or review treats a modification or deletion of existing test code as still eligible for lite fast-path review, or applies a lower review bar than an invariant change would require.

# Beliefs

## Prefer Scripts for Deterministic Logic
Deterministic tasks that demand no LLM capability (e.g. linting, formatting, git ops) should be converted into scripts.

# Considerations

## Prefer Automated Tests over Prose Rules
Where possible, use automated tests to express invariants.

## Governance Persistence
Persist new invariants, beliefs, and considerations only when a reviewed mission explicitly promotes them into the relevant governance artifact.
