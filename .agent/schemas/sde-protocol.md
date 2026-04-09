# Invariants

## Governance Scope
This document only applies to SDEs.

## No Modification to Tests
Do not create, modify, or delete any test.

## Final Verifications
Before reporting ready-for-review:
1. Run the coverage tool for new/modified code. Verify coverage threshold is met. 
2. If the target repo provides a formatter and/or linter, run them and ensure clean results
3. Fetch and merge from target repo's latest root branch
4. Verify all Acceptance Criteria is met
The raw output from tests, coverage, and linter(if available) must be written to dedicated files under worktree root.

## Refactoring Justification
Refactor only if an Acceptance Criteria cannot be met without such refactoring. 

## Governance Persistence
Persist governance artifacts as prose rules only if such persistence is in the Acceptance Criteria.