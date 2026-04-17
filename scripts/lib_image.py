#!/usr/bin/env python3
"""Image post-processing: crop, resize, compress, save WebP."""
from __future__ import annotations
import io
from pathlib import Path
from PIL import Image


def _crop_to_ratio(img: Image.Image, ratio: float) -> Image.Image:
    """Centre-crop image to the given width/height ratio."""
    w, h = img.size
    cur = w / h
    if abs(cur - ratio) < 0.01:
        return img
    if cur > ratio:
        new_w = int(h * ratio)
        left  = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    new_h = int(w / ratio)
    top   = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def save_as_webp(png_bytes: bytes, out_path: Path, *, width: int, height: int, quality: int = 82) -> int:
    """Crop to `width:height` ratio, resize, save WebP. Returns bytes written."""
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img = _crop_to_ratio(img, width / height)
    img = img.resize((width, height), Image.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "WEBP", quality=quality, method=6)
    return out_path.stat().st_size


# Standard aspect presets used across the site
PRESETS = {
    "blog-hero":        {"width": 1200, "height": 630, "quality": 82},
    "blog-hero-large":  {"width": 1600, "height": 840, "quality": 80},
    "product-card":     {"width":  800, "height": 800, "quality": 85},
    "philosophy":       {"width": 1200, "height": 800, "quality": 82},
    "og-default":       {"width": 1200, "height": 630, "quality": 82},
}
