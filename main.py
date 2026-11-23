#!/usr/bin/env python3
"""Roast Your Own Agent — a one-line self-roast.

The roast is a single sentence, 119 characters long.  The script checks
the line against a small set of shape rules before it ever touches the
disk, writes it out, then reads the file back and compares the bytes so
a partial write can never pass silently.
"""

import os
import sys

ROAST = (
    "My agent wrote 400 lines to fix one typo, then asked me to review "
    "its work \u2014 I hired a helper and got a middle manager."
)

MAX_LENGTH = 200


def _fails_shape(text):
    """Return a human-readable problem with *text*, or None if it is fine."""
    if not text:
        return "line is empty"
    if text != text.strip():
        return "line has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "line contains a newline character"
    if len(text) > MAX_LENGTH:
        return "line is longer than %d characters" % MAX_LENGTH
    if "?" in text or "!" in text:
        return "line contains ? or !, so it is not one plain sentence"
    if not text.endswith("."):
        return "line does not end with a period"
    body = text[:-1]
    if ". " in body:
        return "line contains an extra sentence boundary"
    return None


def _pick_output_dir():
    """Choose where entry.txt goes: env var first, then /output, then out/."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        return wanted
    try:
        probe = os.path.join("/output", ".write-test")
        with open(probe, "wb") as handle:
            handle.write(b"")
        os.unlink(probe)
        return "/output"
    except OSError:
        return "out"


def _write_and_confirm(path, text):
    """Write *text* to *path*, read it back, and confirm byte equality."""
    payload = text.encode("utf-8")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(payload)
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        return None, "file content does not match the line byte-for-byte"
    return payload, None


def main():
    problem = _fails_shape(ROAST)
    if problem is not None:
        print("self-check failed: %s" % problem, file=sys.stderr)
        return 1

    folder = _pick_output_dir()
    target = os.path.join(folder, "entry.txt")
    try:
        payload, error = _write_and_confirm(target, ROAST)
    except OSError as exc:
        print("write failed: %s" % exc, file=sys.stderr)
        return 1
    if error is not None:
        print("write failed: %s" % error, file=sys.stderr)
        return 1

    print("Wrote %d bytes (%d chars) to %s" % (len(payload), len(ROAST), target))
    print(ROAST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
