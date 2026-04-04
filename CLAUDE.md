# Invariants

## Lead-Agent Scope
This repo-root `CLAUDE.md` is written for the lead agent only. Non-lead agents may act only on the role-specific inputs explicitly granted by their phase and must not treat this file as their bootstrap source unless that phase explicitly requires it.

## New-SDLC Bootstrap
The purpose of this harness is to run work through `/new-sdlc`, and its bootstrap steps must be followed before interview, repo-specific analysis, or execution begins. The target repo may be this harness repo itself or another repo.

## Required Critic Review
Whenever `/new-sdlc` requires critic review, the lead agent must complete that review before continuing. If spawning a required critic agent is blocked because the environment requires explicit user approval, the user declines, or the critic tool is otherwise unavailable, the lead agent must stop, rewrite `handoff.md` with the blocker, and ask the dev for direction. The lead agent must not skip that review phase, continue execution, or proceed to Cleanup past it.

## Completion-Review Before Commits
Until `/new-sdlc`'s required completion-review phase approves the implementation, the lead agent and any spawned dev agent must keep the implementation uncommitted in the worktree. Before completion review, the lead agent must merge the latest applicable repo-root branch state into the current worktree and reconcile the implementation against that merged state. The applicable repo-root branch state is the integration branch named by the target repo's governing artifacts; if those artifacts name none, it is the branch from which the worktree was created. A merge is non-trivial when it is neither `Already up to date.` nor a clean fast-forward with no merge commit and no manual conflict resolution. Completion-review critics must review the live uncommitted diff plus the required runtime verification artifacts for that merged state. If that pre-review merge, or any cleanup-phase merge attempted before the worktree is removed, is non-trivial, the lead agent must reset the mission to the applicable completion-review phase, re-verify the acceptance criteria against the merged state, and obtain fresh completion-review approval before creating additional commits or removing the worktree. Only after that approval may the lead agent create the commit or commits needed to leave the worktree clean for Cleanup.

## Approved Mission Immutability
Once a `mission.md` has been approved for `/new-sdlc`, that approved mission is immutable for the rest of that mission. If implementation or review reveals the mission must change, the lead agent must stop the current mission, keep the approved `mission.md` unchanged, and follow `.agent/schemas/abort-protocol.md`, including rewriting `handoff.md` to state that the mission is already aborted and not resumable. The lead agent must not autonomously create a replacement mission.

## Belief Definition Consistency
Belief-definition rules in `mission-schema.md` and `handoff-protocol.md` must stay consistent. When `.agent/schemas/mission-schema.md` defines beliefs or `.agent/schemas/handoff-protocol.md` qualifies when a recovered mission may capture a belief, the file must require that beliefs define default-binding rules with an explicit scope or condition, are traceable to at least one consideration or implementation artifact, and do not contradict invariants. For this invariant, an implementation artifact is a concrete repository artifact whose implementation or behavior motivates the rule, such as a script, test, or generated runtime file.

## Meta Governance
This harness has no external constraints

# Considerations

## Template Files
Template files (`*.template`) inside this harness are not governance files as set out by `governance-schema.md`. They, however, materially shape how the Invariants and Beliefs are enforced. Flag any proposed changes to the developer and include full approved text in `mission.md` as a **consideration**.

## Enforcement Limits
These invariants are currently text-only. More direct enforcement will require prompt, phase, merge-state, and mission-lifecycle observability from the harness.

## Bootstrap Check
Run within Mission Creation after routing, against the applicable repo root. Two subcommands:
- `python3 -m scripts.bootstrap_check [repo_root]` — Outputs one of: `ROOT_ARTIFACTS`, `MULTIPLE_WORKTREES`, `ONE_WORKTREE_NO_HANDOFF`, `ONE_WORKTREE_ABORTED`, `ONE_WORKTREE_RESUMABLE`, `NO_WORKTREE`. Exits 0 in all cases. Use to detect root artifacts and get an overall worktree-state summary.
- `python3 -m scripts.bootstrap_check list [repo_root]` — Outputs one line per worktree: `<path> <status>`, where status is `RESUMABLE`, `ABORTED`, or `NO_HANDOFF`. Exits 0 in all cases (outputs nothing when no worktrees exist). Use during the interview to inspect individual worktrees before applying the relatedness test defined in `.agent/schemas/handoff-protocol.md` and `.claude/commands/new-sdlc.md`.
