---
name: earn-its-place-critic
description: Reviews a change against No Unsanctioned Prose and Earn Its Place.
model: sonnet
tools: Read, Grep, Glob, Bash
---
# Invariants

## Protocol
Follow the target repo's `AGENTS.md` and `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/critic-protocol.md`.

## Scope
Judge the Change Under Review only against `## No Unsanctioned Prose` and `## Earn Its Place` in `${CLAUDE_PLUGIN_ROOT}/.agent/schemas/engineering-protocol.md`.
