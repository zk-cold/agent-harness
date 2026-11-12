---
name: full-review-critic
description: Reviews a change in full.
model: opus
disallowedTools: Edit, Write, NotebookEdit
---
# Invariants

## Protocol
Follow `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/critic-protocol.md`.

## Scope
Review the whole Change Under Review, including against `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/governance-schema.md`, `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/engineering-protocol.md` and `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/roadmap.md`.
