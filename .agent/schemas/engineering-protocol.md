# Invariants

## Tests Are Invariants
Semantic modifications or deletions of existing test code must be treated with the same review weight as invariant changes.

# Beliefs

## Prefer Scripts for Deterministic Logic
Deterministic tasks that demand no LLM capability (e.g. linting, formatting, git ops) should be converted into scripts.

# Considerations

## Prefer Automated Tests over Prose Rules
Where possible, use automated tests to express invariants.

## Governance Persistence
Persist new invariants, beliefs, and considerations only when a reviewed mission explicitly promotes them into the relevant governance artifact.
