#!/usr/bin/env python3
"""handoff.md generator for the agent harness.

Generates a handoff.md string from structured inputs. Raises ValueError on
invalid input with a markdown-formatted violations list.

Modes:
  pre-mission   Three sections: Next / Ongoing Step, Known Failed Attempts,
                Dev Interview Transcript. --transcript is required.
  post-mission  Two sections: Next / Ongoing Step, Known Failed Attempts.
                --transcript is disallowed.
"""

import sys


def generate(mode, next_step, failed_attempts, transcript):
    """Return a handoff.md string, or raise ValueError listing violations.

    Args:
        mode: "pre-mission" or "post-mission", or None if not provided.
        next_step: text for the Next / Ongoing Step section (required).
        failed_attempts: text for Known Failed Attempts, or None (defaults to "None").
        transcript: text for Dev Interview Transcript; required in pre-mission,
                    disallowed in post-mission.

    Returns:
        Generated handoff.md string.

    Raises:
        ValueError: markdown-formatted violations list when input is invalid.
    """
    violations = []

    if mode is None:
        violations.append("- Missing required mode flag: `--pre-mission` or `--post-mission`")
    elif mode not in ("pre-mission", "post-mission"):
        violations.append(
            f"- Unrecognized or conflicting mode `{mode}`: must be exactly one of"
            " `--pre-mission` or `--post-mission`"
        )

    if next_step is None:
        violations.append("- Missing required flag: `--next-step`")

    if mode == "pre-mission" and transcript is None:
        violations.append(
            "- Missing required flag for pre-mission mode: `--transcript`"
        )
    elif mode == "post-mission" and transcript is not None:
        violations.append(
            "- Flag `--transcript` is disallowed in post-mission mode"
        )

    if violations:
        raise ValueError("## Violations\n\n" + "\n".join(violations))

    body_failed = failed_attempts if failed_attempts is not None else "None"

    sections = [
        f"## Next / Ongoing Step\n\n{next_step}",
        f"## Known Failed Attempts\n\n{body_failed}",
    ]
    if mode == "pre-mission":
        sections.append(f"## Dev Interview Transcript\n\n{transcript}")

    return "\n\n".join(sections) + "\n"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate a handoff.md file.")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--pre-mission", action="store_true", default=False)
    mode_group.add_argument("--post-mission", action="store_true", default=False)
    parser.add_argument("--next-step", dest="next_step", default=None)
    parser.add_argument("--failed-attempts", dest="failed_attempts", default=None)
    parser.add_argument("--transcript", default=None)

    args = parser.parse_args()

    if args.pre_mission:
        mode = "pre-mission"
    elif args.post_mission:
        mode = "post-mission"
    else:
        mode = None

    try:
        result = generate(mode, args.next_step, args.failed_attempts, args.transcript)
        print(result, end="")
        sys.exit(0)
    except ValueError as exc:
        print(str(exc))
        sys.exit(1)
