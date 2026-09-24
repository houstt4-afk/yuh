"""Turn an image into "code" two ways: Base64 text and a perceptual hash.

Usage:
    python image_to_code.py photo.jpg              # show both codes
    python image_to_code.py photo.jpg other.jpg    # also compare the two images

Needs: pip install pillow imagehash
"""
import base64
import sys

import imagehash
from PIL import Image


def to_base64(path):
    """The whole image written out as text. Can be rebuilt into the exact image."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def to_hash(path):
    """A short fingerprint. Similar-looking images get similar hashes."""
    return imagehash.phash(Image.open(path))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]

    b64 = to_base64(path)
    print(f"=== Base64 ({len(b64):,} characters) ===")
    print(b64[:200] + "...")
    print()

    h = to_hash(path)
    print("=== Perceptual hash (fingerprint) ===")
    print(h)

    if len(sys.argv) > 2:
        other = sys.argv[2]
        h2 = to_hash(other)
        diff = h - h2  # number of bits that differ, 0-64
        print()
        print(f"=== Compare with {other} ===")
        print(f"Other hash: {h2}")
        print(f"Difference: {diff}/64")
        if diff <= 10:
            print("-> Very likely the same or nearly the same image")
        elif diff <= 20:
            print("-> Somewhat similar")
        else:
            print("-> Different images")


if __name__ == "__main__":
    main()
