# Invariants

## Tests Are Hard Constraints
Semantic modifications or deletions of existing test code must be reviewed with the same rigor as changes to such constraints.

## Documentation for External Constraints
Tests expressing external constraints must satisfy the same anchor requirements set out by `governance-schema.md`.

## Hard Constraint Coverage
Every testable invariant or external constraint must have a corresponding test.

## New Test Purpose
Each new test must express an identified invariant or external constraint.

## Test-Only Qualification
When the mission delivery mode is `Test-Only`, each new or modified test must map to a proposed invariant or external constraint explicitly qualified as `Already-Satisfied Behavior`.
