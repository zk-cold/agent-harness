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
Review the Change Under Review in full, including against `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/governance-schema.md` and `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/engineering-protocol.md`.
