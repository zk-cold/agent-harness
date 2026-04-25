# Invariants

## Governance Scope
This document does not apply to any sub-agents.

## Escalation
Whenever fast-path assumption no longer stands, escalate to normal flow.

## Leave Changes Uncommitted
All changes must remain uncommitted.

## Delivery Mode Flow
Execute the applicable flow below in order:
1. If the mission delivery mode is `TDD`:
   a. Writing tests - follow `sdet-protocol.md` as an SDET
   b. Verification against `sdet-protocol.md` - once locked, no further additions/modifications/deletions
   c. Follow `sde-protocol.md` as an SDE
2. If the mission delivery mode is `TDD-exempt`, follow `sde-protocol.md` as an SDE
3. If the mission delivery mode is `Test-Only`:
   a. Writing tests - follow `sdet-protocol.md` as an SDET
   b. Verification against `sdet-protocol.md` - once locked, no further additions/modifications/deletions
   c. Run the relevant tests and write their raw output to `test-output.txt`
   d. If the target repo provides a formatter and/or linter, run them, ensure clean results, and write the raw output to `lint-output.txt`
   e. If coverage verification is explicitly required by the mission or target-repo governance, run it and write the raw output to `coverage-output.txt`

## Fail-Fast on Governance Breach
If completing the mission would breach a governance artifact not amended or overridden by the approved mission, halt and follow `abort-protocol.md`.

# Considerations
## Fast-Path Validation Timing
Upon creating/modifying/removing a new file, verify the file count criteria.
