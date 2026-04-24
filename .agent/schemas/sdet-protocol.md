# Invariants

## Governance Scope
This document only applies to SDETs.

## No Prod-Scope Code
Do not create, modify, or delete any prod-scope code, unless it's an API change made explicit in the mission.

## No Governed Document Changes
Do not create, modify, or delete any governed document by `governance-schema.md`.

## TDD Fail-on-write
When the mission delivery mode is `TDD`, and unless made explicit in the mission that the invariant or external constraint is already satisfied, its corresponding test(s) must fail.

## Test-Only Boundaries
When the mission delivery mode is `Test-Only`, every new or modified test must map to an in-scope item explicitly qualified as `Already-Satisfied Behavior`.

## Test Every Testable Hard Constraint
Each invariant or external constraint that's in-scope for persistence as test must be expressed by at least one test(s).

## Test Only Hard Constraints
Each test must express at least one (or part of) invariant or external constraint.

## Document External Constraints
Each external constraint must be documented of the same anchor info specified by `governance-schema.md`.

## Fail-Fast on Governance Breach
If completing the mission would breach a governance artifact not amended or overridden by the approved mission, halt and surface the blocker in the response to the lead.
