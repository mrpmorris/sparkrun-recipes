#!/usr/bin/env python3
"""Cap the `stop` list at 4 entries in lm-eval's local-completions payload.

vLLM 0.27+ enforces the OpenAI limit of at most 4 stop sequences. lm-eval's
humaneval task ships 5 (`\\nclass`, `\\ndef`, `\\n#`, `\\nif`, `\\nprint`), so every
humaneval request is rejected with:

    400 {"error":{"message":"2 validation errors: ...
         {'type': 'too_long', 'loc': ('body', 'stop', 'list[str]'),
          'msg': 'List should have at most 4 items ...

lm-eval already trims to `stop[:4]` in LocalChatCompletion and
OpenAIChatCompletion; LocalCompletionsAPI (the `--model local-completions`
path benchllm uses) is the one that does not. This applies the same trim there.

Idempotent. Exits non-zero and changes nothing if the anchor cannot be found
uniquely, so an lm-eval upgrade that moves the line fails loudly instead of
silently reverting to 1150 HTTP 400s per run.

Usage: <venv>/bin/python patch-lm-eval-stop.py [--check]
       --check  report status only, never write (exit 1 if unpatched)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CLASS = "class LocalCompletionsAPI"
ANCHOR = '"stop": stop,'
REPLACEMENT = '"stop": stop[:4],  # patched by patch-lm-eval-stop.py: vLLM 0.27+ caps stop at 4'
PATCHED_MARK = '"stop": stop[:4],'


def find_target() -> Path:
    try:
        import lm_eval.models.openai_completions as mod
    except ImportError as exc:
        sys.exit(f"patch-lm-eval-stop: cannot import lm_eval ({exc}). "
                 f"Run me with the benchllm venv's python.")
    return Path(mod.__file__)


def class_region(src: str) -> tuple[int, int]:
    """Byte range of LocalCompletionsAPI, up to the next top-level class."""
    start = src.find(CLASS)
    if start == -1:
        sys.exit(f"patch-lm-eval-stop: {CLASS} not found - lm-eval layout changed.")
    nxt = re.search(r"^class ", src[start + len(CLASS):], re.MULTILINE)
    end = start + len(CLASS) + nxt.start() if nxt else len(src)
    return start, end


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report only, do not write")
    args = ap.parse_args()

    path = find_target()
    src = path.read_text(encoding="utf-8")
    start, end = class_region(src)
    region = src[start:end]

    if PATCHED_MARK in region:
        print(f"patch-lm-eval-stop: already patched ({path})")
        return

    n = region.count(ANCHOR)
    if n != 1:
        sys.exit(f"patch-lm-eval-stop: expected exactly 1 occurrence of {ANCHOR!r} "
                 f"in {CLASS}, found {n} in {path}. Refusing to guess - "
                 f"lm-eval changed, update this script.")

    if args.check:
        sys.exit(f"patch-lm-eval-stop: NOT patched ({path}). "
                 f"humaneval will fail with HTTP 400 'stop: too_long'.")

    path.write_text(src[:start] + region.replace(ANCHOR, REPLACEMENT) + src[end:],
                    encoding="utf-8")
    print(f"patch-lm-eval-stop: patched {path} ({CLASS}: stop -> stop[:4])")


if __name__ == "__main__":
    main()
