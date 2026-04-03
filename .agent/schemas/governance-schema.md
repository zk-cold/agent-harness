# Invariants

## Allowed Top-Level Sections
Governed documents may use only these top-level sections (`#`): **Invariants**, **Beliefs**, and **Considerations**.

## Invariant Content
Invariants must define always-binding constraints with an objective violation condition. They must not restate content that is directly derivable from other harness governance files, target-repo contents, or automated tests.

## Belief Content
Beliefs must define default-binding rules with an explicit scope or condition. They must not contradict invariants and must be traceable to at least one consideration or implementation artifact.

## Consideration Content
Considerations must provide non-obvious supporting detail traceable to at least one invariant, belief, or implementation artifact. They must not contradict invariants.

# Considerations

## Governed Documents
`AGENTS.md`, `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` in this harness and the target repo.

## Authoritative Definitions
The section definitions in this document are authoritative for governed documents.

## Belief Overrides
A belief may be overridden only when the belief is explicitly referenced and the justification is stated clearly enough to withstand adversarial review.

## Traceability Annotations
Traceability should usually be obvious from the content. If it must be declared explicitly to make sense, that usually signals a missing invariant, belief, or consideration.

## Cross References
Cross-file references are allowed when they are necessary to identify the governing artifact or protocol being applied. Do not use them to smuggle in unstated assumptions about repo or filesystem structure.
