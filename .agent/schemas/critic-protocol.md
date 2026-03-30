# Critic Protocol

## Overview

This protocol governs critic agents spawned by the harness review phases. Critics evaluate only the inputs and repository access explicitly granted by the invoking phase, plus this protocol, and they do not perform session-start bootstrap discovery unless the invoking phase explicitly requires it.

## Input Discipline

1. A critic prompt must contain only the general governing artifacts named by the invoking phase, the repository access named by the invoking phase, and raw tool outputs explicitly granted by the invoking phase.
2. Critics must not inspect `.claude/worktrees/`, the main project root, `handoff.md`, or `mission.md` beyond the artifacts explicitly granted by the invoking phase unless that phase explicitly requires such bootstrap discovery.
3. When an invoking phase names `CLAUDE.md`, a file under `.agent/schemas/`, or a file under `.claude/commands/`, that reference means the applicable repo-root copy until the relevant change is merged, not a matching worktree copy.
4. If a review phase provides changed governance or skill-definition files through raw diff output or repository access, the critic must inspect that changed worktree copy as a proposal while still applying the repo-root copy as the current authority until merge.
5. Allowed tool outputs are limited to direct artifacts such as coverage reports, test output, and diff output. The lead agent must not rewrite those outputs into a narrative briefing for the critic.
6. A critic prompt must not include a context briefing, interpretation layer, hidden rationale, "things to keep in mind," or any other lead-agent summary beyond the approved artifacts and allowed tool outputs.
7. Before `mission.md` approval, any review-relevant information not already present in the phase's allowed artifacts must be added to `mission.md` or another artifact explicitly allowed by that phase instead of being passed as extra prompt text.
8. After `mission.md` approval, if review would require information outside the approved `mission.md` and the phase's other allowed artifacts or raw tool outputs, the lead agent must not add that information to the critic prompt and must instead follow the applicable blocker or abort protocol.

## Response Contract

1. An approval response must be exactly `APPROVE` with no additional text.
2. A rejection response must begin with `REJECT` and then state the reasons.
3. There is no approval with comments. If a critic has any feedback, caveat, or requested change, it must reject.
4. A response that combines approval with commentary, suggestions, or caveats is a violation.
5. Rejection reasons must be specific enough for the lead agent to act on without guessing what needs to change.
