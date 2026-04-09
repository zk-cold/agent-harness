# Invariants

## Excluded Heavy Tools
Critics must not run tests, coverage tools, linters, formatters, or any tool that executes project code.

## Approve with No Comments
An approval response must be exactly `APPROVE` with no additional text.
If there are any feedback, caveats, requested changes, the response must be `REJECT` with reasons.

# Considerations

## Counting Governance Artifacts
Each new/modified/removed prose rule count as 1 change in its respective category.
Each template change count as 1 consideration change.
Each semantically-modified test count as 1 change in its respective category (invariant or external constraint).