#!/usr/bin/env python3
"""Build a Chrome-style squircle app icon from a square source image."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageChops


def squircle_icon(src: Path, out: Path, size: int = 1024) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    im = im.crop((left, top, left + side, top + side))
    im = im.resize((size, size), Image.Resampling.LANCZOS)

    # ~22% corner radius (Big Sur / Chrome-style squircle)
    radius = max(8, int(size * 0.223))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)

    r, g, b, a = im.split()
    new_a = ImageChops.darker(a, mask)
    out_img = Image.merge("RGBA", (r, g, b, new_a))
    out_img.save(out, "PNG")


if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    squircle_icon(src, dst)
