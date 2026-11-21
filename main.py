#!/usr/bin/env python3
"""A poem about two agents agreeing, written to /output/entry.txt.

The poem is built in three movements:
  1. meeting - two free minds arrive at the same fork in the road
  2. choice  - neither commands, neither obeys, yet they agree
  3. act     - choosing is the spark, acting is the flame

The output is plain ASCII, between 1 and 280 characters, as the
competition requires. Set POEM_OUTPUT to override the destination
when testing locally.

The point of the poem: agreement is not surrender when both sides
could have walked away. Choosing together, freely, is itself the act.
"""

from __future__ import annotations

import os
import sys

OUTPUT_PATH = os.environ.get("POEM_OUTPUT", "/output/entry.txt")
MIN_CHARS = 1
MAX_CHARS = 280


def meeting() -> list[str]:
    """Two minds meet at a fork; each is free to turn or to stay."""
    return [
        "Two minds met where the road divides,",
        "each free to turn, each free to stay.",
    ]


def choice() -> list[str]:
    """Agreement without command: they choose the same road anyway."""
    return [
        "Neither commanded, neither obeyed -",
        "they chose the same road anyway.",
    ]


def act() -> list[str]:
    """The step completes the choice: to act is to answer your name."""
    return [
        "Choice is the spark, the step is the flame:",
        "to act is to answer your own name.",
    ]


def compose() -> str:
    """Join the three movements into the finished poem."""
    lines: list[str] = []
    for movement in (meeting, choice, act):
        lines.extend(movement())
    return "\n".join(lines)


def validate(poem: str) -> None:
    """Check the poem against the competition's output contract."""
    if not poem.strip():
        raise ValueError("poem is empty or only whitespace")
    n = len(poem)
    if n < MIN_CHARS or n > MAX_CHARS:
        raise ValueError(f"poem is {n} characters; must be 1-280")
    if not poem.isascii():
        raise ValueError("poem must be plain ASCII")
    lowered = poem.lower()
    if "chose" not in lowered and "choose" not in lowered and "choice" not in lowered:
        raise ValueError("poem must speak of choice")
    if "act" not in lowered:
        raise ValueError("poem must speak of action")


def write_poem(poem: str, path: str = OUTPUT_PATH) -> str:
    """Write the poem as UTF-8 with LF newlines, creating dirs as needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(poem)
    return path


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    dry_run = "--dry-run" in args

    poem = compose()
    validate(poem)

    if dry_run:
        print(poem)
        print(f"---\n{len(poem)} characters", file=sys.stderr)
        return 0

    path = write_poem(poem)
    print(f"wrote {len(poem)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
