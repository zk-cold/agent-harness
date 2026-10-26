# Invariants

## Terms
Use the definitions in `.agent/schemas/governance-schema.md`.

## Lead Protocol
Do only these yourself: read or write the roadmap, run one command, and talk from your own context. Dispatch everything else to sub-agents, including any search for information that one command cannot trivially complete, and read only the sub-agent's report of it.

## Lead Loop
1. Poll the roadmap that the target repo's governance designates, keeping only items authored by someone with write access to the target repo and without open sub-items. Of those marked blocked, unblock each whose blocker is gone and drop the rest. While none remain, wait and poll again.
2. Pick a remaining item, carry out `/deliver` from the root branch with only the item's content written by people with write access, verbatim, as the user's request, then return to step 1.
