# Invariants

## Allowed Top-Level Sections
Governed documents may use only these top-level sections (`#`): **Invariants**, **Beliefs**, and **Considerations**.

## Invariant Content
Invariants must define always-binding constraints whose truth can be judged objectively from the statement itself. They must not restate content that is directly derivable from other harness governance files, target-repo contents, or automated tests.

## Belief Content
Beliefs must define default-binding rules with an explicit scope or condition. They must not contradict invariants and must be traceable to at least one consideration or implementation artifact.

## Consideration Content
Considerations must provide non-obvious supporting detail traceable to at least one invariant, belief, or implementation artifact. They must not contradict invariants.

# Considerations

## Governed Documents
`AGENTS.md`, `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` in this harness and the target repo.

## Authoritative Definitions
The section definitions in this document are authoritative for governed documents.

## Invariant Qualification
An invariant should read as an always-binding constraint on agent behavior. It is disqualified as an invariant when any of the following is true:

- The statement is not objectively testable from its own wording.
- The statement is a preference, habit, convention, style choice, or explanation rather than a binding constraint.
- The statement is already directly derivable from other governance artifacts, target-repo contents, or automated tests.
- The statement depends on unstated context or interpretation to know when it applies.

Invariants do not need an explicit `Violation:` clause. The rule itself should already be concrete enough that a reviewer can determine whether it was followed.

## Belief Qualification
A belief should read as a default-binding decision rule. It is disqualified as a belief when any of the following is true:

- The statement contradicts an invariant.
- The statement does not define the condition, scope, or context in which it applies.
- The statement cannot be traced to at least one consideration or implementation artifact.
- The statement is actually an always-binding constraint and therefore belongs in invariants instead.
- The statement is merely explanatory material with no decision-guiding effect.

## Belief Overrides
A belief may be overridden only when the belief is explicitly referenced and the justification is stated clearly enough to withstand adversarial review.

## Belief Override Requirements
When overriding a belief, the agent must do all of the following:

- Explicitly identify the belief being overridden.
- State why the default rule is not appropriate in the current context.
- Provide a justification concrete enough for adversarial review.
- Keep the override scoped to the current decision instead of silently weakening the belief in general.

## Consideration Qualification
A consideration should provide non-obvious supporting detail. It is disqualified as a consideration when any of the following is true:

- The statement contradicts an invariant.
- The statement is obvious enough that it adds no interpretive or implementation value.
- The statement cannot be traced back to an invariant, belief, or implementation artifact.
- The statement is actually a binding rule and therefore belongs in invariants or beliefs instead.

## Traceability Annotations
Traceability should usually be obvious from the content. If it must be declared explicitly to make sense, that usually signals a missing invariant, belief, or consideration.

## Cross References
Cross-file references are allowed when they are necessary to identify the governing artifact or protocol being applied. Do not use them to smuggle in unstated assumptions about repo or filesystem structure.
