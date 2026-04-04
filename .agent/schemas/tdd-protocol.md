# Invariants

## Coverage Threshold

The coverage threshold is **>80% line coverage on the code being touched by the mission**. This single definition is the source of truth — no skill file or mission.md may define a conflicting threshold.

This threshold applies in two contexts:

1. **Fast-path eligibility:** the target code must already meet the threshold before execution begins.
2. **TDD baseline**: before the red-green loop begins, coverage on the target code must meet the threshold. If it does not, the agent fills coverage gaps first (see TDD Execution Loop step 3).

## Coverage Tool Requirement

A mission may proceed only when exactly one of the following is true:

- **Coverage tool in scope:** The mission includes setup or configuration of an appropriate coverage tool for the target repo's language as an in-scope deliverable.
- **Coverage tool available:** The target repo already has a working coverage tool, confirmed during interview or early execution.
- **TDD-exempt assumption:** The mission's `Assumptions` section includes the TDD-exempt assumption defined below.

For `/new-sdlc` fast path specifically: if no coverage tool is available and mission.md does not include coverage tool setup as in-scope, the request is ineligible for fast path.

## TDD Exemption

A mission may proceed without the TDD loop only when its `Assumptions` section includes an assumption stating that the mission can be carried out TDD-exempt because every in-scope deliverable is a non-testable artifact.

The TDD-exempt assumption is valid only when all in-scope deliverables are non-testable artifacts.

- If any non-exempt artifacts (executable code, configuration that affects runtime behavior) are in scope, the assumption is invalid.

## TDD Execution Loop

When a mission does not have a valid TDD-exempt assumption, the execution phase must follow these sub-steps in order. The agent must not write prod-scope code before completing steps 1–3, and must not write prod-scope code for an AC before writing its failing test (step 4).

### 1. Setup / Verify Coverage Tool

Confirm the coverage tool is available and working. If the mission scopes coverage tool setup, complete that setup now. Run the tool once to verify it produces output. If it fails, surface the blocker — do not proceed without working coverage measurement.

### 2. Measure Baseline Coverage

Run the coverage tool against the code being touched by the mission. Record the baseline coverage percentage. This baseline is used in step 5 to verify no coverage regression.

### 3. Fill Coverage Gaps

If the baseline coverage on the target code is below the coverage threshold (>80% line coverage), write tests to bring it up to the threshold. Then:

- Verify all tests (existing and new) are green.
- Do not touch prod-scope code during this step. The goal is to establish a safety net around the code about to change, not to modify the code itself.

### 4. Per-AC Red-Green Cycle

For each acceptance criterion in mission.md, in order:

**a. Write a test** that asserts the AC's condition. The test must be specific to the AC — not a broad integration test that incidentally covers it.

**b. Verify the test is red** (fails). If the test passes immediately, apply the green-on-write rule:

- Verify the test would fail if the AC's condition were not met (e.g., by reasoning about or temporarily negating the assertion).
- If the test would still pass regardless, it is invalid — rewrite it and re-verify red.
- If the test would fail without the condition, the AC is already met by existing code. Record it as met and proceed to the next AC.

**d. Write the minimum prod code** to make the test pass.

**e. Verify the test is green.** If it fails, fix the prod code (not the test) and re-verify.

**f. Refactor** if needed, verifying tests remain green after any refactoring.

### 5. Final Verification

After all ACs have been addressed:

- Run the full test suite. All tests must pass.
- Run the coverage tool. Verify no coverage regression compared to the baseline recorded in step 2.
- If the target repo provides a formatter and/or linter, run them and ensure results are clean.

# Considerations

## Overview
This protocol governs the test-driven development loop within `/new-sdlc` execution phases.
