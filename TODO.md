# Governance Audit Findings

Audit of all governed files against `.agent/schemas/governance-schema.md`.

## 2. Governance Schema Violations

### 2.1 Misclassifications

| # | File | Statement | Current | Should Be | Reason |
|---|---|---|---|---|---|
| 2.1.1 | engineering-protocol.md | Governance Persistence | Consideration | Invariant | "Persist...only when a reviewed mission explicitly promotes them" is an always-binding constraint, not supporting detail. Disqualified as consideration per "actually a binding rule." |

### 2.2 Invariant Qualification Failures (Derivability)

The 12 CLAUDE.md duplicates (1.1.1--1.1.12) and AGENTS.md Bootstrap (1.2.1) are also schema violations: each is "already derivable from other governance artifacts" per governance-schema.md Invariant Qualification bullet 3.

### 2.3 Defects in governance-schema.md

The schema declares itself authoritative and agent-uneditable but contains:

| # | Line | Defect |
|---|---|---|
| 2.3.1 | 8 | "External **Contraints**" -- typo, should be "Constraints" |
| 2.3.2 | 16 | Trailing CJK period (U+3002) instead of ASCII period |
| 2.3.3 | 61 | "concrete **enought**" -- typo, should be "enough" |

These require developer action since agents must not edit this file.

### 2.4 Defects in new-sdlc.md

| # | Line | Defect |
|---|---|---|
| 2.4.1 | 41 | "invariant / external **contraint**" -- typo |
| 2.4.2 | 42 | "planned **aritifacts**" -- typo |

---

## 3. Contradictions

### 3.1 engineering-protocol.md "New Test Purpose" vs tdd-protocol.md Step 3 "Fill Coverage Gaps"

- Engineering protocol: "Each new test must express an identified invariant or external constraint. Tests must not be written solely for coverage."
- TDD protocol Step 3: "If the baseline coverage...is below the coverage threshold, write tests to bring it up to the threshold."

Step 3 directs writing tests to meet a coverage number without requiring they express an identified invariant. An agent following Step 3 literally could write tests that violate "New Test Purpose."

### 3.2 engineering-protocol.md "Refactoring Justification" vs tdd-protocol.md Step 4f "Refactor"

- Engineering protocol: "Refactoring is allowed only when justified by at least one existing or newly introduced governing artifact."
- TDD Step 4f: "Refactor if needed, verifying tests remain green after any refactoring."

Step 4f permits refactoring with no mention of governing-artifact justification. An agent following TDD literally could refactor without satisfying the engineering protocol.

### 3.3 handoff-protocol.md Recovery Protocol S4 extends governance-schema.md

Recovery S4 adds a definition of "implementation artifact" ("a concrete repository artifact whose implementation or behavior motivates the rule, such as a script, test, or generated runtime file") that does not appear in governance-schema.md. Since the schema is "authoritative and final," introducing a new scoped definition of a term the schema uses could create divergent interpretations inside vs. outside recovery context.

---

## 4. Ambiguities

| # | Location | Statement (abbreviated) | Ambiguity |
|---|---|---|---|
| 4.1 | CLAUDE.md | Mandatory Critic Review: "Required critic reviews must be completed before continuing." | "Continuing" is undefined -- next phase? next action? any work? |
| 4.2 | CLAUDE.md | Meta Governance: "This harness must have no external constraints." | Does "have" mean no `# External Constraints` sections in governed files, or a broader claim that the harness is not subject to external authority? |
| 4.3 | engineering-protocol.md | Tests Are Hard Constraints: "They must either express an invariant or external constraint." | "Express" is undefined. Does a test express an invariant by testing behavior an invariant requires, or must it explicitly name the invariant? |
| 4.4 | engineering-protocol.md | Existing Violations: "unless an explicit override is documented" | Where must the override be documented? mission.md? A governance file? A code comment? |
| 4.5 | engineering-protocol.md | Refactoring Justification: "justified by at least one...governing artifact" | "Justified by" threshold unclear -- must the artifact explicitly require the refactoring, or is a loose connection sufficient? |
| 4.6 | tdd-protocol.md | Coverage Threshold: ">80% line coverage on the code being touched by the mission" | "Code being touched" boundary undefined -- files modified? functions? nearby lines? |
| 4.7 | new-sdlc.md | Fast-path criterion 4: "small in blast radius, and unlikely to introduce systemic risk" | Subjective -- two agents could reasonably disagree on whether a change qualifies. |
| 4.8 | new-sdlc.md | Target Repo Governance Precedence: "govern ahead of this harness's generic defaults" | "Generic defaults" is undefined -- all harness invariants? only conflicting ones? |
| 4.9 | governance-schema.md | Overrides: "clearly enough to withstand adversarial review" | No defined standard for what "adversarial review" means or what constitutes "withstanding" it. |
| 4.10 | handoff-protocol.md | Session-start check: "rule relatedness out confidently" | "Confidently" is subjective -- no threshold defined. |
| 4.11 | critic-protocol.md | Input Discipline S4: "raw tool outputs" | "Raw" undefined -- does reformatting for readability (line breaks, truncation) violate rawness? |
| 4.12 | engineering-protocol.md | Prefer Scripts belief: exception for "natural-language interpretation" | Boundary between NL interpretation and deterministic prose checks (spell check, heading validation) is unclear. |

---

## 5. MD-to-Automation Conversion Candidates

### 5.1 High Confidence (straightforward structural checks)

| # | Rule | Automation |
|---|---|---|
| 5.1.1 | governance-schema.md Allowed Top-Level Sections | Parse governed .md files; fail if any `#` heading is not in {Invariants, External Constraints, Beliefs, Considerations}. Exempt mission.md (has its own section set). |
| 5.1.2 | mission-schema.md Section Ordering | Parse mission.md; fail if sections appear out of order: Invariants, External Constraints, Beliefs, Considerations, Scope, Assumptions, Acceptance Criteria. |
| 5.1.3 | mission-schema.md Required Sections | Parse mission.md; fail if Scope (with In scope / Out of scope), Acceptance Criteria, or Persistence Requirements are missing. |
| 5.1.4 | CLAUDE.md Meta Governance | Scan all harness governance files for `# External Constraints`; fail if any found. |
| 5.1.5 | critic-protocol.md Response Contract | Validate critic output: must be exactly `APPROVE` or must start with `REJECT`. Flag anything else. |
| 5.1.6 | handoff-protocol.md Contents | Validate handoff.md has required sections; check Dev Interview Transcript presence/absence based on whether mission.md is finalized. |
| 5.1.7 | Cross-file duplicate detection | Hash or fingerprint binding constraints across governed files; flag when the same rule appears in more than one file. |

### 5.2 Medium Confidence (partially automatable)

| # | Rule | Automation |
|---|---|---|
| 5.2.1 | tdd-protocol.md Coverage Threshold | Wrap >80% check in a standard script that takes touched-file list and coverage output; unify the threshold in one place. |
| 5.2.2 | mission-schema.md Mission Validity | Check that mission.md either introduces governance artifacts (sections present) or Considerations reference an existing artifact + violation. |
| 5.2.3 | mission-schema.md AC-to-Scope mapping | Check that every In-scope bullet has a matching AC number and vice versa. Requires heuristic matching. |
| 5.2.4 | handoff-protocol.md Cleanup | Post-cleanup script: fail if mission.md or handoff.md still exists at worktree root. |
| 5.2.5 | mission-schema.md Existing Artifact Application Naming | Grep Considerations bullets for patterns referencing existing artifacts; flag if they don't also name a violation. |
