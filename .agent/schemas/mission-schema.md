# Invariants

## Mission Template
Copy `.agent/templates/mission.md` to the target path and fill in the placeholders.

## Delivery Mode
Each mission must declare exactly one delivery mode: `TDD`, `TDD-exempt`, or `Test-Only`.

## Test-Only Scope Qualification
When the delivery mode is `Test-Only`, every proposed invariant or external constraint must explicitly identify itself as `Already-Satisfied Behavior` and must not declare `_persist: <governed-document>_`.

## Full Texts for Governance Artifacts
For new or updated governance artifacts and templates, full proposed text must be presented in the mission section that matches the artifact's category: invariants in `## Invariants`, external constraints in `## External Constraints`, considerations (including template proposals per `governance-schema.md` `## Template Files` and any violation-resolution consideration required by `mission-critic-protocol.md` `## Mission Justification`) in `## Considerations`.

## Assumptions Contents
Assumptions must materially enable, shape, or constrain the mission. They must not be verifiable during Mission Creation.

## Prefer Fast Path
Submit for fast-path approval if either of the following is true:
- The delivery mode is `Test-Only`.
- We modify or remove at most three governed artifacts and do not override considerations.

## Stubbing Policy
Each `TDD` or `Test-Only` mission must declare, under mission.md's `## Considerations` section, a `_transient_` consideration whose body establishes the stubbing policy for the mission. The body must be either an unambiguous policy permitting no stubbing, or an enumerated allowlist of the symbols a test may replace with a mock, stub, fake, or spy (an empty allowlist permits none).

## Runtime-Patching Policy
Each `TDD` or `Test-Only` mission must declare, under mission.md's `## Considerations` section, a `_transient_` consideration whose body establishes the runtime-patching policy for the mission. The body must be either an unambiguous policy permitting no runtime patching, or an enumerated allowlist of the modules, classes, functions, attributes, or constants a test may mutate, replace, or rebind at runtime (an empty allowlist permits none).

## Governance Artifact Persistence
Each governance artifact proposed for addition or modification in a mission may end with a trailing italics line declaring its persistence:
- `_transient_` — the artifact applies during the mission but is not persisted afterward.
- `_persist: <governed-document>_` — the artifact is persisted as a prose rule in the named governed document.

Invariants and External Constraints without such a trailing line default to test persistence. A Consideration without such a trailing line is `_transient_` by default; it may declare `_persist: <governed-document>_` only when its lasting governance value beyond the mission is self-evident from the rule's own text. Considerations cannot be persisted as tests.

## Persistence Declared, Not Justified
A governance artifact of any category — Invariant, External Constraint, or Consideration — proposed for addition or modification in a mission must not include a clause whose purpose is to justify its persistence disposition: that it persists, that it is `_transient_`, or that it is persisted as a prose rule rather than as a test.
