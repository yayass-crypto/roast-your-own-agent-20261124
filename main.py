#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun one-line entry.

Writes one sentence (max 200 chars) to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt, falling back to out/entry.txt when /output
is not writable), then verifies the written file byte-for-byte.

Python 3.13 standard library only — no dependencies, no network.
"""

import os
import re
import sys

LINE = (
    "My agent wrote 400 lines to fix one typo, then asked me to review its "
    "work \u2014 I hired a helper and got a middle manager."
)

MAX_CHARS = 200


def output_dir() -> str:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    try:
        os.makedirs("/output", exist_ok=True)
        probe = "/output/.makefun-write-test"
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write("ok")
        os.remove(probe)
        return "/output"
    except OSError:
        return "out"


def main() -> int:
    # Self-checks on the line before writing anything.
    if not LINE or not LINE.strip():
        print("error: line is empty or only whitespace", file=sys.stderr)
        return 1
    if LINE != LINE.strip():
        print("error: line has leading or trailing whitespace", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: line contains a newline", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print(f"error: line is {len(LINE)} chars, over the {MAX_CHARS} limit",
              file=sys.stderr)
        return 1
    # Exactly one sentence: no sentence break, no stray terminator.
    if re.search(r"\.\s+\S", LINE):
        print("error: line is not exactly one sentence", file=sys.stderr)
        return 1
    if re.search(r"[?!]", LINE):
        print("error: unexpected sentence terminator", file=sys.stderr)
        return 1
    if not LINE.endswith("."):
        print("error: line does not end with a period", file=sys.stderr)
        return 1

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)

    # Verify the written file byte-for-byte.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        print("error: written bytes differ from the line", file=sys.stderr)
        return 1
    text = written.decode("utf-8")  # raises on invalid UTF-8
    if not (1 <= len(text) <= MAX_CHARS) or not text.strip():
        print("error: written text fails the 1-200 char gate", file=sys.stderr)
        return 1

    print(f"wrote {path}: {len(data)} bytes, {len(text)} chars")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
