# Invariants

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
- **Cleanup reset to completion review.** If Cleanup is interrupted because a cleanup-phase merge is non-trivial under the applicable skill flow, rewrite `handoff.md` immediately so **Next / Ongoing Step** names the applicable completion-review phase for the merged state. Do not leave `handoff.md` pointing at Cleanup once that reset has occurred.
- **Session-start check.** On session start, the lead agent must inspect `.claude/worktrees/` and the main project root before any interview or execution work begins. If `handoff.md` or `mission.md` exists at the main project root, the lead agent must stop and ask the dev how to proceed before continuing. Otherwise, if exactly one worktree exists and it contains `handoff.md` at its root, the lead agent loads it and uses its contents to orient before proceeding. If multiple worktrees exist, or if exactly one worktree exists but it does not contain `handoff.md`, the lead agent must stop and ask the dev how to proceed before continuing. If no worktree exists and no legacy root runtime artifacts exist, the lead agent must create a worktree before any interview or execution work begins. If a `handoff.md` exists and the lead agent will treat the current prompt as fresh work instead of resuming that handoff, the lead agent must confirm with the dev before discarding or replacing it. Whenever the lead agent later spawns a non-lead agent, that prompt must include the exact sentence stem `You are a non-lead agent.`, must state that the recipient operates only on the role-specific inputs granted by its phase, and must forbid bootstrap discovery unless the active phase explicitly requires it. Spawned non-lead agents resume only from the role-specific artifacts or worktree context explicitly handed to them and must not perform their own bootstrap discovery unless the active phase explicitly requires it.
- **Canonical governance artifacts.** Until a change is merged, the authoritative copies of harness `CLAUDE.md`, harness `.agent/schemas/*.md`, and harness `.claude/commands/*.md` are the main repo-root copies. Matching worktree files and unstaged changes to them are proposals only and are not effective policy before merge.
- **Aborted missions are terminal.** If `handoff.md` says the mission is already aborted and must not be resumed per `.agent/schemas/abort-protocol.md`, the next session must not resume that mission. It may only summarize blockers, either follow the Recovery Protocol below or confirm whether the user wants to start fresh work, and then discard or replace the old handoff if appropriate.

## Recovery Protocol

Use this protocol only after `.agent/schemas/abort-protocol.md` has already been completed and `handoff.md` records that the prior mission is aborted and must not be resumed.

1. Recovery cannot begin until the dev provides input that addresses the blocker summary from the aborted mission.
2. The blocker-resolution conversation starts the Mission Creation phase for the restarted mission. If the blocker is resolved clearly enough during that conversation, the agent may draft mission.md within that same phase without a separate mission-generation phase.
3. If the dev's blocker resolution introduces a rule, constraint, or assumption for the restarted work that is not already explicit in the blocker summary or the prior approved mission, the agent must ask at least one follow-up question aimed at surfacing it.
4. When recovery surfaces a candidate new or modified `CLAUDE.md` invariant, the new mission must capture it in `Invariants`. When recovery surfaces a mission-specific constraint, the new mission must capture it in `Scope`, `Dependencies & Assumptions`, or `Acceptance Criteria`, as appropriate. When recovery surfaces a belief, the new mission may capture it in `Beliefs` only when it is traceable to an invariant; otherwise the agent must add the supporting invariant first or omit the belief.
5. The previously approved `mission.md` from the aborted mission remains unchanged throughout that aborted mission. After the abort state is already recorded and recovery has re-entered the Mission Creation phase, the agent drafts a new `mission.md` for the restarted lifecycle by consulting the previous mission and carrying forward only the prior content that still remains accurate after the blocker resolution and any newly captured invariants or considerations are applied.
6. Recovery resets `handoff.md` to restart the lifecycle from the Mission Creation phase for the new mission.
7. Recovery reuses the existing worktree. Before recovery continues, any file with unstaged changes that either modify `CLAUDE.md` or modify lines inside a `mission.md` file's `Invariants` or `Beliefs` sections must have all of its unstaged changes discarded.
8. The restarted mission goes through review and execution from scratch under the applicable skill flow. For `new-sdlc`, any mission recovered from abort is ineligible for fast path and must route to normal flow.

## Cleanup

At the end of the final phase (Cleanup), the lead agent removes both `mission.md` and `handoff.md` from the worktree root. These are runtime artifacts and must not persist after a mission is complete.

# Considerations

## Considerations

- **Handoff generator** — Use to produce a well-formed `handoff.md`. `python3 -m scripts.handoff_generator --pre-mission|--post-mission --next-step "<text>" [--failed-attempts "<text>"] [--transcript "<text>"]`. `--transcript` is required in `--pre-mission` mode and disallowed in `--post-mission` mode.
