# Invariants

## Location
The canonical location of `handoff.md` is the worktree root.

## Contents

Before `mission.md` has been finalized, every `handoff.md` must contain the following sections:

1. **Next / Ongoing Step** — The immediate next action or the step currently in progress. Must be specific enough for a fresh agent session to resume without re-interviewing the dev. This field may also record the terminal aborted state defined by `.agent/schemas/abort-protocol.md`; when it does, the prior mission must not be resumed.
2. **Known Failed Attempts** — A list of approaches attempted and failed during the current phase only, with brief reasons. This prevents a resuming agent from re-treading dead ends that remain relevant to the step being resumed. When the phase changes, discard failed attempts from earlier phases instead of carrying them forward. If no attempts have failed in the current phase, this section must still be present with `None` as its content.
3. **Dev Interview Transcript** — The developer's initial prompt followed by the full, verbatim interview Q&A collected while shaping the mission. Every question asked and every answer given must be reproduced exactly. Do not summarize or paraphrase.

After `mission.md` has been finalized, `handoff.md` must still contain **Next / Ongoing Step** and **Known Failed Attempts**, but it must no longer include the **Dev Interview Transcript** section or any of its contents.

## Lifecycle

- **Full rewrite on phase conclusion.** At the conclusion of each phase (or at the primary agent's discretion mid-phase), `handoff.md` is fully rewritten — not appended to. Before `mission.md` is finalized, the rewritten file must contain all three sections with current information. After `mission.md` is finalized, the rewritten file must omit the **Dev Interview Transcript** section entirely.
- **Current-phase failed attempts only.** Every rewrite must keep only the failed attempts from the phase named in **Next / Ongoing Step**. When a new phase begins, reset **Known Failed Attempts** to `None` unless an attempt has already failed in that new phase.
- **Aborted missions are terminal.** If `handoff.md` says the mission is already aborted and must not be resumed per `.agent/schemas/abort-protocol.md`, the next session must not resume that mission. It may only summarize blockers, either follow the Recovery Protocol below or confirm whether the user wants to start fresh work, and then discard or replace the old handoff if appropriate.

## Recovery Protocol

Use this protocol only after `.agent/schemas/abort-protocol.md` has already been completed and `handoff.md` records that the prior mission is aborted and must not be resumed.

1. Recovery cannot begin until the dev provides input that addresses the blocker summary from the aborted mission.
2. The blocker-resolution conversation starts the Mission Creation phase for the restarted mission. If the blocker is resolved clearly enough during that conversation, the agent may draft mission.md within that same phase without a separate mission-generation phase.
3. If the dev's blocker resolution introduces a rule, constraint, or assumption for the restarted work that is not already explicit in the blocker summary or the prior approved mission, the agent must ask at least one follow-up question aimed at surfacing it.
4. When recovery surfaces a candidate new or modified `CLAUDE.md` invariant, the new mission must capture it in `Invariants`. When recovery surfaces a mission-specific constraint, the new mission must capture it in `Scope`, `Assumptions`, or `Acceptance Criteria`, as appropriate. When recovery surfaces a belief, the new mission may capture it in `Beliefs` only when it is a default-binding rule with an explicit scope or condition, is traceable to at least one consideration or implementation artifact, does not contradict invariants, and uses the same meaning of `implementation artifact` as this protocol: a concrete repository artifact whose implementation or behavior motivates the rule, such as a script, test, or generated runtime file.
5. The previously approved `mission.md` from the aborted mission remains unchanged throughout that aborted mission. After the abort state is already recorded and recovery has re-entered the Mission Creation phase, the agent drafts a new `mission.md` for the restarted lifecycle by consulting the previous mission and carrying forward only the prior content that still remains accurate after the blocker resolution and any newly captured invariants or considerations are applied.
6. Recovery resets `handoff.md` to restart the lifecycle from the Mission Creation phase for the new mission.
7. Recovery reuses the existing worktree. Before recovery continues, remove unstaged changes to governance artifacts from the working tree in a reversible way. For this rule, `governance artifacts` has the meaning defined by `.agent/schemas/governance-schema.md`. If governance changes are already isolated to whole files or hunks, the agent may discard just those governance changes. If a file mixes governance and non-governance unstaged edits such that the governance changes cannot be cleanly isolated, the agent must stash the whole file or the whole worktree before recovery continues rather than attempting partial manual discard. Any created stash entry must be reported in `handoff.md` or the user-facing response so the preserved work remains discoverable. Unstaged changes to non-governance code files may otherwise remain in place.
8. The restarted mission goes through review and execution from scratch under `/new-sdlc`. Any mission recovered from abort is ineligible for the lite fast-path Mission Creation review variant and must use the full review variant.

# Considerations

## Handoff Generator
Use to produce a well-formed `handoff.md`. `python3 -m scripts.handoff_generator --pre-mission|--post-mission --next-step "<text>" [--failed-attempts "<text>"] [--transcript "<text>"]`. `--transcript` is required in `--pre-mission` mode and disallowed in `--post-mission` mode.

