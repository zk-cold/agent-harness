# Invariants

## Location
The canonical location of `handoff.md` is the worktree root.

## Resumption
On session start, if `handoff.md` exists and the mission is resumable, resume to the recorded **Next / Ongoing Step**.
Otherwise, follow `recovery-protocol.md`.

A mission is **resumable** when its `handoff.md` does not contain the abort sentinel string `This mission is already aborted and must not be resumed` — equivalently, `python3 -m scripts.bootstrap_check list` reports the worktree as `RESUMABLE` (rather than `ABORTED` or `NO_HANDOFF`).

## Failed Attempts Are Per Phase
Once a new phase begins, reset `Known Failed Attempts` to `None`.


# Considerations

## Handoff Template
Use `.agent/templates/handoff.md` to produce a well-formed `handoff.md`. Fill placeholders by direct substitution.

## Relatedness Test
A worktree's `handoff.md` is **related** to the current user request when the request would resume, modify, or supersede the work recorded in that handoff's `## Dev Interview Transcript`. During `Phase: Mission Creation` step 2, the lead reads each candidate transcript and applies this test; unrelated worktrees are left untouched.

