# Repository Governance Review

## Reviewed Files

### Authoritative files inspected
1. `CLAUDE.md`
2. `AGENTS.md`
3. `.agent/schemas/abort-protocol.md`
4. `.agent/schemas/critic-protocol.md`
5. `.agent/schemas/fast-path-impl-critic-protocol.md`
6. `.agent/schemas/fast-path-impl-protocol.md`
7. `.agent/schemas/governance-schema.md`
8. `.agent/schemas/handoff-protocol.md`
9. `.agent/schemas/impl-critic-protocol.md`
10. `.agent/schemas/mission-critic-protocol.md`
11. `.agent/schemas/mission-schema.md`
12. `.agent/schemas/recovery-protocol.md`
13. `.agent/schemas/sde-protocol.md`
14. `.agent/schemas/sdet-protocol.md`
15. `.agent/schemas/test-critic-protocol.md`
16. `.claude/commands/new-sdlc.md`

### Changed worktree proposal copies inspected
None. All governance files matched their committed versions.

---

## Contradictions

### C1. Phase name mismatch in `new-sdlc.md`
- **Phase: Fast-Path Execution** step 3 says "Enter `Phase: Fast-Path Critic`" (`.claude/commands/new-sdlc.md`, line 63).
- The actual phase heading is **"Phase: Fast-Path Post-Impl Critic"** (`.claude/commands/new-sdlc.md`, line 71).
- These names do not match; a routing agent following the literal reference will fail to locate the correct phase.

### C2. Top-level section violation in `recovery-protocol.md`
- `governance-schema.md` **Allowed Top-Level Sections** invariant: "Governed documents may only define governance artifacts, with their category being top-level sections."
- `governance-schema.md` **Governance Artifacts** invariant defines those categories as **Invariants**, **External Constraints**, and **Considerations**.
- `.agent/schemas/recovery-protocol.md` line 3 introduces `# Governance Scope` as a top-level section, which is not a governance artifact category. This violates the structural invariant.

### C3. Singular vs plural section name in `fast-path-impl-protocol.md`
- `governance-schema.md` defines the governance artifact category as **Considerations** (plural).
- `.agent/schemas/fast-path-impl-protocol.md` line 17 uses `# Consideration` (singular).
- A strict parser or validator treating these as distinct section names would flag this as a non-conforming top-level section, same class of violation as C2.

### C4. Meta Governance vs External Constraints as a governance artifact
- `CLAUDE.md` **Meta Governance** invariant bars governed files from containing an `# External Constraints` section.
- `governance-schema.md` defines **External Constraints** as a governance artifact category and provides content and qualification rules for it.
- These two invariants are logically compatible only if no governed file within this harness will ever need external constraints. The governance schema defines a category that the meta governance invariant makes structurally impossible to use. If external constraints arise (e.g., a third-party API contract), there is no compliant place to record them in a governed file.

---

## Ambiguities

### A1. Incomplete sentence in Coverage Verification (`new-sdlc.md`, line 54)
> "If the baseline coverage is below threshold, follow  identifying the insufficient baseline coverage and the affected code."

The word "follow" is followed by a double space and no protocol or document reference. The action to take when baseline coverage is insufficient is undefined.

### A2. Coverage threshold never defined
Multiple files reference a "coverage threshold" (`new-sdlc.md` Coverage Verification, `sde-protocol.md` Final Verifications, `impl-critic-protocol.md` Coverage Threshold Verification) but no governance file defines what that threshold is, how it is configured, or where to look for a project-specific value.

### A3. "Runtime artifacts" location and naming unspecified
`sde-protocol.md` **Final Verifications** requires writing raw output from tests, coverage, and linter to "dedicated files under worktree root." `impl-critic-protocol.md` references "runtime artifacts provided for review." Neither specifies file names, formats, or a discovery convention, leaving the SDE and critic to guess.

### A4. Missing "Test Critic Review" prompt template
`.claude/commands/new-sdlc.md` **Phase: Test Critic** references spawning an agent using the "Test Critic Review" template. `.agent/templates/new-sdlc-prompts.md` contains templates for: Fast-Path Mission Creation Critic, Mission Creation Critic, Fast-Path Post-Impl Critic, SDET Execution, SDE Execution, and Post-Impl Critic. No "Test Critic Review" template exists. This makes Phase: Test Critic unexecutable per the Sub-Agent Prompt Discipline invariant.

### A5. Resubmission scope vs feedback delegation
`.claude/commands/new-sdlc.md` **Resubmissions** consideration says "Each resubmission is to a new agent." However, several phases (Post-Impl Critic, Fast-Path Post-Impl Critic, Test Critic) instruct the lead to "delegate the feedback to the [existing] agent" and "wait for its fix & resubmit." It is unclear whether the subsequent critic review of the fix counts as a "resubmission" requiring a fresh agent, or whether only the initial submission to a critic phase counts.

### A6. Typo "most not" in Approved Mission Immutability (`new-sdlc.md`, line 19)
> "Once approved, `mission.md` most not be modified."

Should read "must not." As written, this is not objectively testable from its own wording, which could technically disqualify it as an invariant under `governance-schema.md` Invariant Qualification.

### A7. Typo "bliefs" in `fast-path-impl-critic-protocol.md` (line 6)
> "There are overrides to considerations or bliefs"

Should read "beliefs." Also, "beliefs" is not a governance artifact category defined in `governance-schema.md`. This may be an intended synonym for considerations, or it may reference an undefined concept.

### A8. Typo "bevhior" in `governance-schema.md` (line 67)
> "shape agent bevhior"

Should read "behavior." This is in the Code Comments consideration and does not affect enforceability, but reduces document quality.

### A9. Typo "reviwer cna" in `mission-critic-protocol.md` (line 19)
> "a reviwer cna determine pass/fail"

Should read "a reviewer can."

### A10. Typo "escaltion" in `new-sdlc.md` (line 78)
> "Close mission/escaltion critic agents."

Should read "escalation."

### A11. Typo "Excemption" in `impl-critic-protocol.md` (line 10)
> "TDD Excemption"

Should read "Exemption."

---

## Markdown to Script Conversions

### S1. Governed-document structural validator
**Source procedures**: `governance-schema.md` Allowed Top-Level Sections, Governance Artifacts definitions.
**Proposed automation**: A script that parses every governed document (`AGENTS.md`, `CLAUDE.md`, `.agent/schemas/*.md`, `.claude/commands/*.md`) and verifies that all top-level (`#`) headings are governance artifact categories (`Invariants`, `External Constraints`, `Considerations`). Would have caught C2 and C3 above.

### S2. Meta Governance `# External Constraints` check
**Source procedure**: `CLAUDE.md` Meta Governance invariant.
**Proposed automation**: A script (or extension of S1) that verifies no governed file contains an `# External Constraints` section. Single `grep -l` across the governed file set.

### S3. Fast-path eligibility checker
**Source procedures**: `mission-critic-protocol.md` Fast-Path Eligibility, `fast-path-impl-critic-protocol.md` Fast-Path Eligibility Verification.
**Proposed automation**: A script that, given a worktree, counts governed artifact changes (new/modified/removed), checks for consideration overrides, and counts git-tracked files with uncommitted changes. Outputs pass/fail with details.

### S4. Cross-reference link validator
**Source**: Phase name references throughout `new-sdlc.md`, protocol cross-references across all schemas.
**Proposed automation**: A script that extracts all backtick-quoted phase names and file references from governance Markdown and validates they resolve to actual headings or file paths. Would have caught C1 and A4.

### S5. SDE final-verification runner
**Source procedure**: `sde-protocol.md` Final Verifications.
**Proposed automation**: A script that runs the test suite, measures coverage against a configured threshold, runs formatter/linter if available, and fetches/merges from root branch — collecting all outputs into named files under worktree root. Addresses A3 by standardizing output file names.

### S6. Trivial merge check
**Source procedure**: `CLAUDE.md` Trivial Merge Qualification.
**Proposed automation**: A script that attempts a `git merge --no-commit --no-ff` and checks if the result is "Already up to date" or a clean fast-forward, then aborts the merge. Returns pass/fail for use in Phase: Cleanup.

### S7. Prompt template completeness check
**Source**: `new-sdlc.md` Sub-Agent Prompt Discipline invariant, phase definitions referencing templates.
**Proposed automation**: A script that extracts all template names referenced in `new-sdlc.md` and verifies each has a corresponding heading in `new-sdlc-prompts.md`. Would have caught A4.

### S8. Governance typo/quality linter
**Source**: Various typos found across governance files (A6-A11).
**Proposed automation**: A spellcheck pass (e.g., `cspell` or `aspell`) configured with a project-specific dictionary, run as a pre-commit hook on governed Markdown files.
