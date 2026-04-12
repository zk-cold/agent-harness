# Governance Audit Notes

Reviewed authoritative paths:
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

Worktree proposal detection:
- Git reports `.claude/commands/audit.md` as modified in the active worktree, but `git diff -- .claude/commands/audit.md` is textually empty. I therefore treated `HEAD:.claude/commands/audit.md` as the authoritative copy and the worktree copy as a content-equivalent proposal.

# Contradictions

- `CLAUDE.md` (`Bootstrap`) says every prompt must be handled with `/new-sdlc`. `AGENTS.md` (`Slash Commands`) says `/name` routes to `.claude/commands/name.md`. `.claude/commands/audit.md` defines a standalone `/audit` command with its own deliverable and read-only rules. Those three rules cannot all be simultaneously operative for a direct `/audit` invocation in this harness.

- `.agent/schemas/handoff-protocol.md` (`Resumption`) says that when `handoff.md` is absent or the mission is not resumable, the agent must follow `recovery-protocol.md`. `.agent/schemas/recovery-protocol.md` (`Governance Scope`) says recovery applies only when `handoff.md` records the mission in aborted state. The no-`handoff.md` path required by `handoff-protocol.md` is therefore outside `recovery-protocol.md`'s stated scope.

- No contradictions found in:
  `CLAUDE.md` beyond the bootstrap conflict above,
  `AGENTS.md` beyond the slash-command conflict above,
  `.claude/commands/audit.md` beyond the bootstrap conflict above,
  `.claude/commands/new-sdlc.md`,
  `.agent/schemas/abort-protocol.md`,
  `.agent/schemas/critic-protocol.md`,
  `.agent/schemas/fast-path-impl-critic-protocol.md`,
  `.agent/schemas/fast-path-impl-protocol.md`,
  `.agent/schemas/governance-schema.md`,
  `.agent/schemas/impl-critic-protocol.md`,
  `.agent/schemas/mission-critic-protocol.md`,
  `.agent/schemas/mission-schema.md`,
  `.agent/schemas/sde-protocol.md`,
  `.agent/schemas/sdet-protocol.md`,
  `.agent/schemas/test-critic-protocol.md`.

# Ambiguities

- `CLAUDE.md` (`Bootstrap Check`) says the relatedness test is defined in `.agent/schemas/handoff-protocol.md` and `.claude/commands/new-sdlc.md`, but neither reviewed file defines such a test. `.claude/commands/new-sdlc.md` also uses the phrase "related `handoff.md`" without defining how relatedness is determined.

- `.claude/commands/audit.md` (`Worktree Proposal Detection`) does not specify what counts as the authoritative repo-root copy when the active worktree is itself the repo root and the changed file has the same pathname. This audit had to infer that `HEAD` is the authoritative source.

- `.agent/schemas/mission-schema.md` (`Full Texts for Governance Artifacts`) requires "their respective optional sections", but it does not name those sections or define their structure. `.agent/schemas/mission-critic-protocol.md` (`Mission Justification`) also requires a mission to include "a consideration about violation-resolution" without saying where that consideration belongs in the mission document.

- `.agent/schemas/fast-path-impl-protocol.md` (`TDD Flow`, step 2) says "once locked, no further additions/modifications/deletions" without specifying what becomes locked: tests, all files, only hard-constraint tests, or the full worktree state.

- `.agent/schemas/sde-protocol.md` (`Final Verifications`) requires writing raw output from tests, coverage, and linting to fixed files, but the numbered procedure explicitly requires coverage and optional linting, not a final test run. `.agent/schemas/impl-critic-protocol.md` (`Test Result Verification`) then requires the implementation review to trust `test-output.txt`. The docs do not say whether SDE must rerun tests after implementation changes, after merging the root branch, or both.

- `.agent/schemas/recovery-protocol.md` (`Reuse Worktree`) says governed documents in the existing worktree "must be reset" but does not say reset to what source of truth: `HEAD`, the root branch tip, the last approved mission state, or something else.

- `.agent/schemas/sdet-protocol.md` (`Document External Constraints`) requires each external constraint to be documented with anchor info, but `No Governed Document Changes` prevents putting that documentation into governed prose files. The protocol does not say whether the anchor belongs in test names, code comments, helper data, or some other artifact.

- `.agent/schemas/critic-protocol.md` (`Counting Governance Artifacts`) says each semantically modified test counts as one change in its respective category, but it does not define whether that unit is per file, per test case, or per hard constraint expressed by the test.

- `.agent/schemas/test-critic-protocol.md` (`Hard Constraint Coverage`) says every testable hard constraint must have a corresponding test, but it does not explicitly scope that rule to the mission or to modified constraints. Read literally, it can be interpreted as a whole-repo completeness requirement on every test review.

- No material ambiguities found in:
  `AGENTS.md`,
  `.agent/schemas/abort-protocol.md`,
  `.agent/schemas/fast-path-impl-critic-protocol.md`,
  `.agent/schemas/governance-schema.md`,
  `.agent/schemas/handoff-protocol.md` beyond the missing relatedness definition noted above.

# Markdown to Script Conversions

- `CLAUDE.md`, `AGENTS.md`, `.claude/commands/audit.md`, and `.agent/schemas/governance-schema.md`: add a `scripts/governance_audit` command that discovers the mandated review surface, compares authoritative versus worktree copies, lints for unreachable command routing, and renders `TODO.md` in the required three-section format.

- `CLAUDE.md`, `.claude/commands/new-sdlc.md`, `.agent/schemas/handoff-protocol.md`, and `.agent/schemas/recovery-protocol.md`: extend `scripts.bootstrap_check` or add a `scripts/session_router` that resolves root-artifact state, worktree relatedness, resumable versus aborted routing, and the next required action without leaving those decisions in prose.

- `.agent/schemas/mission-schema.md` and `.agent/schemas/mission-critic-protocol.md`: add a `scripts/mission_validator` check that verifies structural completeness, AC-to-scope mappings, AC-to-governance mappings, persistence AC specificity, TDD-exemption validity, and fast-path eligibility before critic review.

- `.agent/schemas/fast-path-impl-protocol.md`, `.agent/schemas/sde-protocol.md`, `.agent/schemas/sdet-protocol.md`, `.agent/schemas/impl-critic-protocol.md`, `.agent/schemas/test-critic-protocol.md`, and `.agent/schemas/fast-path-impl-critic-protocol.md`: add a `scripts/phase_verifier` that checks required runtime artifacts (`test-output.txt`, `coverage-output.txt`, `lint-output.txt`), validates dirty-file counts for fast path, verifies test/coverage freshness, and enforces phase-specific preconditions.

- `.agent/schemas/critic-protocol.md` and `.claude/commands/new-sdlc.md`: add a prompt-instantiation and response-check script that expands the required critic/SDE/SDET templates and validates that critic responses are exactly `APPROVE` or `REJECT` with reasons.

- No additional conversion candidates found in:
  `.agent/schemas/abort-protocol.md`,
  `.agent/schemas/governance-schema.md` beyond the audit linting candidate above.
