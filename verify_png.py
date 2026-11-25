#!/usr/bin/env python3
"""Verify that entry.png is a whole, valid 1024x1024 PNG under 1 MiB.

Checks the file end to end: signature, every chunk's length and CRC, the IHDR
dimensions, that image data is present, and that the stream ends with IEND and
no trailing bytes. Prints the sha256 on success.

Usage:
    python3 verify_png.py [path]      # default: entry.png next to this script
"""

import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(HERE, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_W = EXPECTED_H = 1024


class BadPNG(Exception):
    pass


def verify(path):
    """Raise BadPNG on any defect; return (size, sha256, width, height)."""
    if not os.path.isfile(path):
        raise BadPNG(f"not a file: {path}")

    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise BadPNG(f"{size} bytes, over the {MAX_BYTES}-byte limit")
    if size < len(PNG_MAGIC) + 12:
        raise BadPNG(f"{size} bytes, too short to be a PNG")

    with open(path, "rb") as fh:
        data = fh.read()

    sha = hashlib.sha256(data).hexdigest()

    if data[:8] != PNG_MAGIC:
        raise BadPNG(f"bad signature: {data[:8]!r}")

    pos = 8
    first = True
    width = height = None
    saw_data = False
    saw_iend = False

    while pos < len(data):
        if pos + 8 > len(data):
            raise BadPNG(f"truncated chunk header at offset {pos}")
        length, ctype = struct.unpack(">I4s", data[pos : pos + 8])
        if length > 0x7FFFFFFF:
            raise BadPNG(f"chunk {ctype!r} has illegal length {length}")

        body_start = pos + 8
        body_end = body_start + length
        crc_end = body_end + 4
        if crc_end > len(data):
            raise BadPNG(
                f"chunk {ctype!r} at offset {pos} runs past end of file "
                f"(needs {crc_end} bytes, file has {len(data)})"
            )

        body = data[body_start:body_end]
        (stored_crc,) = struct.unpack(">I", data[body_end:crc_end])
        actual_crc = zlib.crc32(ctype + body) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise BadPNG(
                f"chunk {ctype!r} at offset {pos} has CRC {stored_crc:08x}, "
                f"computed {actual_crc:08x}"
            )

        if first:
            if ctype != b"IHDR":
                raise BadPNG(f"first chunk is {ctype!r}, expected IHDR")
            if length != 13:
                raise BadPNG(f"IHDR length is {length}, expected 13")
            width, height = struct.unpack(">II", body[:8])
            first = False
        elif ctype == b"IDAT":
            saw_data = True
        elif ctype == b"IEND":
            if length != 0:
                raise BadPNG(f"IEND length is {length}, expected 0")
            saw_iend = True
            pos = crc_end
            break

        pos = crc_end

    if width is None:
        raise BadPNG("no IHDR chunk found")
    if not saw_data:
        raise BadPNG("no IDAT chunk found; image has no data")
    if not saw_iend:
        raise BadPNG("stream ended without IEND; file is truncated")
    if pos != len(data):
        raise BadPNG(f"{len(data) - pos} trailing bytes after IEND")
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        raise BadPNG(
            f"dimensions are {width}x{height}, expected {EXPECTED_W}x{EXPECTED_H}"
        )

    return size, sha, width, height


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_PATH
    if len(argv) > 2:
        print(f"usage: {os.path.basename(argv[0])} [path]", file=sys.stderr)
        return 2

    try:
        size, sha, width, height = verify(path)
    except BadPNG as exc:
        print(f"verify_png.py: INVALID: {path}: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"verify_png.py: error reading {path}: {exc}", file=sys.stderr)
        return 1

    print(f"ok: {path}")
    print(f"  {width}x{height}, {size} bytes (limit {MAX_BYTES})")
    print(f"  sha256 {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
