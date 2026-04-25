# Invariants

## Mission Template
Copy `.agent/templates/mission.md` to the target path and fill in the placeholders.

## Delivery Mode
Each mission must declare exactly one delivery mode: `TDD`, `TDD-exempt`, or `Test-Only`.

## Test-Only Scope Qualification
When the delivery mode is `Test-Only`, every invariant or external constraint that the mission proposes for test persistence must explicitly identify itself as `Already-Satisfied Behavior`.

## Full Texts for Governance Artifacts
For new or updated governance artifacts and templates, full proposed text must be presented in their respective optional sections.

## Assumptions Contents
Assumptions must materially enable, shape, or constrain the mission. They must not be verifiable during Mission Creation.

## Prefer Fast Path
Submit for fast-path approval if either of the following is true:
- The delivery mode is `Test-Only`.
- We propose/remove/modify at most one governed artifact and do not override considerations.

## Stubbing Policy
Each `TDD` or `Test-Only` mission must declare, under mission.md's `## Invariants` section, an invariant whose body establishes the stubbing policy for the mission. The body must be either an unambiguous blanket ban, or an enumerated allowlist of the symbols a test may replace with a mock, stub, fake, or spy (an empty allowlist permits none).

## Runtime-Patching Policy
Each `TDD` or `Test-Only` mission must declare, under mission.md's `## Invariants` section, an invariant whose body establishes the runtime-patching policy for the mission. The body must be either an unambiguous blanket ban, or an enumerated allowlist of the modules, classes, functions, attributes, or constants a test may mutate, replace, or rebind at runtime (an empty allowlist permits none).

## Governance Artifact Persistence
Each governance artifact proposed for addition or modification in a mission must end with a trailing italics line declaring its persistence:
- `_transient_` — the artifact applies during the mission but is not persisted afterward.
- `_persist: <governed-document>_` — the artifact is persisted as a prose rule in the named governed document.

Invariants and External Constraints without such a trailing line default to test persistence. Considerations cannot be persisted as tests; they must declare either `_transient_` or `_persist: <governed-document>_` explicitly.
