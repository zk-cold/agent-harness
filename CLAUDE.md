# Invariants

## Bootstrap
Unless you are a sub-agent, handle any prompt with `/new-sdlc`.

## Mandatory Critic Review
Required critic reviews must be completed before continuing.

## Completion-Review before Commits
Until required completion-review approves the implementation, the implementation must stay uncomitted in the worktree.

## Approved Mission Immutability
Once a `mission.md` has been approved, that approved mission is immutable for the rest of that mission.

## Meta Governance
This harness must have no external constraints.

## Root Branch
The root branch for this harness is `main`.

# Considerations

## Critic Spawning Blockers
If spawning the required critic is blocked by runtime, the mission must be blocked, and user must be prompted for direction.

## Abort Protocol
If implementation or review reveals an immutable `mission.md` must change, keep the `mission.md` unchanged, and follow `.agent/schemas/abort-protocol.md`.

## Completion-Review Detailed Workflow
The applicable repo-root branch state is the integration branch named by the target repo's governing artifacts; if those artifacts name none, it is the branch from which the worktree was created.
Before the completion review, the latest applicable repo-root branch state must be merged the current worktree.
A merge is non-trivial when it is neither `Already up to date.` nor a clean merge with no manual conflict resolution.
When the merge is non-trivial, the lead agent must verify merged diff (including uncomitted changes) from repo-root branch state, against the defined Scope and ACs, before submission for review.
Completion-review critics must review the live uncommitted diff plus the required runtime verification artifacts for that merged state.
If clean-up phase merge is non-trivial, mission must be reset to completion-review phase, and obtain fresh completion-review approvals.
Only after such approval, the changes can be merged back to repo-root branch state & cleaned up.

## Template Files
Flag any proposed template (`*.template`) changes to the developer and include full approved text of updated sections in `mission.md` as a **consideration**.

## Harness-Local Scope Invariant
The opening scope invariant in this file is specific to this harness `CLAUDE.md`. It should not be generalized into an assumption that target repo `CLAUDE.md` files use the same audience or scope model.

## Codex Sub-Agent Boundary
In this harness, the opening scope invariant means Codex sub-agents must ignore `CLAUDE.md` while still being free to continue reading `AGENTS.md`. That split is deliberate: `CLAUDE.md` carries lead-only governance here, while `AGENTS.md` remains a useful Codex routing artifact.

## Bootstrap Breadth
`Bootstrap` intentionally treats any prompt as a request to create new SDLC. That breadth is deliberate for the current harness because governance-document edits are implementation work. Narrowing should happen only through future explicit exclusions, not by silently weakening the invariant.

## Bootstrap Check
Run within Mission Creation after routing, against the applicable repo root. Two subcommands:
- `python3 -m scripts.bootstrap_check [repo_root]` — Outputs one of: `ROOT_ARTIFACTS`, `MULTIPLE_WORKTREES`, `ONE_WORKTREE_NO_HANDOFF`, `ONE_WORKTREE_ABORTED`, `ONE_WORKTREE_RESUMABLE`, `NO_WORKTREE`. Exits 0 in all cases. Use to detect root artifacts and get an overall worktree-state summary.
- `python3 -m scripts.bootstrap_check list [repo_root]` — Outputs one line per worktree: `<path> <status>`, where status is `RESUMABLE`, `ABORTED`, or `NO_HANDOFF`. Exits 0 in all cases (outputs nothing when no worktrees exist). Use during the interview to inspect individual worktrees before applying the relatedness test defined in `.agent/schemas/handoff-protocol.md` and `.claude/commands/new-sdlc.md`.
