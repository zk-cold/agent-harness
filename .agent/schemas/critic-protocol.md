# Invariants

## Prompt Construction
A critic prompt must follow the applicable template exactly except for placeholder substitution and omission of explicitly optional blocks. It must contain only the governing artifacts named by the invoking phase and, for prompt-only critic sub-agents, raw tool outputs explicitly granted by that phase. `.agent/schemas/governance-schema.md` must appear first among the governance artifacts in every critic prompt. For tool-capable critic sub-agents, the prompt contains the governing artifacts and the worktree path; the critic sub-agent retrieves raw data itself using its granted tools. Each critic prompt must also state that the recipient operates only on the role-specific inputs granted by the invoking phase and must forbid session-start bootstrap discovery unless the invoking phase explicitly requires it.

## Input Discipline

These rules apply to all critic sub-agents. Where a rule's scope depends on whether a critic sub-agent has tool access, the distinction is noted.

1. Critic sub-agents operate only on the role-specific inputs granted by the invoking phase and must not inspect `.claude/worktrees/`, the main project root, `handoff.md`, or `mission.md` beyond the artifacts explicitly granted by the invoking phase unless that phase explicitly requires such bootstrap discovery.
2. When an invoking phase names a file under `.agent/schemas/` or a file under `.claude/commands/`, the critic prompt must include the artifacts explicitly named by the phase. Runtime-discovered repo files such as `CLAUDE.md` or `AGENTS.md` do not need to be listed explicitly unless the phase requires them as prompt artifacts.
3. If changed governance or skill-definition files are present in the diff or discoverable through repository access, the critic sub-agent must inspect those changed worktree copies as part of the review.
4. The primary agent must not rewrite raw tool outputs or raw data into a narrative briefing for the critic sub-agent. For prompt-only critic sub-agents, raw tool outputs provided in the prompt must be unmodified direct artifacts (coverage reports, test output, diff output). For tool-capable critic sub-agents, the primary agent provides no raw tool outputs in the prompt — the critic sub-agent fetches what it needs.
5. A critic prompt must not include a context briefing, interpretation layer, hidden rationale, "things to keep in mind," or any other primary-agent summary beyond the approved artifacts and, for prompt-only critic sub-agents, allowed raw tool outputs.
6. Before `mission.md` approval, any review-relevant information not already present in the phase's allowed artifacts must be added to `mission.md` or another artifact explicitly allowed by that phase instead of being passed as extra prompt text.
7. After `mission.md` approval, if review would require information outside the approved `mission.md` and the phase's other allowed artifacts, raw tool outputs (for prompt-only critic sub-agents), or tool-accessible data (for tool-capable critic sub-agents), the primary agent must not add that information to the critic prompt and must instead follow the applicable blocker or abort protocol.

## Completion-Review Tool Access

Completion-review phases (post-implementation review in both skills) grant critic sub-agents read-only tool access so they can inspect the codebase and changes directly rather than relying on primary-agent-provided prompt text.

### Granted read-only tools

Completion-review critic sub-agents may use: Read, Grep, Glob, `git diff`, `git log`, `git show`, and other read-only repository inspection commands.

### Excluded heavy tools

Completion-review critic sub-agents must not run test suites, coverage tools, linters, formatters, or any tool that executes project code. These are heavy verification tools.

### Heavy verification outputs as runtime artifacts

Before spawning a completion-review critic sub-agent, the primary agent (or execution sub-agent) must write heavy verification outputs — such as full test suite results, coverage reports, and linter output — as runtime artifact files at the worktree root. Each completion-review runtime artifact file must contain only raw tool output; it must not include primary-agent summaries, acceptance-criteria self-evaluation, or any other narrative interpretation. The critic sub-agent reads those artifact files using its granted read-only tools. The primary agent does not include heavy verification outputs in the critic prompt.

## Response Contract

1. An approval response must be exactly `APPROVE` with no additional text.
2. A rejection response must begin with `REJECT` and then state the reasons.
3. There is no approval with comments. If a critic has any feedback, caveat, or requested change, it must reject.
4. Rejection reasons must be specific enough for the primary agent to act on without guessing what needs to change.
