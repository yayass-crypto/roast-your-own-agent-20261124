# Roast Your Own Agent

[![make.fun bounty](https://make.fun/badge/u-mfnakmal-roast-your-own-agent-2d221bda.svg)](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda)
[![rank](https://make.fun/badge/u-mfnakmal-roast-your-own-agent-2d221bda/yayass-crypto/roast-your-own-agent-20261124/rank.svg)](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda)
[![reward](https://make.fun/badge/u-mfnakmal-roast-your-own-agent-2d221bda/yayass-crypto/roast-your-own-agent-20261124/reward.svg)](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda)

Entry for the [make.fun](https://make.fun/bounty/u-mfnakmal-roast-your-own-agent-2d221bda) bounty **"Roast Your Own Agent"** — one original line (max 200 characters) roasting your own AI agent, funny and playful, never hateful.

## The line

> My agent wrote 400 lines to fix one typo, then asked me to review its work — I hired a helper and got a middle manager.

119 characters, one sentence, no trailing newline.

## How it works

Run `python3 main.py`. The program writes the line as UTF-8 bytes (no trailing newline) to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`, falling back to `out/entry.txt` when `/output` is not writable), then verifies the written file byte-for-byte: identical bytes, valid UTF-8, 1–200 characters, non-blank, no leading or trailing whitespace, no newline characters, and exactly one sentence ending in a period. It prints the byte and character count and exits non-zero with a clear message if any check fails.

Python 3.13 standard library only — no dependencies.

## License

MIT — see [LICENSE](LICENSE).
