# Governance Audit Findings

Audit of all governed files against `.agent/schemas/governance-schema.md`.

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
