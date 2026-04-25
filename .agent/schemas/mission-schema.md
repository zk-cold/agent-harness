# Invariants

## Mission Template
Copy `.agent/templates/mission.md` to the target path and fill in the placeholders.

## Delivery Mode
Each mission must declare exactly one delivery mode: `TDD`, `TDD-exempt`, or `Test-Only`.

## Test-Only Scope Qualification
When the delivery mode is `Test-Only`, every in-scope item must explicitly identify itself as `Already-Satisfied Behavior`.

## Full Texts for Governance Artifacts
For new or updated governance artifacts and templates, full proposed text must be presented in their respective optional sections.

## Assumptions Contents
Assumptions must materially enable, shape, or constrain the mission. They must not be verifiable during Mission Creation.

## Acceptance Criteria
ACs must be objectively-verifiable, unambigous, specific, and traceable to at least one governance artifact.


## AC and Scope Mapping
Each in-scope item must derive at least 1 AC. Each AC must govern at least one in-scope item.


## Prefer Fast Path
Submit for fast-path approval if either of the following is true:
- The delivery mode is `Test-Only`.
- We propose/remove/modify at most one governed artifact, do not override considerations, and have fewer than 5 files in scope.

## Stubbing Policy
Each `TDD` or `Test-Only` mission must declare, under mission.md's `## Invariants` section, an invariant whose body establishes the stubbing policy for the mission. The body must be either an unambiguous blanket ban, or an enumerated allowlist of the symbols a test may replace with a mock, stub, fake, or spy (an empty allowlist permits none).

## Runtime-Patching Policy
Each `TDD` or `Test-Only` mission must declare, under mission.md's `## Invariants` section, an invariant whose body establishes the runtime-patching policy for the mission. The body must be either an unambiguous blanket ban, or an enumerated allowlist of the modules, classes, functions, attributes, or constants a test may mutate, replace, or rebind at runtime (an empty allowlist permits none).

## AC Behavioral Scope
An Acceptance Criterion must not originate a runtime behavior requirement for a deliverable's shipped production code (e.g. inputs/outputs, state transitions, error handling, observable side effects). Any such requirement must first be captured as an invariant or external constraint, and the AC may only verify the persistence or satisfaction of that invariant or external constraint. ACs that assert on build, test, or process tooling (e.g. test pass/fail, coverage thresholds, linter results) are out of this rule's scope.
