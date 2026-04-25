# Invariants

## Structural Completeness
Reject any mission that omits `Delivery Mode`, `Scope` (with both `In scope` and `Out of scope` subsections), or `Acceptance Criteria`.

## Delivery Mode Validation
Reject if the mission declares zero, multiple, or unsupported delivery modes.

## Mission Justification
Each mission must either
(a) propose at least one new/modified/removed governance artifact
(b) include a consideration about violation-resolution

## Violation-Resolution Specificity
When a consideration claims to resolve an existing violation, it must name both the governance artifact and the violation.

## Governance Artifact Vetting
Each proposed governance artifact (and every part thereof) must be challenged against the content & disqualification clauses defined by `governance-schema.md`.

## Acceptance Criteria Rigor
Each AC must be independently verifiable - a reviewer can determine pass/fail by examining deliverables alone, with no additional explanation needed.

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
Reject if `TDD-exempt` is declared but an in-scope item is testable.

## Test-Only Validation
Reject if `Test-Only` is declared and any in-scope item:
(a) requires prod-scope code changes
(b) is not explicitly qualified as `Already-Satisfied Behavior`

## Fast-Path Eligibility
When the review context explicitly identifies the mission as fast-path and the delivery mode is not `Test-Only`, all criteria must be met:
- No more than one governed artifact change
- No consideration overrides
- Scope <5 files

## AC Behavioral Scope
Reject any AC that originates a runtime behavior requirement for a deliverable's shipped production code (e.g. inputs/outputs, state transitions, error handling, observable side effects) instead of verifying persistence or satisfaction of an invariant or external constraint that captures that behavior. ACs asserting on build, test, or process tooling are out of this rule's scope.

## Stubbing and Runtime-Patching Policy Declaration
For missions whose delivery mode is `TDD` or `Test-Only`, reject unless the mission's `## Invariants` section declares a stubbing-policy invariant and a runtime-patching-policy invariant (titles need not match specific strings, but each invariant must be unambiguous about which policy it establishes). Each such invariant's body must be either an unambiguous blanket ban or an enumerated allowlist.

# Considerations

## Inevident Exclusions
Out-of-scope items without stated or obvious reasons may signal unexamined scope boundaries.

## Scope Creep Through Ambiguity
Challenge each in-scope item's boundary to be concrete enough.

## Test Feasibility
When a hard constraint's persistence AC is by test, challenge the feasibility.

## Persisting Hard Constraint as Test
Hard constraints' preferred form of persistence are automated tests. Challenge any proposed text persistence for hard constraints, if an automated test is viable.
