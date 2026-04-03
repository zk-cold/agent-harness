# Invariants

## Allowed Top-Level Sections
Governed documents may use only these top-level sections (`#`): **Invariants**, **Beliefs**, and **Considerations**.

## Authoritative Definitions
The definitions in this document are authoritative and final. Agents must not edit this file.

## Invariant Content
Invariants must define always-binding constraints。

## Belief Content
Beliefs must define default-binding rules with an explicit scope or condition.

## Consideration Content
Considerations must provide non-obvious supporting detail traceable to at least one invariant, belief, or implementation artifact. They must not contradict invariants.

# Considerations

## Governed Documents
`AGENTS.md`, `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` in this harness and the target repo.

## Invariant Qualification
A statement is disqualified as an invariant when any of the following is true:
- It is not objectively testable from its own wording.
- It is a preference, habit, convention, style choice, or explanation rather than a binding constraint.
- It is already derivable from other governance artifacts or target-repo contents.

Invariants do not need an explicit `Violation:` clause. The rule itself should already be concrete enough that a reviewer can determine whether it was followed.

## Belief Qualification
A statement is disqualified as a belief when any of the following is true:
- It contradicts an invariant.
- It does not define the condition, scope, or context in which it applies.
- It cannot be traced to at least one consideration or implementation artifact.
- It is actually an always-binding constraint and therefore belongs in invariants instead.

## Belief Overrides
A belief may be overridden only when the belief is explicitly referenced and the justification is stated clearly enough to withstand adversarial review.

## Consideration Qualification
A consideration should provide non-obvious supporting detail. It is disqualified as a consideration when any of the following is true:
- It contradicts an invariant.
- It is obvious enough that it adds no interpretive or implementation value.
- It cannot be traced back to an invariant, belief, or implementation artifact.
- It is actually a binding rule and therefore belongs in invariants or beliefs instead.

## Traceability
Traceability should usually be obvious from the content. If it must be declared explicitly to make sense, that usually signals a missing invariant, belief, or consideration.

## Cross References
Cross-file references are allowed when they are necessary to identify the governing artifact or protocol being applied. Do not use them to smuggle in unstated assumptions about repo or filesystem structure.
