# Invariants

## Governance Scope
This document only applies to SDETs.

## No Prod-Scope Code
Do not create, modify, or delete any prod-scope code, unless it's an API change made explicit in the mission.

## No Governed Document Changes
Do not create, modify, or delete any governed document by `governance-schema.md`.

## Fail-on-write
Unless made explicit in the mission that the hard constraint is already satisfied, its corresponding test(s) must fail.

## Test Every Testable Hard Constraint
Each hard constraint that's in-scope for persistence as test must be expressed by at least one test(s).

## Test Only Hard Constraints
Each test must express at least one (or part of) hard constraint.

## Document External Constraints
Each external constraint must be documented of the same anchor info specified by `governance-schema.md`.