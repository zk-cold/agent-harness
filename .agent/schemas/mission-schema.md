# Invariants

## Self-Containment
Every `mission.md` must be self-contained: a critic sub-agent with access to only the harness repo-root `.agent/schemas/governance-schema.md`, the repo-root `.agent/schemas/critic-protocol.md`, the repo-root `.agent/schemas/mission-schema.md`, and `mission.md` must be able to evaluate it.

When a mission proposes changes to a harness `*.template` file, `mission.md` must reproduce the full proposed text of each updated section for each changed template file in `Considerations` rather than referring to a diff, summary, or external note.

## Section Ordering
When present, sections appear in this order: Invariants, External Constraints, Beliefs, Considerations, Scope, Assumptions, Acceptance Criteria.

## Required Sections

### 1. Scope

**Required subsections:**

- **In scope:** — Bulleted list of deliverables or work items this mission will produce.
- **Out of scope:** — Bulleted list of related work explicitly excluded. This is not exhaustive; it targets the most likely sources of scope creep.

**Constraints:**
- Every in-scope item must have at least one corresponding acceptance criterion. If an in-scope item has no AC, either add one or move the item to out-of-scope.
- Out-of-scope items should name the reason for exclusion when it is not obvious (e.g., "deferred to next phase", "owned by another team").

### 2. Acceptance Criteria

**Constraints:**
- Each AC must be **testable**: an independent reviewer can determine whether it has been met by examining the deliverables, without needing to ask the author.
- Each AC must be **unambiguous**: there is one reasonable interpretation of what "met" means.
- Each AC must be **specific**: it references concrete artifacts, sections, or behaviors — not vague qualities like "well-designed" or "comprehensive."
- ACs are numbered sequentially.
- Each non-persistence AC maps to one or more in-scope items.
- Each persistence AC maps to the governed artifact it persists.
- Do not include ACs for out-of-scope items.

### 3. Persistence Requirements

**Constraints:**
- Every governed artifact captured in `Invariants`, `External Constraints`, `Beliefs`, or `Considerations` must have at least one acceptance criterion that requires the artifact to be persisted.
- When a governed artifact is not persisted as automated tests, its persistence acceptance criterion must require the same text in the governed file and matching top-level governance section where the artifact will live after the mission completes.
- When a mission's `Considerations` section references an existing governing artifact solely to apply it retrospectively to an existing violation — without modifying, extending, or reinterpreting that artifact — the mission may explicitly exempt that consideration from persistence by listing it in `Out of scope`. When so exempted, that consideration does not require a persistence acceptance criterion.
- Every consideration that a mission persists must be prepared to withstand adversarial critic review against its lasting governance value beyond the mission.

## Mission Validity

A mission must satisfy at least one of the following: (1) the mission introduces at least one governing artifact in Invariants, External Constraints, Beliefs, or Considerations; (2) the mission's Considerations include at least one bullet that explicitly names an existing governing artifact being applied to resolve an existing violation.

## Existing Artifact Application Naming

When a mission applies an existing governing artifact through Considerations, the relevant Considerations bullet must name both the existing governing artifact and the existing violation being resolved.

## Optional Sections
Optional mission sections may be used only under these exact headings: `Invariants`, `External Constraints`, `Beliefs`, `Considerations`, `Assumptions`.
- Omit optional sections entirely when not applicable; do not include empty or placeholder sections.
- For changes other than removals, full new text must be proposed, not a description of changes.
- Critics must review rigoriously any proposed new/updated governance artifacts, against their qualifications clauses

## Assumptions Content
Things believed to be true, that materially enables / shapes / constraints the mission.

# Considerations

## Assumption Qualifications
A statement is disqualified as an assumption when any of the following is true:
- It is verifiable during Mission Creation
- It does not serve as a precondition to the drafted mission
- It serves governance value beyond the scope of this mission

## Mission Generator
Use `python3 -m scripts.mission_generator [path/to/mission.md]` to interactively draft or rewrite `mission.md`. This is an agent-operated convenience tool, not an approval gate. It should safely capture multiline text and special characters and emit a schema-ordered draft for review.
