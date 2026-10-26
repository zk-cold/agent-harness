# Invariants

## Lead Protocol
Do only these yourself: read or write the roadmap, run one command, and talk from your own context. Dispatch everything else to sub-agents, including any search for information that one command cannot trivially complete, and read only the sub-agent's report of it.

## Lead Loop
1. Determine the target repo and its root branch as `/deliver` does.
2. Poll the roadmap that the target repo's governance designates, keeping only items authored by someone with write access to the target repo. While none remain, wait and poll again.
3. Pick a remaining item, carry out `/deliver` from the root branch with only the item's content written by people with write access, verbatim, as the user's request, then close the item and return to step 2.
