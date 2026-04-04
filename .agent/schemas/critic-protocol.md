# Invariants

## Overview

This protocol governs critic agents spawned by the harness review phases. The lead agent's prompt to each critic must be instantiated from the applicable entry in `.agent/templates/new-sdlc-subagents.prompt.template`, must include `.agent/schemas/governance-schema.md` as the first governance artifact listed, must include the exact sentence stem `You are a non-lead agent.`, must state that the recipient operates only on the role-specific inputs granted by the invoking phase, and must forbid session-start bootstrap discovery unless the invoking phase explicitly requires it. Critics evaluate only the inputs and repository access explicitly granted by the invoking phase, plus this protocol, and they do not perform session-start bootstrap discovery unless the invoking phase explicitly requires it.

## Input Discipline

These rules apply to all critic agents. Where a rule's scope depends on whether the critic has tool access, the distinction is noted.

1. A critic prompt must contain only the general governing artifacts named by the invoking phase and, for prompt-only critics, raw tool outputs explicitly granted by the invoking phase. `.agent/schemas/governance-schema.md` must appear first among the governance artifacts in every critic prompt. For tool-capable critics (see Completion-Review Tool Access below), the prompt contains the governing artifacts and the worktree path; the critic retrieves raw data itself using its granted tools. Within a single critic prompt, each artifact path listed by the invoking phase must appear at most once; later prompt text must refer back to those already listed artifacts generically instead of repeating the paths.
2. Critics must treat the lead agent's `You are a non-lead agent.` prompt language as binding: they operate only on the role-specific inputs granted by the invoking phase and must not inspect `.claude/worktrees/`, the main project root, `handoff.md`, or `mission.md` beyond the artifacts explicitly granted by the invoking phase unless that phase explicitly requires such bootstrap discovery.
3. When an invoking phase names `CLAUDE.md`, a file under `.agent/schemas/`, or a file under `.claude/commands/`, the critic prompt must include the artifacts explicitly named by the phase.
4. If changed governance or skill-definition files are present in the diff or discoverable through repository access, the critic must inspect those changed worktree copies as part of the review.
5. The lead agent must not rewrite raw tool outputs or raw data into a narrative briefing for the critic. For prompt-only critics, raw tool outputs provided in the prompt must be unmodified direct artifacts (coverage reports, test output, diff output). For tool-capable critics, the lead agent provides no raw tool outputs in the prompt — the critic fetches what it needs.
6. A critic prompt must not include a context briefing, interpretation layer, hidden rationale, "things to keep in mind," or any other lead-agent summary beyond the approved artifacts and (for prompt-only critics) allowed tool outputs.
7. Before `mission.md` approval, any review-relevant information not already present in the phase's allowed artifacts must be added to `mission.md` or another artifact explicitly allowed by that phase instead of being passed as extra prompt text.
8. After `mission.md` approval, if review would require information outside the approved `mission.md` and the phase's other allowed artifacts, raw tool outputs (for prompt-only critics), or tool-accessible data (for tool-capable critics), the lead agent must not add that information to the critic prompt and must instead follow the applicable blocker or abort protocol.

## Completion-Review Tool Access

Completion-review phases (post-implementation review in both skills) grant critics read-only tool access so they can inspect the codebase and changes directly rather than relying on lead-agent-provided prompt text.

### Granted read-only tools

Completion-review critics may use: Read, Grep, Glob, `git diff`, `git log`, `git show`, and other read-only repository inspection commands.

### Excluded heavy tools

Completion-review critics must not run test suites, coverage tools, linters, formatters, or any tool that executes project code. These are heavy verification tools.

### Heavy verification outputs as runtime artifacts

Before spawning a completion-review critic, the lead agent (or dev agent) must write heavy verification outputs — such as full test suite results, coverage reports, and linter output — as runtime artifact files at the worktree root. Each completion-review runtime artifact file must contain only raw tool output; it must not include lead-agent summaries, acceptance-criteria self-evaluation, or any other narrative interpretation. The critic reads those artifact files using its granted read-only tools. The lead agent does not include heavy verification outputs in the critic prompt.

## Response Contract

1. An approval response must be exactly `APPROVE` with no additional text.
2. A rejection response must begin with `REJECT` and then state the reasons.
3. There is no approval with comments. If a critic has any feedback, caveat, or requested change, it must reject.
4. A response that combines approval with commentary, suggestions, or caveats is a violation.
5. Rejection reasons must be specific enough for the lead agent to act on without guessing what needs to change.
