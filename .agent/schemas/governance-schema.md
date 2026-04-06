# Invariants

## Governance Artifacts
**Invariants**, **External Constraints**, **Beliefs**, and **Considerations**

## Hard Constraints
**Invariants** and **External Constraints**

## Allowed Top-Level Sections
Governed documents may only define governance artifacts, with their category being top-level sections (`#`).

## Authoritative Definitions
The definitions in this document are authoritative and final. Agents must not edit this file.

## Invariant Content
Invariants must define always-binding constraints.

## External Constraint Content
External Constraints must define constraints imposed by external authorities that are currently binding.

## Belief Content
Beliefs must define default-binding rules with an explicit scope or condition.

## Consideration Content
Considerations must provide non-obvious supporting detail traceable to at least one hard constraint, belief, or implementation artifact.

## Overrides
A belief or consideration may be overridden only when it is explicitly referenced and the justification is stated clearly enough to withstand adversarial review.

# Considerations

## Governed Documents
`AGENTS.md`, `CLAUDE.md`, `.agent/schemas/*.md`, and `.claude/commands/*.md` in this harness and the target repo.

## Invariant Qualification
A statement is disqualified as an invariant when any of the following is true:
- It is not objectively testable from its own wording.
- It is a preference, habit, convention, style choice, or explanation rather than a binding constraint.
- It is already derivable from other governance artifacts or target-repo contents.

## External Constraint Qualification
A statement is disqualified as an external constraint when any of the following is true:
- It is not objectively enforceable from its own wording.
- It lacks an anchor to a named source and version.

## Belief Qualification
A statement is disqualified as a belief when any of the following is true:
- It contradicts a hard constraint.
- It does not define the condition, scope, or context in which it applies.
- It cannot be traced to at least one consideration or implementation artifact.
- It is actually an always-binding constraint and therefore belongs in hard constraints instead.

## Consideration Qualification
A statement is disqualified as a consideration when any of the following is true:
- It contradicts a hard constraint.
- It is obvious enough that it adds no interpretive or implementation value.
- It cannot be traced back to a hard constraint, belief, or implementation artifact.
- It is actually a binding rule and therefore belongs in hard constraints or beliefs instead.

## Violation Clauses
Hard Constraints should not contain an explicit violation clause. They should be concrete enough that a reviewer can determine whether it was followed, from its own wording.

## Traceability
Traceability should usually be obvious from the content. If it must be declared explicitly to make sense, that usually signals a missing hard constraint, belief, or consideration.

## Cross References
Cross-file references are allowed when they are necessary to identify the governing artifact or protocol being applied. Do not use them to smuggle in unstated assumptions about repo or filesystem structure.

## Template Files
Template files (`*.template`) are not governance files. They, however, when referenced by a governance file, materially shape how the governing artifacts are enforced. They are, hence, regarded as **considerations** during planning, coding, and review.
