# Invariants

## Flow Order
For a fresh request, the lead agent must follow the shared phases and then the applicable flow-specific phases in order.

## Target Repo Governance Precedence
When operating inside a target repo, that repo's `CLAUDE.md` invariants, beliefs, and considerations govern ahead of this harness's beliefs and considerations. Any target-repo-specific dependencies or assumptions recorded in the mission govern execution decisions unless doing so would violate the target repo's own invariants.

## Handoff Resumption
If a relevant `handoff.md` exists on session start, the lead agent may resume only from a recorded Next / Ongoing Step that clearly maps to one of the phases below or a substep within the current phase. If that handoff marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume it. Otherwise, if the recorded step does not clearly map to a phase or substep, the lead agent must ask the dev how to proceed instead of skipping required phases.

## Required Critic Availability

Any phase in this skill that requires critic agents is blocking. If the environment requires explicit user approval before spawning a required critic, the user declines, or the critic tool is otherwise unavailable, the lead agent must fully rewrite `handoff.md` per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Blocked: awaiting user approval or tool availability to spawn the required critic agent(s) for <phase name>. Do not resume past this phase without that review.` Then stop, surface the blocker to the dev, and await direction. The lead agent must not skip the blocked review phase, continue execution, or proceed to Cleanup past it.

## Shared Phases

### Phase: Mission Creation

**Actor:** Lead agent (interview and mission drafting); one or two critic agents depending on review variant.
**Inputs (critic agents):** The harness repo-root `.agent/schemas/governance-schema.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, the harness repo-root `.agent/schemas/mission-schema.md`, `mission.md` from the worktree root, and for lite review only, any raw eligibility tool outputs explicitly relied on during the interview, such as coverage report output. In every critic prompt, `governance-schema.md` must be the first governance artifact listed.
**Outputs:** Approved `mission.md` at the worktree root, with review outcome determining whether execution proceeds through fast path or normal flow.

Begin the interview. First determine which repo is the target repo; for harness-governance or harness-implementation requests, the target repo is this harness repo itself. If the target repo is not automatically clear, ask the user to clarify before proceeding. Once the target repo is identified, immediately check it for root artifacts: if `handoff.md` or `mission.md` exists at the target repo root, the lead agent must stop and ask the dev how to proceed before continuing. Then read and follow that repo's `CLAUDE.md` before any repo-specific analysis or execution begins, and search the target repo for repo-local `SKILL.md` files. For each skill found, follow that skill before continuing mission work there. If the mission proposes changes to any harness `*.template` file, the lead agent must flag that fact to the dev during Mission Creation and must ensure `mission.md` includes the full proposed text for each changed template file in `Considerations`.

During the interview, the lead agent must check for worktrees under the target repo's `.claude/worktrees/` directory: for each worktree, read its `handoff.md` (if any) and judge whether it is related to the current request using the relatedness test in `.agent/schemas/handoff-protocol.md`. If the lead agent judges a worktree handoff to be related, it must surface that handoff to the dev and ask how to proceed. Unrelated worktrees must be ignored. If the loaded `handoff.md` marks the prior mission as already aborted and not resumable per `.agent/schemas/abort-protocol.md`, the lead agent must not resume that mission. Summarize the blockers from the old handoff to the user, then either follow the Recovery Protocol in `.agent/schemas/handoff-protocol.md` or confirm that the current prompt should be treated as fresh work before discarding or replacing that handoff. Any mission recovered from abort is ineligible for lite review: it restarts from Phase: Mission Creation under the Recovery Protocol and then uses full review. Otherwise, if it reflects a mission whose `mission.md` has already been approved and the current prompt changes that mission's scope or intent, the lead agent must not resume that mission. Keep the approved `mission.md` unchanged and follow `.agent/schemas/abort-protocol.md` using the scope or intent change as the blocker summary. After surfacing that abort to the user, confirm that the new prompt should be treated as fresh work before discarding or replacing the old handoff. If the lead agent will treat the current prompt as fresh work instead of resuming the loaded `handoff.md`, confirm with the dev before discarding or replacing that handoff. If the handoff is relevant, the lead agent may resume from its recorded Next / Ongoing Step per `.agent/schemas/handoff-protocol.md` only when that step clearly continues the same mission without reopening approved work. The lead agent must create a worktree in the target repo before any execution work begins. Whenever the lead agent later spawns a non-lead agent for this skill, instantiate the matching prompt from `.agent/templates/new-sdlc-subagents.prompt.template`.

If no relevant `handoff.md` exists, begin the interview from scratch. If a relevant `handoff.md` resumes Phase: Mission Creation, continue from the recorded next question or step rather than restarting from scratch. Mission Creation is a single loop:

1. Interview until the lead agent has enough information to draft or revise `mission.md`.
2. Draft or revise `mission.md` at the worktree root following the harness repo-root `.agent/schemas/mission-schema.md`.
3. Submit the current draft to the applicable review variant.
4. If the required approvals are not yet obtained, return to interview and drafting only as needed, then repeat the loop.

**Fast-path eligibility:** A request qualifies for the fast path only when all four criteria are met:

1. **No modification or removal of more than one governing artifacts** — Changing a `*.template` file referenced by a governed document counts as a consideration change.
2. **No belief or consideration overrides**
3. **>80% test coverage around target code**
4. **Clear scope, limited & safe change** — the change is well-defined, modifies no more than three files, does not alter control flow shared across modules, and does not change public API contracts except to add new ones or remove deprecated ones.

After each draft, the lead agent selects one review variant for that loop iteration:

- **Lite review** — use whenever fast path is still plausible and no eligibility criterion is already known to fail. Confirmed evidence is preferred, but not required for every criterion during Mission Creation: unresolved, plausible, later-checkable fast-path facts may remain as explicit `Assumptions` in `mission.md` and optional raw eligibility tool outputs. Spawn one critic agent. That critic reads only the harness repo-root `.agent/schemas/governance-schema.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, the harness repo-root `.agent/schemas/mission-schema.md`, `mission.md`, and any raw eligibility tool outputs explicitly relied on during the interview, and must follow the listed critic protocol. Instantiate the `Mission Creation Lite-Review Critic` template from `.agent/templates/new-sdlc-subagents.prompt.template` with `governance-schema.md` first, then only those remaining artifact references plus raw eligibility tool outputs. If the critic cannot be spawned, follow Required Critic Availability before taking any other action.
- **Full review** — use whenever any fast-path eligibility criterion is already known to be unmet, whenever lite review rejects for fast-path ineligibility or invalid fast-path assumptions, or whenever the lead agent already knows the mission must proceed through normal flow. Spawn the first critic agent for `mission.md` review. That critic reads only the harness repo-root `.agent/schemas/governance-schema.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, the harness repo-root `.agent/schemas/mission-schema.md`, and `mission.md`, and must follow the listed critic protocol. Instantiate the `Mission Creation Full-Review Critic` template from `.agent/templates/new-sdlc-subagents.prompt.template` with `governance-schema.md` first, then only those remaining artifact references. If the first critic approves, spawn a second fresh critic with the same allowed inputs and prompt template. If either required critic cannot be spawned, follow Required Critic Availability before taking any other action.

Review outcomes stay within Mission Creation until approvals are complete:

- If lite review approves: that exact `mission.md` becomes the approved mission for the rest of this fast-path run and must not be modified. Proceed to fast-path Phase: Execute in Worktree.
- If lite review rejects for fast-path ineligibility: stay in Mission Creation, switch to full review, and continue the loop without treating this as a separate phase.
- If lite review rejects for other reasons: the lead agent fixes the issues and repeats Mission Creation under lite review if eligibility still holds, otherwise under full review. Repeat until approved, or escalate to the user if stuck.
- If the first full-review critic rejects: the lead agent fixes the issues and repeats Mission Creation under full review from the first critic step. Repeat until approved, or escalate to the user if stuck.
- If the first full-review critic approves and the second full-review critic approves: that exact `mission.md` becomes the approved mission for the rest of this mission and must not be modified. Proceed to normal-flow Phase: Dev Agent Execution.
- If the second full-review critic rejects: the lead agent fixes the issues and repeats Mission Creation under full review from the first critic step. Repeat until approved, or escalate to the user if stuck.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Fast-Path Flow

### Phase: Execute in Worktree (Fast Path)

**Actor:** Lead agent.
**Inputs:** Approved `mission.md`, target repo codebase.
**Outputs:** Implementation (code changes in worktree), passing unit tests, modified code remains above the >80% coverage threshold.

Execute the approved mission in an isolated git worktree. The exact `mission.md` approved in Phase: Mission Creation is the execution contract for this phase and must remain unchanged. Produce only the deliverables specified in scope. Leave implementation changes uncommitted in the worktree for Post-Implementation Review (Fast Path); do not create commits during this phase. If implementation reveals that the mission itself must change, follow `.agent/schemas/abort-protocol.md`.

If the approved mission includes the TDD-exempt assumption defined by `.agent/schemas/tdd-protocol.md`, verify that the assumption is valid (all deliverables are non-executable artifacts), then execute without the TDD loop. If execution reveals that the assumption is false, follow `.agent/schemas/abort-protocol.md`. Otherwise, follow the TDD Execution Loop defined in `.agent/schemas/tdd-protocol.md`. This includes: setup/verify coverage tool, measure baseline, verify baseline meets threshold (abort if not), per-AC red-green cycle, and final verification (coverage threshold check).

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

### Phase: Post-Implementation Review (Fast Path)

**Actor:** One fresh critic agent (not the Phase: Mission Creation lite-review critic).
**Inputs:** The exact `mission.md` approved in Phase: Mission Creation, the harness repo-root `.agent/schemas/governance-schema.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, and read-only tool access to the worktree and repository. The critic is a tool-capable critic per `.agent/schemas/critic-protocol.md`.
**Outputs:** Response per `.agent/schemas/critic-protocol.md`.

Before writing heavy verification outputs or spawning the critic, the lead agent must merge the latest applicable target-repo root branch state into the current worktree and reconcile the implementation against that merged state. The applicable branch is the integration branch named by the target repo's governing artifacts; if those artifacts name none, it is the branch from which the worktree was created. If Git reports `Already up to date.` or performs a clean fast-forward, continue this phase on the merged state. Otherwise the merge is non-trivial per the harness repo-root `CLAUDE.md` `Trivial Merge Qualification` invariant: re-run the related unit tests and re-verify all acceptance criteria against the merged state, rewrite `handoff.md` with Next / Ongoing Step set to `Phase: Post-Implementation Review (Fast Path) - rerun verification on the merged state, rewrite completion-review runtime artifacts, and submit that state to a fresh critic.`, and restart this phase from its beginning with a fresh critic.

After the applicable repo-root state has been merged, the lead agent must write any heavy verification outputs (test suite results, coverage reports, linter output) as dedicated runtime artifact files at the worktree root per the Completion-Review Tool Access section of `.agent/schemas/critic-protocol.md`. These runtime artifact files are intentional, git-ignored review inputs created for critic review. They must contain only raw tool output per `.agent/schemas/critic-protocol.md` and must not include lead-agent summaries, acceptance-criteria self-evaluation, or incidental temporary files such as test tmp output.

Spawn a fresh critic agent with read-only tool access and the worktree path. The critic uses its granted tools (Read, Grep, Glob, `git diff`, `git log`, `git show`) to inspect the live uncommitted diff, the changes, and the codebase directly. The critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the approved mission, and does not violate any invariants in the repo-root governing artifacts listed in Inputs. The critic must follow the listed critic protocol. Instantiate the `Fast-Path Post-Implementation Critic` template from `.agent/templates/new-sdlc-subagents.prompt.template` with `governance-schema.md` first, then only the remaining governing artifact references listed in Inputs and the worktree path. If changed target-repo governance or skill-definition files are discoverable through the critic's tool access, the critic reviews them directly. If review would require information outside the approved mission, the phase-allowed artifacts, or tool-accessible data, do not brief the critic; follow `.agent/schemas/abort-protocol.md` or the applicable escalation flow instead. If the critic cannot be spawned, follow Required Critic Availability before taking any other action. If the diff modifies or deletes test code, or modifies or deletes invariants in governance files, the critic must REJECT — the change is not eligible for fast path.

- If the critic approves: create the commit or commits needed to leave the approved implementation clean in the worktree, then proceed to Phase: Cleanup.
- If the critic rejects because the change is no longer eligible for fast path: escalate to normal flow per Escalation: Fast Path to Normal Flow.
- If the critic rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree, re-runs related unit tests, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh critic. Repeat until approved, or escalate to the user if stuck.
- If the critic rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Escalation: Fast Path to Normal Flow

When fast-path eligibility is lost during or after implementation (e.g., the post-implementation critic rejects for eligibility), the lead agent must evaluate whether the approved `mission.md` can be submitted intact to the full Mission Creation review variant:

- **If `mission.md` can be submitted intact** (no fast-path-specific language that would need removal): The lead agent submits it to one additional critic for mission review using the `Fast-Path Escalation Critic` template from `.agent/templates/new-sdlc-subagents.prompt.template`. This brings the total mission-review approvals to two (one from lite Mission Creation review, one from this escalation review). If this critic approves, the mission remains the approved mission and the lead agent proceeds to normal-flow Phase: Dev Agent Execution, handing the dev subagent the approved `mission.md` and the unstaged work from the fast-path attempt. If this critic rejects, the lead agent fixes the issues and resubmits to a fresh critic. Repeat until approved, or escalate to the user if stuck.

- **If `mission.md` requires modification** (e.g., contains fast-path-specific language): The lead agent aborts per `.agent/schemas/abort-protocol.md`, keeping the approved `mission.md` unchanged. Then follow the Recovery Protocol in `.agent/schemas/handoff-protocol.md`: restart from Phase: Mission Creation, draft a new `mission.md` only after the recovery interview is complete, submit it to the full review variant in Phase: Mission Creation, and proceed through normal-flow execution. Unstaged work from the fast-path attempt is preserved in the worktree for the dev agent.

If the escalation critic cannot be spawned, follow Required Critic Availability before taking any other action.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

## Normal Flow

### Phase: Dev Agent Execution

**Actor:** Dev subagent (spawned by the lead agent via the Agent tool).
**Inputs:** The harness repo-root `.agent/schemas/governance-schema.md`, approved `mission.md`, target repo codebase (in worktree). If escalated from fast path, any unstaged work from the fast-path attempt is present in the worktree. In the spawned dev prompt, `governance-schema.md` must be the first governance artifact listed.
**Outputs:** Implementation (code changes in worktree), modified code remains above the >80% coverage threshold, clean formatter/linter results.

The lead agent spawns a dev subagent and hands it the approved `mission.md`. Instantiate the `Dev Agent Execution` template from `.agent/templates/new-sdlc-subagents.prompt.template` with `governance-schema.md` first. The dev agent executes the approved mission in the worktree from that handed-off context and must not rerun session-start bootstrap discovery of `.claude/worktrees/`, the main project root, `handoff.md`, or `mission.md` unless a later phase explicitly requires it. The exact `mission.md` approved in the preceding review phase is the execution contract and must remain unchanged. The dev agent must produce only the deliverables specified in scope and must leave implementation changes uncommitted in the worktree for post-implementation review. If implementation reveals that the mission itself must change, the dev agent must stop and report the blocker to the lead agent, who then follows `.agent/schemas/abort-protocol.md`.

If the approved mission includes the TDD-exempt assumption defined by `.agent/schemas/tdd-protocol.md`, the dev agent verifies that the assumption is valid (all deliverables are non-executable artifacts), then executes without the TDD loop. If execution reveals that the assumption is false, the dev agent must stop and report the blocker to the lead agent, who then follows `.agent/schemas/abort-protocol.md`. Otherwise, the dev agent must follow the TDD Execution Loop defined in `.agent/schemas/tdd-protocol.md`. This includes: setup/verify coverage tool, measure baseline, verify baseline meets threshold (abort if not), per-AC red-green cycle, and final verification (coverage threshold check + formatter/linter).

Only after the TDD loop's final verification passes (or, for missions proceeding under a valid TDD-exempt assumption, after all deliverables are produced and acceptance criteria verified) does the dev agent report completion to the lead agent.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

### Phase: 2-Critic Post-Implementation Review

**Actor:** Two fresh critic agents, spawned sequentially (not any previously used critics in this mission).
**Inputs:** The exact approved `mission.md`, the harness repo-root `.agent/schemas/governance-schema.md`, the harness repo-root `.agent/schemas/critic-protocol.md`, and read-only tool access to the worktree and repository. Each critic is a tool-capable critic per `.agent/schemas/critic-protocol.md`.
**Outputs:** Response per `.agent/schemas/critic-protocol.md` from each critic that is spawned.

Before writing heavy verification outputs or spawning the critics, the lead agent must merge the latest applicable target-repo root branch state into the current worktree and reconcile the implementation against that merged state. The applicable branch is the integration branch named by the target repo's governing artifacts; if those artifacts name none, it is the branch from which the worktree was created. If Git reports `Already up to date.` or performs a clean fast-forward, continue this phase on the merged state. Otherwise the merge is non-trivial per the harness repo-root `CLAUDE.md` `Trivial Merge Qualification` invariant: re-run the full regression suite, re-verify all acceptance criteria against the merged state, rewrite `handoff.md` with Next / Ongoing Step set to `Phase: 2-Critic Post-Implementation Review - rerun verification on the merged state, rewrite completion-review runtime artifacts, submit that state to the first fresh critic, and if it approves then to a second fresh critic.`, and restart this phase from its beginning with two fresh critics.

After the applicable repo-root state has been merged, the lead agent must write any heavy verification outputs (full test suite results, coverage reports, linter output) as dedicated runtime artifact files at the worktree root per the Completion-Review Tool Access section of `.agent/schemas/critic-protocol.md`. These runtime artifact files are intentional, git-ignored review inputs created for critic review. They must contain only raw tool output per `.agent/schemas/critic-protocol.md` and must not include lead-agent summaries, acceptance-criteria self-evaluation, or incidental temporary files such as test tmp output.

Spawn the first fresh critic agent with read-only tool access and the worktree path. That critic uses its granted tools (Read, Grep, Glob, `git diff`, `git log`, `git show`) to inspect the live uncommitted diff, the changes, and the codebase directly. The critic evaluates whether the implementation stays within scope, satisfies all acceptance criteria in the approved mission, and does not violate any invariants in the repo-root governing artifacts listed in Inputs. The critic must follow the listed critic protocol. Instantiate the `Normal-Flow Post-Implementation Critic` template from `.agent/templates/new-sdlc-subagents.prompt.template` with `governance-schema.md` first, then only the remaining governing artifact references listed in Inputs and the worktree path. If changed target-repo governance or skill-definition files are discoverable through the critic's tool access, the critic reviews them directly. If review would require information outside the approved mission, the phase-allowed artifacts, or tool-accessible data, do not brief the critic; follow `.agent/schemas/abort-protocol.md` instead. If the first critic approves, spawn a second fresh critic with the same allowed inputs and prompt template. If a required critic cannot be spawned, follow Required Critic Availability before taking any other action.

- If the first critic rejects: the lead agent fixes the issues in the worktree (or instructs the dev subagent to fix them), re-runs the full regression suite, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh first critic. Repeat until approval, or escalate to the user if stuck.
- If the first critic approves and the second critic approves: create the commit or commits needed to leave the approved implementation clean in the worktree, then proceed to Phase: Cleanup.
- If the second critic rejects but the approved `mission.md` remains correct: the lead agent fixes the issues in the worktree (or instructs the dev subagent to fix them), re-runs the full regression suite, re-verifies all acceptance criteria, and resubmits the updated diff to a fresh first critic. Repeat until both approve, or escalate to the user if stuck.
- If either spawned critic rejects because the mission itself must change: follow `.agent/schemas/abort-protocol.md`.

Write/update `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md`.

### Phase: Cleanup

Before deleting any files, rewrite `handoff.md` at the worktree root per `.agent/schemas/handoff-protocol.md` with Next / Ongoing Step set to `Phase: Cleanup - apply the target repo's commit/merge rules if any, verify the worktree is clean, then remove mission.md, completion-review runtime artifacts, and handoff.md last, then immediately present results to the user in the same turn.` Cleanup may begin only after the approved implementation changes have been committed following the applicable post-implementation review approval.

Cleanup follows the target repo's commit/merge rules. If the target repo's governing artifacts require or permit merging the approved worktree branch before worktree removal, apply those rules. If the target repo defines no merge rule, default to commit-only and do not auto-merge. Any cleanup-phase merge attempted before worktree removal that is non-trivial per the harness repo-root `CLAUDE.md` `Trivial Merge Qualification` invariant must reset the mission to the applicable completion-review phase: do not continue Cleanup, rewrite `handoff.md` so Next / Ongoing Step names the applicable completion-review phase for the merged state, and resume from that review phase with fresh critic approval before any further cleanup. If a required or permitted cleanup merge fails for any other reason, leave the worktree in place and report the failure to the user.

Then remove `mission.md` if it still exists and `handoff.md` last from the worktree root. If cleanup is interrupted or any deletion fails before `handoff.md` is removed, leave that latest `handoff.md` state in place so the next session can resume cleanup deterministically. After both runtime artifacts are removed, verify that the worktree has no uncommitted changes before removing it. Run `git status` in the worktree and check for unstaged modifications, staged-but-uncommitted changes, and untracked files. If any uncommitted changes are detected, do not remove the worktree — stop, report the uncommitted state to the user (listing the affected files), and leave the worktree in place. Only when the worktree is clean (all changes committed to the branch) proceed to remove the worktree via `git worktree remove --force`. If worktree removal fails, leave the worktree in place and report the failure to the user. Cleanup completion is the end of the mission lifecycle. Immediately after cleanup succeeds, present results to the user.

# Beliefs

## Fast-Path Preference
Mission Creation should make a good-faith attempt to keep a request on fast path whenever no fast-path disqualifier is already known. If a fast-path eligibility fact is still unknown but is plausibly true and can be checked during lite review, execution, or post-implementation review, the lead agent should capture it as an explicit `Assumptions` entry in `mission.md` instead of forcing normal flow up front. These assumptions are provisional: they do not waive the fast-path rules, and fast path must be abandoned as soon as review or execution disproves any of them.

# Considerations

## Redundancy Rationale

Under the current workflow, the full test suite runs twice: once during TDD Final Verification (pre-merge) and again during completion-review (post-merge) when writing runtime artifacts. The pre-merge run is redundant because the post-merge run is authoritative — it validates the implementation against the latest integrated state. Removing the pre-merge run eliminates wasted compute without reducing confidence, since the post-merge run is mandatory regardless of merge triviality.

## Merge Gate
Run before completion review to classify a merge and, on a non-trivial result, rewrite `handoff.md` with the correct phase-reset text. Two subcommands:
- `python3 -m scripts.merge_gate check-dirty <worktree_path>` — Prints `CLEAN` or `DIRTY` with affected paths; exits 0 (clean) or 1 (dirty).
- `python3 -m scripts.merge_gate do-merge <git_work_dir> <handoff_dir> <variant> <branch>` — Valid variants for this skill: `new-sdlc-fast-path`, `new-sdlc-normal`. Exit codes: 0 trivial, 1 invalid variant, 2 non-trivial (handoff rewritten), 3 merge error, 4 non-trivial but handoff absent.
