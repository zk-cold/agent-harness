# Invariants

## Violation-Resolution Specificity
When a consideration claims to resolve an existing violation, it must name both the governance artifact and the violation.

## Clause-Level Challenge
The challenge decomposes each proposed governance artifact into its individual clauses and challenges every clause. An artifact survives only if every one of its clauses survives. The challenge does not judge the mission as a whole.

# Considerations

## Challenge Checks
Each clause is challenged, confined to these three checks, in priority order:
1. Conformance to the content and disqualification clauses of `governance-schema.md` and to the governance-artifact content rules in this document.
2. For a proposed invariant only, whether it is a real business mandate rather than an external constraint or a derived implementation detail.
3. Whether the clause carries lasting governance value beyond the mission.

## Non-Surviving Clauses
A clause that does not survive must never be passed as a non-disqualifying note.

## Clause Dispositions
Return one disposition per clause, each with a one-line reason, drawn from:
- SURVIVES
- REVISE
- RECLASSIFY-EXTERNAL-CONSTRAINT
- DEMOTE — non-obvious ⇒ give the accompanying consideration text; obvious ⇒ DROP
- PROMOTE — a consideration clause that is actually an always-binding or general rule ⇒ make it an invariant
- MARK-TRANSIENT
- UNCLEAR — say what the lead must clarify
