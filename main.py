#!/usr/bin/env python3
"""Entry program for the news-image-20261119 bounty.

Writes the pre-composed front page (entry.png, built by compose.py and
stored beside this script) to the output directory from MAKEFUN_OUTPUT_DIR
(default /output). Deterministic: the same bytes are copied on every run,
so two runs produce byte-identical output. Standard library only.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")


if __name__ == "__main__":
    main()
