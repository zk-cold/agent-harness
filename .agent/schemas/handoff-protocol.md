# Handoff Protocol

This document defines the format, lifecycle, and rules for `handoff.md`.

## Contents

Every `handoff.md` must contain the following sections:

1. **Next / Ongoing Step** — The immediate next action or the step currently in progress. Must be specific enough for a fresh agent session to resume without re-interviewing the dev.
2. **Known Failed Attempts** — A list of approaches that were tried and failed, with brief reasons. This prevents a resuming agent from re-treading dead ends. If no attempts have failed, this section must still be present with "None" as its content.
3. **Dev Interview Transcript** — The full, verbatim Q&A from the interview phase. Every question asked and every answer given must be reproduced exactly. Do not summarize or paraphrase.

## Lifecycle

- **Full rewrite on phase conclusion.** At the conclusion of each phase (or at the lead agent's discretion mid-phase), `handoff.md` is fully rewritten — not appended to. The rewritten file must contain all three sections with current information.
- **Session-start check.** On session start, the lead agent must check for an existing `handoff.md` at the project root. If one exists, the agent loads it and uses its contents to orient before proceeding. If it exists but appears irrelevant to the dev's current prompt, the agent must confirm with the dev before discarding it.

## Cleanup

At the end of the final phase (Cleanup), the lead agent removes both `mission.md` and `handoff.md` from the project root. These are runtime artifacts and must not persist after a mission is complete.
