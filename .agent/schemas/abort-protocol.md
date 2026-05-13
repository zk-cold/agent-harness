# Invariants

## When To Abort
Follow this protocol when the current mission cannot continue without replacing or modifying the approved `mission.md`.

## Abort Marker
State in `handoff.md`'s **Next / Ongoing Steps** that the mission is aborted and must not be resumed, including the blocker summary.

## Worktree Preservation
Do not remove the worktree during abort.

## Terminal Halt
Do not continue execution, review, or cleanup after abort.

## Worktree Cleanup
A permanently-aborted worktree may only be removed via `python3 -m scripts.cleanup_aborted_worktree <worktree-path>`.
