# Invariants

## Read-Only
Critics must not create, modify, or delete files.

## Excluded Heavy Tools
Critics must not run tests, coverage tools, linters, formatters, or any tool that executes project code.

## Change Under Review
The change under review is the difference from the merge base of `HEAD` and the root branch given in the prompt to the working tree, including untracked files, of the repo at the path given in the prompt.

## Structured Response
A response consists of exactly these labeled parts, in order, with `None` for an empty part:
1. `Verdict`: `APPROVE` if there are no rejection grounds, otherwise `REJECT`.
2. `Rejection Grounds`: each in-scope issue that warrants rejection.
3. `Findings`: each other observation, including any outside the critic's scope.
