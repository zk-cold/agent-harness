# Invariants

## Fast-Path Eligibility Verification
Fast-path eligibility requires either of the following:
- The mission delivery mode is `Test-Only`.
- No more than three governance artifacts are modified or removed and no considerations are overridden.

## Eligibility-Reject Tag
A `REJECT` response that fails any criterion of `## Fast-Path Eligibility Verification` must begin with `REJECT[fast-path-eligibility]` before any free-form reasons.
