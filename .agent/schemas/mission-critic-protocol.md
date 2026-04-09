# Invariants

## Structural Completeness
Reject any mission that omits `Scope` (with both `In scope` and `Out of scope` subsections) or `Acceptance Criteria`.

## Mission Justification
Each mission must either
(a) propose at least one new/modified/removed governance artifact
(b) include a consideration about violation-resolution

## Violation-Resolution Specificity
When a consideration claims to resolve an existing violation, it must name both the governance artifact and the violation.

## Governance Artifact Vetting
Each proposed governance artifact (and every part thereof) must be challenged against the content & disqualification clauses defined by `governance-schema.md`.

## Acceptance Criteria Rigor
Each AC must be independently verifiable - a reviwer cna determine pass/fail by examine deliverables alone, with no additional explanation needed.

## AC-Scope Traceability
Each in-scope item must trace to at least one AC. Each AC must trace to at least one in-scope item.

## AC-Governance Traceability
Each AC must trace to at least one governance artifact. 

## Governance Artifact Persistence
Each governance artifact, except explicitly exempted considerations, must have a corresponding AC for its persistence.

## Consideration Persistence Evaluation
Each proposed consideration must be evaluated of its lasting governance value beyond the mission.
It must be persisted if such value exists, or must otherwise be exempted for its persistence.

## Persistence AC Specificity
Except for hard constraints persisted as tests, each persistence AC must name the artifact title, the target document, and the matching top-level section.

## Governance Artifact Completeness
Proposed governance artifacts must present full text.

## Assumption Validity
Reject any assumptions that
(a) are verifiable during Mission Creation
(b) do not serve as a precondition to the mission
(c) carries governance value beyond the mission

## TDD Exemption Validation
Reject if TDD Exemption is declared but an in-scope item is testable.

## Fast-Path Eligibility
All criteria must be met
- No more than one governed artifact change
- No consideration overrides
- Scope <5 files

# Considerations

## Inevident Exclusions
Out-of-scope items without stated or obvious reasons may signal unexamined scope boundaries.

## Scope Creep Through Ambiguity
Challenge each in-scope item's boundary to be concrete enough.

## Test Feasibility
When a hard constraint's persistence AC is by test, challenge the feasibility.

## Persisting Hard Constraint as Test
Hard constraints' preferred form of persistence are automated tests. Challenge any proposed text persistence for hard constraints, if an automated test is viable.