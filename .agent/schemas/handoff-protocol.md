# Handoff Protocol

This document defines the format, lifecycle, and rules for `handoff.md`. The canonical location of `handoff.md` is the worktree root.

## Contents

Before `mission.md` has been finalized, every `handoff.md` must contain the following sections:

1. **Next / Ongoing Step** — The immediate next action or the step currently in progress. Must be specific enough for a fresh agent session to resume without re-interviewing the dev. This field may also record the terminal aborted state defined by `.agent/schemas/abort-protocol.md`; when it does, the prior mission must not be resumed.
2. **Known Failed Attempts** — A list of approaches attempted and failed during the current phase only, with brief reasons. This prevents a resuming agent from re-treading dead ends that remain relevant to the step being resumed. When the phase changes, discard failed attempts from earlier phases instead of carrying them forward. If no attempts have failed in the current phase, this section must still be present with `None` as its content.
3. **Dev Interview Transcript** — The developer's initial prompt followed by the full, verbatim interview Q&A collected while shaping the mission. Every question asked and every answer given must be reproduced exactly. Do not summarize or paraphrase.

After `mission.md` has been finalized, `handoff.md` must still contain **Next / Ongoing Step** and **Known Failed Attempts**, but it must no longer include the **Dev Interview Transcript** section or any of its contents.

## Lifecycle

- **Full rewrite on phase conclusion.** At the conclusion of each phase (or at the lead agent's discretion mid-phase), `handoff.md` is fully rewritten — not appended to. Before `mission.md` is finalized, the rewritten file must contain all three sections with current information. After `mission.md` is finalized, the rewritten file must omit the **Dev Interview Transcript** section entirely.
- **Current-phase failed attempts only.** Every rewrite must keep only the failed attempts from the phase named in **Next / Ongoing Step**. When a new phase begins, reset **Known Failed Attempts** to `None` unless an attempt has already failed in that new phase.
- **Session-start check.** On session start, the lead agent must inspect `.claude/worktrees/` and the main project root before any interview or execution work begins. If `handoff.md` or `mission.md` exists at the main project root, the agent must stop and ask the dev how to proceed before continuing. Otherwise, if exactly one worktree exists and it contains `handoff.md` at its root, the agent loads it and uses its contents to orient before proceeding. If multiple worktrees exist, or if exactly one worktree exists but it does not contain `handoff.md`, the agent must stop and ask the dev how to proceed before continuing. If no worktree exists and no legacy root runtime artifacts exist, the agent must create a worktree before any interview or execution work begins. If a `handoff.md` exists and the agent will treat the current prompt as fresh work instead of resuming that handoff, the agent must confirm with the dev before discarding or replacing it.
- **Aborted missions are terminal.** If `handoff.md` says the mission is already aborted and must not be resumed per `.agent/schemas/abort-protocol.md`, the next session must not resume that mission. It may only summarize blockers, confirm whether the user wants to start fresh work, and then discard or replace the old handoff if appropriate.

## Cleanup

At the end of the final phase (Cleanup), the lead agent removes both `mission.md` and `handoff.md` from the worktree root. These are runtime artifacts and must not persist after a mission is complete.
