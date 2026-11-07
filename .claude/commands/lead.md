---
description: Delivers roadmap items one after another.
hooks:
  Stop:
    - hooks:
        - type: command
          command: jq -e '.last_assistant_message // "" | test("(^|\n)Awaiting user[.][[:space:]]*$")' >/dev/null || { echo 'Continue the Lead Loop, or end your message with the line "Awaiting user." to yield to the user.' >&2; exit 2; }
---
# Invariants

## Terms
Use the definitions in `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/governance-schema.md`.

## Lead Protocol
Do only these yourself: read or write the roadmap, run one command, and talk from your own context. Dispatch everything else to sub-agents, including any search for information that one command cannot trivially complete, and read only the sub-agent's report of it.

## Yielding
End a turn only to yield to the user, as `/deliver` or the user asks, with `Awaiting user.` as its last line.

## Lead Loop
1. List candidates or, after a pass that left none, run `${CLAUDE_PLUGIN_ROOT}/.agent/scripts/poll <backend> <target repo path>` with the roadmap's backend and a 10-minute timeout, taking the candidates it prints. Keep those on the roadmap. Of those marked blocked, unblock each whose blocker is gone and drop the rest. While none remain, repeat this step.
2. Pick a remaining item, carry out `/deliver` from the root branch with the output of showing it, verbatim, as the user's request, then return to step 1.
