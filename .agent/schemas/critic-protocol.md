# Definitions

## Change Under Review
For the path given in the prompt, the output of `.agent/scripts/change-under-review <path> <root branch>` run from outside it.

# Invariants

## Terms
Use the definitions in `.agent/schemas/governance-schema.md`.

## Read-Only
Critics must not create, modify, or delete files.

## Allowed Commands
Critics may run only `.agent/scripts/change-under-review`, `.agent/scripts/verdict`, read-only `git` subcommands, and commands that only read the roadmap.

## Structured Response
A response is one `.agent/scripts/verdict` accepts, its `Rejection Grounds` being each in-scope issue that warrants rejection and its `Findings` each other observation, including any outside the critic's scope.
