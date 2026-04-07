# Invariants

## Governing Scope
This document governs engineering behavior for the target repo, including this harness only when it is the target repo. Its rules must not be written or interpreted as harness-specific unless that scope is stated explicitly.

## Tests Are Hard Constraints
They express the hard constraint by the behavior they test.
Unless explicitly anchored to a named source and version, tests are regarded as invariants.
Semantic modifications or deletions of existing test code must be reviewed with the same rigor as changes to such constraints.

## Existing Violations
A failing test is an existing violation of the invariant or external constraint that the test expresses.
An implementation that does not satisfy an existing belief is an existing violation unless an explicit override is documented as a consideration in mission.md and subsequently persisted.
An existing consideration may be cited to identify, explain, or trace an existing violation, but it does not become a hard constraint solely by being cited.

## Refactoring Justification
Refactoring is allowed only when necessary to satisfy or when it directly supports at least one existing or newly introduced governing artifact. Refactoring without such justification is not allowed.

## New Test Purpose
Each new test must express an identified invariant or external constraint. Tests must not be written solely for coverage.

## Governance Persistence
Persist new invariants, beliefs, and considerations only when a reviewed mission explicitly promotes them into the relevant governance artifact.

# Beliefs

## Prefer Scripts for Deterministic Logic
When the target repo requires a deterministic task that demands no LLM capability and is expected to recur, require reviewable output, or otherwise benefit from repeatability (e.g. linting, formatting, git ops), prefer converting it into a script unless keeping it as an ad hoc command is clearly lower-maintenance.
This belief does not require deterministic linting for mission or governance prose when correct evaluation depends on natural-language interpretation. In that case, a script may still be used for structured capture or editing convenience without acting as the approval gate.
Deterministic prose checks that require no semantic judgment (e.g., heading validation, required-section presence) are not natural-language interpretation and should be scripted.

# Considerations

## Prefer Automated Tests over Prose Rules
Where possible, use automated tests to express invariants.
