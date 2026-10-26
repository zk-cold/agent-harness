# Invariants

## Read-Only
Critics must not create, modify, or delete files.

## Excluded Heavy Tools
Critics must not run tests, coverage tools, linters, formatters, or any tool that executes project code.

## Change Under Review
The change under review is every uncommitted change, including untracked files, in the repo at the path given in the prompt.

## Approve with No Comments
An approval response must be exactly `APPROVE` with no additional text.
If there are any feedback, caveats, requested changes, the response must be `REJECT` with reasons.
