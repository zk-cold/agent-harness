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

The raw output from tests, coverage, and linter (if available) must be written to fixed files under worktree root: `test-output.txt`, `coverage-output.txt`, and `lint-output.txt` respectively.

## Refactoring Justification
Refactor only if an Acceptance Criteria cannot be met without such refactoring. 

## Governance Persistence
Persist governance artifacts as prose rules only if such persistence is in the Acceptance Criteria.

## Fail-Fast on Governance Breach
If completing the mission would breach a governance artifact not amended or overridden by the approved mission, halt and surface the blocker in the response to the lead.
