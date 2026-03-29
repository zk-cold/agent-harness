# Handoff

## Session
2026-03-29 — Initial design session (Claude.ai chat)

## Current Status
Mission.md drafted and ready for critic review. Proceeding to Claude Code for execution with its native multi-agent capabilities.

## What Was Decided

### File Protocol
```
CLAUDE.md                        # project-level invariants + considerations, MR-gated
.agent/
├── handoff.md                   # current state snapshot, always rewritten in full
├── journal-{session}.md         # append-only session log
└── errors-{session}.md          # session-scoped errors, may be promoted to CLAUDE.md
```

### mission.md Schema
Required sections: Invariants (new/modified), Important Considerations, Scope, Dependencies & Assumptions, Acceptance Criteria.

### CLAUDE.md Schema
Two sections:
- **Invariants** — strict gatekeeping, MR + human approval required to modify
- **Important Considerations** — explicit derivations from invariants, compensating for current model limitations, prunable over time

### Pre-Execution Flow
```
Dev interview (lead agent probes invariants behind any decision that materially affects an AC)
    ↓
Lead agent generates mission.md
    ↓
Fast path check (lead agent):
  (a) no new/modified invariants
  (b) clean, limited, safe scope
  (c) >80% line & branch coverage on target code
    ├── Fast path → 1 critic: outputs Approve / Reject / Escalate
    │     └── Escalate or Reject → normal flow or back to dev
    └── Normal flow → 2 critics: outputs Approve / Reject
          └── Reject → lead agent decides: revise & resubmit, or escalate to dev
    ↓
Mission confirmed → execution (isolated worktree)
```

### Critic Design
- Fresh context per critic instance
- Reads: CLAUDE.md, mission.md, any code it chooses to browse
- Does NOT read: journal, errors files
- Receives coverage report directly (does not re-run tooling)
- "No approval with comments" — approve cleanly or reject with reasons

### Abort Protocol
Blocker detected → create Jira ticket → update handoff.md → halt

### MR Flow (defined, not yet designed in detail)
- CLAUDE.md changes are always part of the MR
- At least 2 naive critics review the MR (may have different focus areas)
- Fast path MR: 1 critic

## Next Steps
1. Run critic review on mission.md (two critics, normal flow — new invariants present)
2. If approved, proceed to design execution phase:
   - Lead agent internal structure & sub-agent orchestration
   - Session lifecycle (start, checkpoint, retrospective)
   - Harness bootstrap (CLAUDE.md initialization, worktree setup)
   - MR critic design (focus areas, output format)
3. Formalize all schemas (handoff.md, journal, errors, CLAUDE.md, mission.md) as templates

## Open Questions
- MR critic focus areas — deferred, to be designed
- Harness infrastructure & tooling integration — out of scope for this mission
- How session boundary is determined (who triggers start/end, retrospective) — partially discussed, not finalized

## Key Constraints
- Every task in isolated Git worktree
- No rollback — abort is the recovery strategy
- CLAUDE.md is MR-gated, never modified directly by agent
