#!/usr/bin/env python3
"""Deterministic entry runner for news-image-20261119.

The entry is a finished front-page image, bundled in this repository as
``entry.png``. Running this script copies those exact bytes into an
output directory and proves the copy is faithful:

* the written file is byte-for-byte identical to the bundled image
  (matching SHA-256 digests), and
* the file stays within the 1 MiB entry limit.

Any mismatch or oversize file exits non-zero, so a bad copy can never
pass as a good one. The operation is fully deterministic: the same
bundled bytes always produce the same output file.
"""

from __future__ import annotations

import argparse
import hashlib
import struct
import sys
from pathlib import Path

# Entry limit: 1 MiB.
MAX_BYTES = 1_048_576

# The bundled front page lives next to this script.
BUNDLED = Path(__file__).resolve().parent / "entry.png"

# Expected dimensions of the front page.
EXPECT_WIDTH = 1024
EXPECT_HEIGHT = 1024

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png_image(data: bytes) -> tuple[int, int]:
    """Confirm *data* is a PNG of the expected front-page dimensions.

    Parses the 8-byte signature and the IHDR chunk directly, so a
    mislabelled or wrong-sized file is caught even when its bytes
    happen to match the bundle. Returns (width, height).
    """
    if data[:8] != PNG_SIGNATURE:
        raise SystemExit("verification failed: not a PNG file")
    if len(data) < 24:
        raise SystemExit("verification failed: PNG too short for IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECT_WIDTH, EXPECT_HEIGHT):
        raise SystemExit(
            f"verification failed: image is {width}x{height}, "
            f"expected {EXPECT_WIDTH}x{EXPECT_HEIGHT}"
        )
    return width, height


def sha256_hex(data: bytes) -> str:
    """Return the lowercase hex SHA-256 digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def read_bundle() -> bytes:
    """Read the bundled image, refusing to continue if it is unusable."""
    if not BUNDLED.is_file():
        raise SystemExit(f"bundled image not found: {BUNDLED}")
    data = BUNDLED.read_bytes()
    if not data:
        raise SystemExit("bundled image is empty")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"bundled image is {len(data)} bytes, over the "
            f"{MAX_BYTES}-byte limit"
        )
    return data


def write_output(data: bytes, out_dir: Path) -> Path:
    """Write *data* to ``<out_dir>/entry.png`` and return its path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    return target


def verify_copy(source: bytes, target: Path) -> tuple[str, int, int]:
    """Check the written file against the source bytes.

    Returns (shared SHA-256 digest, width, height). Exits non-zero on
    any mismatch.
    """
    written = target.read_bytes()
    if written != source:
        raise SystemExit(
            f"verification failed: {target} differs from the bundle"
        )
    width, height = check_png_image(written)
    digest = sha256_hex(written)
    if sha256_hex(source) != digest:
        raise SystemExit("verification failed: digest mismatch")
    if len(written) > MAX_BYTES:
        raise SystemExit(
            f"verification failed: output is {len(written)} bytes, "
            f"over the {MAX_BYTES}-byte limit"
        )
    return digest, width, height


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the bundled entry.png to an output directory "
                    "and verify the copy."
    )
    parser.add_argument(
        "--output", "-o", default="out", type=Path,
        help="output directory (default: out)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data = read_bundle()
    target = write_output(data, args.output)
    digest, width, height = verify_copy(data, target)
    print(f"entry.png: {width}x{height}, {len(data)} bytes, "
          f"sha256 {digest}")
    print(f"verified copy written to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
