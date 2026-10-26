# Invariants

## Governed Documents
`CLAUDE.md`, `.agent/schemas/*.md`, `.claude/commands/*.md`, and `.claude/agents/*.md` in this harness and the target repo.

## Governance Artifacts
Governed documents, after any frontmatter, may only define governance artifacts, with their category as a top-level (`#`) section:
- **Invariants**: always-binding constraints.
- **External Constraints**: currently binding constraints imposed by an external authority, anchored to a named source and version.
- **Considerations**: default-binding rules. A consideration may be overridden only when it is explicitly referenced and the justification is stated clearly enough to withstand adversarial review.

## Target Repo Governance
Target repo governance must not conflict with this harness's invariants.

## API Design
An API is any signature, type, or module structure visible from outside its defining module, and any data or wire format exposed outside the module that defines it. Unless it is an External Constraint, the specification of an API being introduced or changed must be recorded as an invariant.

## Sanctioned Files
- `.gitignore`

## No Unsanctioned Prose
Prose outside governed documents that standing governance does not sanction must not be written, and must be removed on encounter.

## Earn Its Place
A token may be written or kept only if it directly shapes or governs production behavior, it cannot be derived from this harness or the target repo, and the work could not be equal or better without it.

## Prose and Token Scope
`No Unsanctioned Prose` and `Earn Its Place` apply only to content git does not ignore and to content governance explicitly designates.
