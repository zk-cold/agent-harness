# Governance Audit Notes

Audit run on 2026-04-28 against `main` HEAD `4967396`. Review surface is the 17 paths required by `.claude/commands/audit.md` `## Review Surface Discovery`.

## Reviewed paths
- `CLAUDE.md`
- `AGENTS.md`
- `.claude/commands/audit.md`
- `.claude/commands/new-sdlc.md`
- `.agent/schemas/abort-protocol.md`
- `.agent/schemas/critic-protocol.md`
- `.agent/schemas/fast-path-impl-critic-protocol.md`
- `.agent/schemas/fast-path-impl-protocol.md`
- `.agent/schemas/governance-schema.md`
- `.agent/schemas/handoff-protocol.md`
- `.agent/schemas/impl-critic-protocol.md`
- `.agent/schemas/mission-critic-protocol.md`
- `.agent/schemas/mission-schema.md`
- `.agent/schemas/recovery-protocol.md`
- `.agent/schemas/sde-protocol.md`
- `.agent/schemas/sdet-protocol.md`
- `.agent/schemas/test-critic-protocol.md`

## Worktree proposal detection
The active worktree (main repo root) is at `4967396` with a clean working tree before this run. The secondary worktree at `.claude/worktrees/audit-governance` is on commit `b2c8b32` (an ancestor of `4967396`) with a clean tree, so per `audit.md` `## Worktree Proposal Detection` it is **not** treated as a proposal — repo-root copies are authoritative and there are no "changed worktree copies" to inspect.

# Contradictions

- **Test-Only `Already-Satisfied Behavior` scope.** `.agent/schemas/mission-schema.md` (`## Test-Only Scope Qualification`) restricts the qualifier to "every invariant or external constraint that the mission proposes for **test persistence**". `.agent/schemas/mission-critic-protocol.md` (`## Test-Only Validation`) rejects when "**any** proposed invariant or external constraint is not explicitly qualified as `Already-Satisfied Behavior`". A Test-Only mission that proposes an invariant with `_persist: <governed-document>_` (text persistence) satisfies the schema but is rejected by the critic.

- **Handoff resumption versus recovery applicability.** `.agent/schemas/handoff-protocol.md` (`## Resumption`) sends every "not resumable" path — including the case where `handoff.md` does not exist — to `recovery-protocol.md`. `.agent/schemas/recovery-protocol.md` (`## Governance Scope`) declares that document applies *only* when `handoff.md` records the mission in aborted state. The no-`handoff.md` and "exists but not aborted-and-not-resumable" cases are routed to a protocol that explicitly excludes them.

- **Greenfield Baseline rule vs. its own numbered steps.** `.claude/commands/new-sdlc.md` `### Coverage Verification` `#### Greenfield Baseline` opens with "When no prod-scope code touched by the mission exists yet (greenfield), record baseline coverage as N/A." It then enumerates steps 1–3 that *measure* baseline coverage and abort if it is below threshold. Under the greenfield rule there is nothing to measure, so the rule and the numbered steps cannot both apply to the greenfield case as the heading implies.

- No contradictions found in:
  `CLAUDE.md`,
  `AGENTS.md`,
  `.claude/commands/audit.md`,
  `.agent/schemas/abort-protocol.md`,
  `.agent/schemas/critic-protocol.md`,
  `.agent/schemas/fast-path-impl-critic-protocol.md`,
  `.agent/schemas/fast-path-impl-protocol.md`,
  `.agent/schemas/governance-schema.md`,
  `.agent/schemas/impl-critic-protocol.md`,
  `.agent/schemas/sde-protocol.md`,
  `.agent/schemas/sdet-protocol.md`,
  `.agent/schemas/test-critic-protocol.md`.

# Ambiguities

- **Relatedness test cited but not defined.** `CLAUDE.md` (`## Bootstrap Check`) states the relatedness test is "defined in `.agent/schemas/handoff-protocol.md` and `.claude/commands/new-sdlc.md`", but neither file actually defines such a test. `new-sdlc.md` `## Phase: Mission Creation` step 2 only uses the bare phrase "related `handoff.md`" without specifying how relatedness is determined.

- **Fast-path eligibility asymmetry between mission-time and impl-time.** `mission-schema.md` `## Prefer Fast Path` and `mission-critic-protocol.md` `## Fast-Path Eligibility` cap governance modifications/removals at three and ban consideration overrides. `fast-path-impl-critic-protocol.md` `## Fast-Path Eligibility Verification` adds a "no more than 7 git-tracked files have uncommitted changes" cap not present at mission time. Whether this asymmetry is intentional, and whether the mission-critic should preview the file-count cap, is unclear.

- **`fast-path-impl-critic-protocol.md` "git-tracked files with uncommitted changes" boundary.** It is unstated whether the cap counts files that were newly created and `git add`ed during the mission, untracked files, or only modifications to previously-committed files. Combined with `fast-path-impl-protocol.md` `## Leave Changes Uncommitted`, the boundary materially changes which fast-path missions remain eligible.

- **`fast-path-impl-protocol.md` "once locked".** Steps 1b and 3b say "Verification against `sdet-protocol.md` — once locked, no further additions/modifications/deletions" without specifying what the lock applies to: only test files, all worktree files, or only tests expressing hard constraints.

- **`mission-critic-protocol.md` fast-path identification channel.** `## Fast-Path Eligibility` triggers "When the review context explicitly identifies the mission as fast-path", but no document specifies how that identification reaches the critic — via the prompt context, a flag in `mission.md`, or another channel.

- **`audit.md` "changed worktree copy" definition.** `## Worktree Proposal Detection` does not define "changed": differs from `HEAD`, has uncommitted changes, or differs from the most recent merge-base. When the active worktree is itself the repo root, the repo-root vs. proposal distinction also collapses.

- **`mission-schema.md` "respective optional sections" and `mission-critic-protocol.md` violation-resolution location.** `## Full Texts for Governance Artifacts` requires text "in their respective optional sections" without naming or defining those sections. `mission-critic-protocol.md` `## Mission Justification` requires "a consideration about violation-resolution" without saying where in `mission.md` that consideration belongs.

- **`recovery-protocol.md` reset baseline.** `## Reuse Worktree` says "Any governed document by `governance-schema.md` must be reset" without naming the source of truth (`HEAD`, root branch tip, last approved mission state, etc.).

- **`new-sdlc.md` `## Phase: Cleanup` "runtime artifacts".** "Remove runtime artifacts (`handoff.md` last)" does not enumerate the artifacts. Likely candidates include `mission.md`, `test-output.txt`, `coverage-output.txt`, `lint-output.txt`, and audit `TODO.md`, but the set must be made explicit for cleanup to be reproducible.

- **Coverage threshold override location.** `new-sdlc.md` `## Default Coverage Threshold` permits a target repo's hard constraints or considerations to override 80% but does not specify where the override is recorded (target-repo `CLAUDE.md`, `mission.md`, an external constraint), so SDE and impl-critic cannot deterministically discover the effective threshold.

- **`new-sdlc.md` Phase: SDE Execution HEAD-hash failure path.** "validate HEAD hash against recorded test commit" prescribes the check but not what to do on mismatch (abort? escalate? re-run?). The next behavior is left implicit.

- **Fast-Path Post-Impl Critic reject-cause routing.** `new-sdlc.md` `## Phase: Fast-Path Post-Impl Critic` distinguishes "Reject (by fast-path eligibility)" from generic "Reject" with different downstream phases, but `critic-protocol.md` requires `REJECT` with free-form reasons. No structured signal lets the lead deterministically pick the path.

- **`sde-protocol.md` `## Final Verifications` test-output coupling.** The numbered procedure runs coverage (1), optional lint (2), then merges the root branch (3); it does not call out a test run. The trailer nonetheless requires raw output from tests to be written to `test-output.txt`. Whether tests must be re-run after the root-branch merge in step 3, or whether prior test output suffices, is unstated.

- **`sdet-protocol.md` external-constraint anchoring location.** `## Document External Constraints` requires anchor info, but `## No Governed Document Changes` blocks writing it to governed prose files. The protocol does not specify whether anchors belong in test names, code comments, fixtures, or elsewhere.

- **`sdet-protocol.md` API-change exception.** `## No Prod-Scope Code` exempts "an API change made explicit in the mission". "API change" is undefined here; `new-sdlc.md` `## API Design` only describes the form an API design takes (invariant or external constraint). The interaction with TDD's test-first ordering is also unstated.

- **`critic-protocol.md` `## Counting Governance Artifacts` unit for tests.** "Each semantically-modified test count as 1 change in its respective category" does not say whether the unit is per file, per test case, or per hard constraint expressed by the test.

- **`test-critic-protocol.md` `## Hard Constraint Coverage` scope.** "Every testable invariant or external constraint must have a corresponding test" does not scope the rule to mission-affected constraints; read literally it imposes a whole-repo completeness check on every test review.

- **`handoff-protocol.md` "resumable" defined out of band.** `## Resumption` keys behavior on whether the mission is "resumable" without defining it. The operational definition lives in `scripts/bootstrap_check` (`RESUMABLE` / `ABORTED` / `NO_HANDOFF`) and is referenced from `CLAUDE.md`, but not from this protocol.

- **`abort-protocol.md` worktree lifecycle.** `## Worktree Preservation` forbids removing the worktree during abort but does not specify when, or by what command, a permanently-aborted worktree is eventually cleaned up. This permits unbounded worktree accumulation.

- **`AGENTS.md` `## Slash Commands` classification.** "/name commands are interpreted as .claude/commands/name.md" documents Claude Code runtime behavior, not a default-binding rule on agent behavior. Whether this passes `governance-schema.md` `## Consideration Qualification` (especially the "obvious enough that it adds no interpretive or implementation value" disqualifier) is debatable.

- No material ambiguities found in:
  `.agent/schemas/governance-schema.md`,
  `.agent/schemas/impl-critic-protocol.md`.

# Markdown to Script Conversions

- **Audit surface discovery and TODO render** (`.claude/commands/audit.md` `## Review Surface Discovery`, `## Deliverable Structure`, `## TODO Lifecycle`). Add `python3 -m scripts.governance_audit` that enumerates the mandated review surface, lints `TODO.md` for the three required sections, and (in a `--gate` mode) verifies that the active `mission.md` accounts for every concrete item under Contradictions / Ambiguities / Markdown to Script Conversions before allowing TODO removal.

- **Session routing and worktree relatedness** (`CLAUDE.md` `## Bootstrap Check`, `.agent/schemas/handoff-protocol.md` `## Resumption`, `.agent/schemas/recovery-protocol.md` `## Governance Scope`, `.claude/commands/new-sdlc.md` `## Phase: Mission Creation`). Extend `scripts.bootstrap_check` (or add `scripts/session_router`) so the relatedness test, RESUMABLE/ABORTED/NO_HANDOFF classification, and the next required action are produced by code rather than re-derived from prose every session.

- **Mission validator** (`mission-schema.md`, `mission-critic-protocol.md`). Extend the existing `scripts/mission_linter` to enforce: structural completeness, exactly-one delivery mode, full text for governance artifacts, the persistence trailer (`_transient_` / `_persist:`), Test-Only `Already-Satisfied Behavior` qualification, Stubbing Policy and Runtime-Patching Policy invariants for `TDD`/`Test-Only`, and the violation-resolution location once the location ambiguity is resolved.

- **Fast-path eligibility check** (`fast-path-impl-critic-protocol.md` `## Fast-Path Eligibility Verification`, `mission-schema.md` `## Prefer Fast Path`, `mission-critic-protocol.md` `## Fast-Path Eligibility`). Add `python3 -m scripts.fast_path_eligibility` that counts modified/removed governance artifacts (using `governance-schema.md` `## Governed Documents` globs) and counts uncommitted changes per the resolved boundary (see ambiguity above). Output `ELIGIBLE` or `INELIGIBLE: <reason>` so both mission-time and impl-time critics consume the same answer.

- **Phase verifier for SDE/SDET artifacts** (`fast-path-impl-protocol.md`, `sde-protocol.md`, `sdet-protocol.md`, `impl-critic-protocol.md`, `test-critic-protocol.md`). Add `python3 -m scripts.phase_verifier` that checks for the required runtime artifacts (`test-output.txt`, `coverage-output.txt`, `lint-output.txt`), validates coverage threshold compliance against the resolved override location, and (for fast path) checks dirty-file count and TDD-exempt / Test-Only artifact-class constraints.

- **Recovery reset of governed documents** (`recovery-protocol.md` `## Reuse Worktree`). Once the reset baseline is named (see ambiguity), wrap the action as `python3 -m scripts.recovery_reset_governed`, performing `git checkout <baseline> -- CLAUDE.md AGENTS.md .agent/schemas/ .claude/commands/`.

- **Cleanup orchestration** (`new-sdlc.md` `## Phase: Cleanup`). Once "runtime artifacts" is enumerated, wrap the sequence (remove artifacts, verify clean, `git worktree remove`) as `python3 -m scripts.cleanup_worktree`.

- **Abort marker writer** (`abort-protocol.md` `## Abort Marker`). Add `python3 -m scripts.handoff_abort "<blocker summary>"` that updates `handoff.md` consistently with `.agent/templates/handoff.md`.

- **Test-commit hash validation** (`new-sdlc.md` `## Phase: SDE Execution`). After the failure path is defined, wrap the validation as `python3 -m scripts.validate_test_hash <hash>` (e.g., `git merge-base --is-ancestor`).

- **Trivial-merge classifier** (`CLAUDE.md` `## Trivial Merge Qualification`). Largely covered by `scripts/merge_gate`; verify it surfaces a single boolean (`TRIVIAL` / `NON_TRIVIAL: <reason>`) directly callable from `new-sdlc.md` `## Phase: Cleanup`.

- Procedures already script-backed (no new conversion needed):
  - `CLAUDE.md` `## Bootstrap Check` → `scripts/bootstrap_check`.
  - `handoff-protocol.md` `## Handoff Template` → `scripts/handoff_generator`.
  - `mission-schema.md` `## Mission Template` → `scripts/mission_generator`.

- No additional script-conversion candidates identified in:
  `AGENTS.md`,
  `.agent/schemas/critic-protocol.md` (qualitative review semantics; only the `APPROVE`/`REJECT` shape is mechanically checkable, already feasible inside any critic-spawning script),
  `.agent/schemas/governance-schema.md` (definitional content),
  `.agent/schemas/test-critic-protocol.md` (qualitative review semantics).
