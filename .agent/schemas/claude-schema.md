# CLAUDE.md Schema

## Overview

CLAUDE.md is the sole source of truth for project-level invariants. All agents must read it at session start. It lives at the project root and is MR-gated — agents never modify it directly.

---

## Sections

Both sections are optional. Include only when there is content to declare. When present, Invariants comes first, Important Considerations second.

### Invariants

**Purpose:** Define the hard rules that govern all agent behavior in this project. These are strict, rarely modified, and require MR + human approval to change.

**Constraints:**
- Each invariant must describe a constraint with a clear violation condition. If violation cannot be objectively determined, it belongs in Important Considerations instead.
- Invariants are numbered sequentially.
- Modifications require an MR with critic review and human approval.
- Pseudo-invariants (preferences, habits, conventions) must not appear here.

### Important Considerations

**Purpose:** Capture explicit derivations from invariants that compensate for current model limitations. These guide agent behavior but are less rigid than invariants — they may be pruned as model capability improves.

**Constraints:**
- Every consideration must be traceable to at least one invariant. If it cannot be derived from an invariant, it is either a missing invariant (flag it) or a preference (exclude it).
- Considerations must remain consistent with the invariants at all times.

---

## Modification Rules

- Agents must never modify CLAUDE.md directly. All changes go through an MR with human approval and critic review.
- Considerations must never contradict invariants. When a conflict exists, the invariant takes precedence.
- Considerations may be pruned as model capability improves, but follow the same modification process as invariants.
- New invariants or considerations may be proposed via mission.md. If accepted through critic review and MR, they are added here.

---

## Titling

The document title is always `# CLAUDE.md`.
