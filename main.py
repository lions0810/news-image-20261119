#!/usr/bin/env python3
"""Entry program for the news-image-20261119 bounty.

Writes the pre-composed front page (entry.png, built by compose.py and
stored beside this script) to the output directory from MAKEFUN_OUTPUT_DIR
(default /output). Deterministic: the same bytes are copied on every run,
so two runs produce byte-identical output. Standard library only.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the output before reporting success: the bytes written must
    # equal the bundled entry bytes exactly, and the file must be at most
    # 1 MiB. Fail loudly instead of shipping a truncated or corrupt copy.
    with open(src, "rb") as f:
        expected = f.read()
    with open(dst, "rb") as f:
        actual = f.read()
    if actual != expected:
        print("ERROR: output entry.png bytes differ from bundled entry.png",
              file=sys.stderr)
        sys.exit(1)
    if len(actual) > 1024 * 1024:
        print(f"ERROR: output entry.png is {len(actual)} bytes, over the "
              "1 MiB limit", file=sys.stderr)
        sys.exit(1)
    print(f"copied {src} -> {dst} ({len(actual)} bytes, verified)")


if __name__ == "__main__":
    main()
