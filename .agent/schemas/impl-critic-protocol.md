# Invariants

## Test Result Verification
The implementation review must use `test-output.txt` from the worktree root. All tests reported in that file must pass.

## Lint Verification
When formatter or linter verification is required, the implementation review must use `lint-output.txt` from the worktree root. All checks reported in that file must pass.

## Coverage Threshold Verification
Modified prod-scope code must meet the coverage threshold.

## TDD Exemption Validation
When the mission assumes `TDD-exempt`, all implementation artifacts must be non-testable.

## Test-Only Validation
When the mission assumes `Test-Only`, all implementation artifacts must be test-scope only.

# Considerations

## Coverage Report
If coverage verification is needed, use `coverage-output.txt` from the worktree root.
