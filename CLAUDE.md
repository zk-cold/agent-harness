# Invariants

## Bootstrap
Unless you are a sub-agent, handle any prompt with `/new-sdlc`.

## Mandatory Critic Review
Required critic reviews must be completed before continuing.

## Meta Governance
This harness must have no external constraints.

## Root Branch
The root branch for this harness is `main`.

## Trivial Merge Qualification
A completion-review or cleanup merge counts as trivial only when Git reports `Already up to date.` or performs a clean fast-forward with no manual conflict resolution.

## Codex Sub-Agent Boundary
Codex sub-agents must ignore this `CLAUDE.md` while remaining free to continue reading `AGENTS.md`.

# Considerations

## Derivability Remediation
governance-schema.md Invariant Qualification bullet 3 ("already derivable from other governance artifacts") is applied to remove invariants, beliefs, and considerations identified as derivable or duplicated in TODO.md section 1 (Possible Removals). Cross-file duplications keep the authoritative copy and remove the restatement; within-file duplications and obvious/low-value items are removed outright.

## Codex Sub-Agent Boundary Rationale
The Codex sub-agent boundary in this file exists because `CLAUDE.md` carries lead-only governance here, while `AGENTS.md` remains a useful Codex routing artifact.

## Harness-Local Scope Invariant
The opening scope invariant in this file is specific to this harness `CLAUDE.md`. It should not be generalized into an assumption that target repo `CLAUDE.md` files use the same audience or scope model.

## Bootstrap Breadth
`Bootstrap` intentionally treats any prompt as a request to create new SDLC. That breadth is deliberate for the current harness because governance-document edits are implementation work. Narrowing should happen only through future explicit exclusions, not by silently weakening the invariant.

## Bootstrap Check
Run within Mission Creation after routing, against the applicable repo root. Two subcommands:
- `python3 -m scripts.bootstrap_check [repo_root]` — Outputs one of: `ROOT_ARTIFACTS`, `MULTIPLE_WORKTREES`, `ONE_WORKTREE_NO_HANDOFF`, `ONE_WORKTREE_ABORTED`, `ONE_WORKTREE_RESUMABLE`, `NO_WORKTREE`. Exits 0 in all cases. Use to detect root artifacts and get an overall worktree-state summary.
- `python3 -m scripts.bootstrap_check list [repo_root]` — Outputs one line per worktree: `<path> <status>`, where status is `RESUMABLE`, `ABORTED`, or `NO_HANDOFF`. Exits 0 in all cases (outputs nothing when no worktrees exist). Use during the interview to inspect individual worktrees before applying the relatedness test defined in `.agent/schemas/handoff-protocol.md` and `.claude/commands/new-sdlc.md`.
