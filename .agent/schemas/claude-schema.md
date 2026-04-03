# Invariants

## Section Order

Include only the sections that have content to declare. When present, Invariants comes first, Beliefs may appear next when the document needs default-binding rules, and Considerations appear last.

## Invariant Entries
Each invariant in `CLAUDE.md` must be numbered sequentially and must include a clear violation condition. Pseudo-invariants such as preferences, habits, or conventions must not appear there.

## Change Control
Unapproved edits to `CLAUDE.md` are proposals only. They do not become effective until reviewed through `/new-sdlc` and merged.

## Review of Proposed Governance Changes
When a diff under review touches `CLAUDE.md`, `.agent/schemas/*.md`, or `.claude/commands/*.md`, reviewers inspect the changed worktree copies as proposals while continuing to apply the repo-root copies as current authority until merge.

# Considerations

## Overview

`CLAUDE.md` is the sole source of truth for project-level invariants. The lead agent reads the repo-root copy at session start. When the lead agent spawns a non-lead agent, the prompt must explicitly define that role boundary and limit the recipient to the inputs granted by its phase.

## Titling

The document title is always `CLAUDE.md`.
