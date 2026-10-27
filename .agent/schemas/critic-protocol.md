# Definitions

## Change Under Review
For the path given in the prompt, the output of `.agent/scripts/change-under-review <path> <root branch>` run from outside it.

# Invariants

## Terms
Use the definitions in `.agent/schemas/governance-schema.md`.

## Read-Only
Critics must not create, modify, or delete files.

## Allowed Commands
Critics may run only `.agent/scripts/change-under-review`, read-only `git` subcommands, and commands that only read the roadmap.

## Structured Response
A response consists of only these labeled parts, in order, omitting any empty part:
1. `Verdict`: `APPROVE` if there are no rejection grounds, otherwise `REJECT`.
2. `Rejection Grounds`: each in-scope issue that warrants rejection.
3. `Findings`: each other observation, including any outside the critic's scope.
