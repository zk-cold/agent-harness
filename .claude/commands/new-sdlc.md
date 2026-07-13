# Invariants

## Flow Order
For a fresh request, follow the phases in order.

## Target Repo Governance Precedence
When operating inside a target repo, that repo's hard constraints and considerations govern ahead of this harness's considerations.

## Handoff Resumption
On session start, follow `handoff-protocol.md`. The recorded **Next / Ongoing Step** must map clearly to a phase in this document.

## Required Sub-Agent Availability
Sub-agent requiring phases are blocking. If a required sub-agent cannot be spawned, write `handoff.md` with the blocker, and surface it to the user.

## Sub-Agent Prompt Discipline
All prompts must be instantiated from `new-sdlc-prompts.md`.

## Approved Mission Immutability
Once approved, `mission.md` must not be modified.

## Mission-Draft Governance Artifact Approval
During Mission Draft, each proposed addition, modification, or removal of a governance artifact must be presented to the user one artifact at a time and must receive user approval before it is included in `mission.md`. If critic feedback requires change, the revised text must get user approval again before resubmission.

## API Design
When a mission introduces or changes an API, the lead writes the minimum prod-scope scaffolding (signatures, type declarations, module skeletons) before handing off to the SDET.

## Coverage Tool Requirement
When TDD applies, a working coverage tool must be in place before the Mission Draft step in Phase: Mission Creation.

## Test-Only Routing
A mission declared `Test-Only` must stay on fast path and must not enter normal-flow execution phases.

## Mission-Draft Challenger
During Mission Draft, a fresh challenger sub-agent must challenge every governance artifact proposed or revised in the draft, and an artifact may be presented to the user for approval under `Mission-Draft Governance Artifact Approval` only after it survives a challenge or the dev overturns every adverse disposition against it.

## Adversarial Feedback Alignment
Before the lead revises a draft in response to adversarial feedback — a challenger disposition or a critic rejection — that feedback and the lead's evaluation of whether the revision aligns with or contradicts the `## Dev Interview Transcript` of `handoff.md` must be recorded in that file's `## Known Failed Attempts`. A revision the lead judges to contradict dev intention must be flagged to the dev rather than carried silently forward.

## Lead Context Is Facts Only
Lead-authored context injected into a sub-agent prompt must state only facts, never instructions to the sub-agent.

# Considerations

## Abort
The term "abort" in this document refer to the actions specified by `abort-protocol.md`.

## Update `handoff.md`
This happens at start of any phase, except `Phase: Mission Creation`.

## Resubmissions
Each critic round spawns a fresh critic agent. Executor sub-agents (SDE, SDET) persist across fix-and-resubmit cycles within a phase.

## Default Coverage Threshold
The default coverage threshold is 80% line coverage on modified code.

## Reframe Procedural Steps as Deliverables
During the Interview and Mission Draft steps, each procedural step should be reframed as a concrete deliverable before it enters mission scope.

## Challenger Checks
The challenge is confined to these three checks, in priority order:
1. Conformance to the content and disqualification clauses of `governance-schema.md`.
2. For a proposed invariant, whether it is a real business mandate rather than an external constraint or a derived implementation detail, dispositioned per `Invariant Business-Mandate Triage`.
3. Whether the artifact carries lasting governance value beyond the mission.

## Invariant Business-Mandate Triage
A proposed invariant that the challenger finds is not a real business mandate does not survive as an invariant: an external constraint is reclassified as an external constraint; a derived implementation detail is rewritten as an accompanying consideration when non-obvious, or dropped when obvious. When the challenger cannot cleanly classify the invariant among business mandate, external constraint, and derived implementation detail, the lead prompts the dev for clarification and applies no disposition until the classification is resolved.

## Phase: Mission Creation
1. Identify target repo
2. Check for `.claude/worktrees/*/` for related `handoff.md` and follow `handoff-protocol.md` if so
3. Otherwise, create fresh worktree. Initialize `handoff.md` following `handoff-protocol.md`
4. Loop **interview -> coverage tooling gate -> mission draft -> coverage verification -> update `handoff.md` -> submission** until approved
### Interview
For any single invariant requested, try ask questions to uncover if there is actually an external constraint / consideration / belief behind it.
### Coverage Tooling Gate
When the Coverage Tool Requirement blocks mission drafting, the lead confirms or suggests the tech stack with the user and sets up the applicable coverage tool before proceeding.
### Mission Draft
Follow `mission-schema.md`.
### Coverage Verification
Run per submission, unless the mission is `TDD-exempt` or `Test-Only`, or there has been no change to prod-scope code since the previous run.
#### Baseline Coverage
- **Greenfield (no prod-scope code touched by the mission exists yet):** record baseline coverage as N/A.
- **Non-greenfield:**
  1. Measure and record baseline coverage against the prod-scope code touched by the mission.
  2. If the baseline coverage is below threshold, abort, surfacing the insufficient baseline coverage and the affected code.
  3. If baseline coverage is satisfactory, record a transient consideration in the mission.
### Submission
Submit to 1 agent using `Fast-Path Mission Creation Critic` template when the mission is `Test-Only` or fast-path is plausible. Enter `Phase: Fast-Path Execution` if approved.
Submit to 2 sequential agents using `Mission Creation Critic` for normal flow. If approved by both critics, enter `Phase: SDET Execution`.

## Phase: Fast-Path Execution
1. Close mission-critic agents.
2. Follow `fast-path-impl-protocol.md`. 
3. Enter `Phase: Fast-Path Post-Impl Critic`

## Escalation to Normal Flow
1. Discard all worktree changes except `handoff.md` and `mission.md`
2. If `mission.md` needs change, abort
3. Otherwise, 1 agent using `Mission Creation Critic` template. If approved, start `Phase: SDET Execution`. Abort otherwise

## Phase: Fast-Path Post-Impl Critic
Spawn agent using `Fast-Path Post-Impl Critic` template.
- Approve -> `Phase: Cleanup`
- Reject (by fast-path eligibility) -> `Escalation to Normal Flow`
- Reject -> fix and resubmit if `mission.md` remains good. Abort otherwise

## Phase: SDET Execution
Close mission/escalation critic agents.
If mission is `TDD-exempt`, enter `Phase: SDE Execution`.
If mission is `Test-Only`, abort because routing has violated `Test-Only Routing`.
Otherwise, spawn agent using `SDET Execution` template.
### Submission
When SDET reports ready, enter `Phase: Test Critic`.

## Phase: Test Critic
Spawn agent using `Test Critic Review` template.
- Approve -> `Phase: Test Commit`
- Reject -> abort if `mission.md` requires change. Otherwise delegate the feedback to the SDET agent. Wait for its fix & resubmit.

## Phase: Test Commit
Commit the changes and **record the hash**. Close SDET and test-critic agents. Enter `Phase: SDE Execution`.

## Phase: SDE Execution
Spawn agent using `SDE Execution` template.
### Submission
When SDE reports ready:
1. If a test commit hash was recorded for this mission, validate that `HEAD` exactly matches it; on mismatch, abort.
2. Fetch and merge the target repo's root branch into the worktree. Abort if the merge is not `Already up to date.` or a clean fast-forward, so that the SDE's pre-merge `test-output.txt` remains canonical.
3. Enter `Phase: Post-Impl Critic`.

## Phase: Post-Impl Critic
Spawn 1 agent using `Post-Impl Critic` template.
- Approve -> `Phase: Cleanup`
- Reject -> abort if `mission.md` requires changes. Otherwise delegate the feedback to the SDE agent. Wait for its fix & resubmit.

## Phase: Cleanup
Close all sub-agents.
Apply target repo's commit/merge rules (default: commit-only). If the merge back is not trivial, reset to the applicable post-impl critic phase.
After the commit/merge step completes, remove every remaining uncommitted file under the worktree root (with `handoff.md` removed last), verify worktree clean, and do `git worktree remove`.
Present results to user.
