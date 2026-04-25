# Invariants

## Structural Completeness
Reject any mission that omits `Delivery Mode`.

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

## Governance Artifact Persistence
Reject any proposed consideration that lacks a `_transient_` or `_persist: <governed-document>_` declaration.

## Consideration Persistence Evaluation
Each proposed consideration must be evaluated of its lasting governance value beyond the mission.
It must be persisted if such value exists, or must otherwise be exempted for its persistence.

## Governance Artifact Completeness
Proposed governance artifacts must present full text.

## Assumption Validity
Reject any assumptions that
(a) are verifiable during Mission Creation
(b) do not serve as a precondition to the mission
(c) carries governance value beyond the mission

## TDD Exemption Validation
Reject if `TDD-exempt` is declared but any proposed invariant or external constraint defaults to (or declares) test persistence.

## Test-Only Validation
Reject if `Test-Only` is declared and any proposed invariant or external constraint is not explicitly qualified as `Already-Satisfied Behavior`.

## Fast-Path Eligibility
When the review context explicitly identifies the mission as fast-path and the delivery mode is not `Test-Only`, all criteria must be met:
- No more than one governed artifact change
- No consideration overrides

## Stubbing and Runtime-Patching Policy Declaration
For missions whose delivery mode is `TDD` or `Test-Only`, reject unless the mission's `## Invariants` section declares a stubbing-policy invariant and a runtime-patching-policy invariant (titles need not match specific strings, but each invariant must be unambiguous about which policy it establishes). Each such invariant's body must be either an unambiguous blanket ban or an enumerated allowlist.

# Considerations

## Inevident Exclusions
Out-of-scope items without stated or obvious reasons may signal unexamined scope boundaries.

## Test Feasibility
When a hard constraint defaults to or declares test persistence, challenge the feasibility.

## Persisting Hard Constraint as Test
Invariants' and external constraints' preferred form of persistence are automated tests. Challenge any proposed text persistence for them, if an automated test is viable.
