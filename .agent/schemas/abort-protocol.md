# Abort Protocol

This document defines the required behavior when a mission or fast-path run must stop without continuing to Cleanup.

## When To Abort

Follow this protocol when continuing the current mission would require reopening approved work. This includes:

1. After `mission.md` approval, implementation reveals the approved mission itself must change.
2. After `mission.md` approval, critic review reveals the approved mission itself must change.
3. Any equivalent terminal blocker where the current mission cannot continue without replacing or modifying the approved `mission.md`.

## Required Actions

1. Keep the approved `mission.md` unchanged. Do not edit it, replace it, or draft a successor `mission.md` autonomously.
2. Fully rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` before responding to the user.
3. Set `handoff.md`'s **Next / Ongoing Step** to: `Aborted: approved mission can no longer continue because <blocker summary>. This mission is already aborted and must not be resumed. Await a fresh user request.`
4. Preserve the current failed-attempt history and the full verbatim dev interview transcript in that rewritten `handoff.md`.
5. Present the blocker summary to the user and state that the current mission has been aborted.
6. Do not continue execution, review, or cleanup for that mission after aborting it.

## Resume Behavior

An aborted mission is terminal. If a later session finds a `handoff.md` whose **Next / Ongoing Step** says the mission is already aborted and must not be resumed, the lead agent must not resume that mission. The lead agent may only summarize the blockers, confirm whether the user's new prompt should be treated as a fresh request, and then discard or replace the old `handoff.md` if the user wants to proceed with new work.
