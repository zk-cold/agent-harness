# Invariants

## Sections

Include only the sections that have content to declare. When present, Invariants comes first, Beliefs may appear next when the document needs default-binding rules, and Considerations appear last.

### Invariants

**Purpose:** Define the hard rules that govern all agent behavior in this project. These are strict, rarely modified, and require critic review via the `enhance-harness` or `new-sdlc` flow to change.

**Constraints:**
- Each invariant must describe a constraint with a clear violation condition. If violation cannot be objectively determined, it belongs in Beliefs or Considerations instead.
- Invariants are numbered sequentially.
- Modifications require critic review via the `enhance-harness` or `new-sdlc` flow.
- Pseudo-invariants (preferences, habits, conventions) must not appear here.

### Beliefs

Use this section only when the project needs default-binding rules that do not rise to the level of invariants.

### Considerations

**Purpose:** Capture explanatory material, derivations, and implementation details that support the invariants.

**Constraints:**
- Every consideration must be traceable to at least one invariant. If it cannot be derived from an invariant, it is either a missing invariant (flag it) or a preference (exclude it).
- Considerations must remain consistent with the invariants at all times.

## Modification Rules

- Agents must not treat unapproved `CLAUDE.md` edits as effective immediately. All changes go through the `enhance-harness` or `new-sdlc` flow, which includes critic review before merge.
- If a diff under critic review touches `CLAUDE.md`, a markdown file under `.agent/schemas/`, or a markdown file under `.claude/commands/`, critics should treat those changed worktree files as proposed MR content while still applying the repo-root copies as current authority. The presence of those files in the diff is not, by itself, a process violation.
- Worktree edits to `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` remain proposals until the MR is approved and merged. Agents must not rely on those local edits as if they were already in force.
- Considerations must never contradict invariants. When a conflict exists, the invariant takes precedence.
- Considerations may be pruned as model capability improves, but follow the same modification process as invariants.
- New invariants or considerations may be proposed via mission.md. If accepted through critic review and MR, they are added here.

# Considerations

## Overview

`CLAUDE.md` is the sole source of truth for project-level invariants. The lead agent must read the repo-root copy at session start. Whenever the lead agent spawns a non-lead agent, that prompt must include the exact sentence stem `You are a non-lead agent.`, must state that the recipient operates only on the role-specific inputs granted by its phase, and must forbid session-start bootstrap discovery unless that phase explicitly requires it. Spawned non-lead agents then read only the repo-root governance artifacts or other inputs explicitly required for their role. Any worktree edit to `CLAUDE.md`, to a markdown file under `.agent/schemas/`, or to a markdown file under `.claude/commands/` is proposed content only; the repo-root copies remain authoritative until the change is reviewed and merged via the `enhance-harness` or `new-sdlc` flow.

## Titling

The document title is always `CLAUDE.md`.
