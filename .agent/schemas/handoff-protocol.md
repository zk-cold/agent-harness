# Invariants

## Location
The canonical location of `handoff.md` is the worktree root.

## Resumption
On session start, if `handoff.md` exists and the mission is resumable, resume to the recorded **Next / Ongoing Step**.
Otherwise, follow `recovery-protocol.md`.

## Failed Attempts Are Per Phase
Once a new phase begins, reset `Known Failed Attempts` to `None`.


# Considerations

## Handoff Template
Use `.agent/templates/handoff.md` to produce a well-formed `handoff.md`. Fill placeholders by direct substitution.

