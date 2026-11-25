#!/usr/bin/env python3
"""Deploy the bundled entry.png into the make.fun output directory.

Standard library only. The copy is staged as a temporary file *inside* the
output directory, given mode 0644, then moved into place with os.replace()
so the grader never observes a partial or mode-0600 file.

Usage:
    python3 main.py                 # writes $MAKEFUN_OUTPUT_DIR/entry.png
    MAKEFUN_OUTPUT_DIR=./out python3 main.py
"""

import hashlib
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
FILE_MODE = 0o644


class DeployError(Exception):
    """A deployment step failed; message is shown to the user verbatim."""


def check_png(path, label):
    """Validate PNG magic bytes and size limit; return (size, sha256)."""
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        raise DeployError(f"{label}: cannot stat {path}: {exc}") from exc

    if size > MAX_BYTES:
        raise DeployError(
            f"{label}: {path} is {size} bytes, over the {MAX_BYTES}-byte limit"
        )
    if size < len(PNG_MAGIC):
        raise DeployError(f"{label}: {path} is only {size} bytes, not a PNG")

    with open(path, "rb") as fh:
        head = fh.read(len(PNG_MAGIC))
        if head != PNG_MAGIC:
            raise DeployError(
                f"{label}: {path} does not start with PNG magic bytes "
                f"(got {head!r})"
            )
        digest = hashlib.sha256()
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)

    return size, digest.hexdigest()


def deploy(source=SOURCE, output_dir=None):
    """Copy source into output_dir/entry.png atomically. Returns final path."""
    if output_dir is None:
        output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR

    if not os.path.isfile(source):
        raise DeployError(f"source image is missing: {source}")

    src_size, src_sha = check_png(source, "source")

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        raise DeployError(
            f"cannot create output directory {output_dir}: {exc}"
        ) from exc

    if not os.path.isdir(output_dir):
        raise DeployError(f"output path is not a directory: {output_dir}")

    dest = os.path.join(output_dir, OUTPUT_NAME)
    staged = None
    try:
        fd, staged = tempfile.mkstemp(
            prefix=".entry-", suffix=".png.tmp", dir=output_dir
        )
        try:
            with os.fdopen(fd, "wb") as out, open(source, "rb") as src:
                while True:
                    chunk = src.read(1 << 20)
                    if not chunk:
                        break
                    out.write(chunk)
                out.flush()
                os.fsync(out.fileno())

            # mkstemp creates 0600; the grader reads as another user.
            os.chmod(staged, FILE_MODE)

            dst_size, dst_sha = check_png(staged, "staged copy")
            if dst_size != src_size or dst_sha != src_sha:
                raise DeployError(
                    "staged copy does not match source "
                    f"(source {src_size} bytes {src_sha}, "
                    f"staged {dst_size} bytes {dst_sha})"
                )

            os.replace(staged, dest)
            staged = None
        finally:
            if staged is not None:
                try:
                    os.unlink(staged)
                except OSError:
                    pass
    except DeployError:
        raise
    except OSError as exc:
        raise DeployError(f"failed to write {dest}: {exc}") from exc

    final_size, final_sha = check_png(dest, "deployed file")
    if final_sha != src_sha:
        raise DeployError(
            f"deployed file {dest} does not match source "
            f"({final_sha} != {src_sha})"
        )

    mode = os.stat(dest).st_mode & 0o777
    if mode != FILE_MODE:
        raise DeployError(
            f"deployed file {dest} has mode {mode:04o}, expected {FILE_MODE:04o}"
        )

    print(f"deployed {dest} ({final_size} bytes, mode {mode:04o})")
    print(f"sha256 {final_sha}")
    return dest


def main(argv):
    output_dir = None
    if len(argv) > 2:
        print(f"usage: {os.path.basename(argv[0])} [output_dir]", file=sys.stderr)
        return 2
    if len(argv) == 2:
        output_dir = argv[1]

    try:
        deploy(output_dir=output_dir)
    except DeployError as exc:
        print(f"main.py: error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
