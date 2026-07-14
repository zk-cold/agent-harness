# Invariants

## Structural Completeness
Reject any mission that omits `Delivery Mode`.

## Delivery Mode Validation
Reject if the mission declares zero, multiple, or unsupported delivery modes.

## Mission Justification
Each mission must either
(a) propose at least one new/modified/removed governance artifact
(b) include a consideration about violation-resolution

## Governance Artifact Persistence
Treat a proposed consideration that carries no persistence declaration as `_transient_`. Reject a consideration that declares `_persist: <governed-document>_` when its lasting governance value beyond the mission is not self-evident from the rule's own text.

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
When invoked via the `Fast-Path Mission Creation Critic` prompt template and the delivery mode is not `Test-Only`, all criteria must be met:
- No more than three governance artifact modifications or removals
- No consideration overrides

## Stubbing and Runtime-Patching Policy Declaration
For missions whose delivery mode is `TDD` or `Test-Only`, reject unless the mission's `## Considerations` section declares a stubbing-policy consideration and a runtime-patching-policy consideration (titles need not match specific strings, but each consideration must be unambiguous about which policy it establishes). Each such consideration must carry a `_transient_` persistence declaration, and its body must be either an unambiguous policy permitting none or an enumerated allowlist.

## Persistence Declared, Not Justified
Reject any proposed governance artifact, of any category, that includes a clause whose purpose is to justify its persistence disposition — that it persists, that it is `_transient_`, or that it is persisted as a prose rule rather than as a test.

# Considerations

## Inevident Exclusions
Out-of-scope items without stated or obvious reasons may signal unexamined scope boundaries.

## Test Feasibility
When a hard constraint defaults to or declares test persistence, challenge the feasibility.

## Persisting Hard Constraint as Test
Invariants' and external constraints' preferred form of persistence are automated tests. Challenge any proposed text persistence for them, if an automated test is viable.
