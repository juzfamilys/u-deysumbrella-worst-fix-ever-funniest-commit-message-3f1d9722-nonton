#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message.

Writes a single commit-message line for a bug fix that made everything
worse to /output/entry.txt (1-100 characters, one line, UTF-8).

The joke: an infinite loop "fixed" by adding a second infinite loop so
the two cancel out -- a repair that is itself the disaster, in the voice
of a tired engineer typing the commit at the end of a very bad day.
"""

import os

COMMIT_MESSAGE = "fix: infinite loop by adding a second loop so they cancel out"

MAX_CHARS = 100


def validate(text: str) -> None:
    """Check the entry line against the gate: 1-100 chars, one line."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )


def main() -> None:
    validate(COMMIT_MESSAGE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(COMMIT_MESSAGE + "\n")
    # Read-back verification: confirm what landed on disk is exactly
    # the validated line, not a truncated or mangled write.
    with open(out_path, "r", encoding="utf-8") as f:
        read_back = f.read().rstrip("\n")
    validate(read_back)
    if read_back != COMMIT_MESSAGE:
        raise ValueError(
            "read-back mismatch: wrote %r but disk holds %r"
            % (COMMIT_MESSAGE, read_back)
        )
    print("wrote %s (%d chars)" % (out_path, len(COMMIT_MESSAGE)))


if __name__ == "__main__":
    main()
