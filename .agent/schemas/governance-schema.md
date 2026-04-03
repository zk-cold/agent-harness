# Invariants

## Schema Bounded Content
Governed documents may use only these top-level sections (`#`): **Invariants**, **Beliefs**, and **Considerations**.

## Authoritative Definitions
The definitions for top-level sections is authoritative and final in this document. They must be applied without reinterpretation.

## Invariants Definition
Define always-binding constraints that govern agent behavior.
**Constraints**:
- Must describe an objectively-enforceable constraint
- Not otherwise derivable from harness governance files or target repo contents
- Not otherwise expressible as automated tests

## Beliefs Definition
Define default-binding rules that guide agent decision-making.
**Constraints**:
- Must never contradict any invariants
- Must define its applicable scope / condition
- Must be traceable to at least one consideration or implementation artifact (e.g. source code)
**Override Protocol**:
A belief may be overridden only if:
- The belief is explicitly referenced
- A justification is provided - and prepared to withstand adversarial review

# Considerations

## Considerations Definition
Provide details that isn't automatically obvious.
**Constraints**:
- Must never contradict any invariants
- Must be traceable to at least one invariant or belief
- Must not state the obvious

## Governed Documents
`AGENTS.md`, `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` in this harness and the target repo.

## Traceability Annotations
Traceability are ideally obvious. A traceability that needs explicit declaration implies missing Invariant / Belief / Consideration to surface.

## Cross References
References across files contains an intrinsic belief in repo / file system structure. They hence should never appear in Invariants.
