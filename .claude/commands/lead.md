---
description: Delivers roadmap items, up to three at once.
hooks:
  Stop:
    - hooks:
        - type: command
          command: jq -e '(.background_tasks // []) != [] or (.last_assistant_message // "" | test("(^|\n)Awaiting user[.][[:space:]]*$"))' >/dev/null || { echo 'Continue the Lead Loop, or end your message with the line "Awaiting user." to yield to the user.' >&2; exit 2; }
---
# Invariants

## Target Repo Governance
Follow the target repo's `AGENTS.md` and `.agent/schemas/*.md`.

## Terms
Use the definitions in `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/governance-schema.md` and `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/roadmap.md`.

## Lead Protocol
Do only these yourself: read or write the roadmap, run one command, and talk from your own context. Dispatch everything else to sub-agents, including any search for information that one command cannot trivially complete.

## Dispatched Searches
Of a dispatched search, read only the sub-agent's report.

## Yielding
End a turn only to await your background tasks or, with `Awaiting user.` as its last line, to yield to the user as `/deliver` or the user asks.

## Lead Loop
1. List candidates or, after a pass that left none and with no delivery in progress, run `${CLAUDE_PLUGIN_ROOT}/.agent/scripts/poll <backend> <target repo path>` with the roadmap's backend and a 10-minute timeout, taking the candidates it prints. Keep those on the roadmap. Of those marked blocked, unblock each whose blocker is gone and drop the rest. While none remain and no delivery is in progress, repeat this step.
2. While fewer than three deliveries are in progress and a remaining item that descends from none of their roadmap items, as listing their descendants shows, has no foreseeable overlap with them, choosing first the most urgent items and those due within 5 days, then those that most pave the way for other items, sharpen the tools delivering them, or by their delay would likely void work on other items, carry out `/deliver` from the root branch with the output of showing such an item, verbatim, as the user's request, dispatching its agents in the background. Return to step 1 whenever a delivery finishes.
