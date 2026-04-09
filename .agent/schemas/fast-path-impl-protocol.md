# Invariants

## Governance Scope
This document does not apply to any sub-agents.

## Escalation
Whenever fast-path assumption no longer stands, escalate to normal flow.

## Leave Changes Uncommitted
All changes must remain uncommitted.

## TDD Flow
Execute below steps in order unless the mission is TDD exempted:
1. Writing tests - follow `sdet-protocol.md` as an SDET
2. Verification against `sdet-protocol.md` - once locked, no further additions/modifications/deletions
3. Follow `sde-protocol.md` as an SDE

# Considerations
## Fast-Path Validation Timing
1. Fail fast whenever we have to override a consideration
2. Upon creating/modifying/removing a new file, verify the file count criteria