#!/usr/bin/env python3
"""
Install Aarambha + Shrutam logos from ~/Downloads and generate web variants.

Outputs:
  /favicon.ico                    (multi-res 16/32/48)
  /apple-touch-icon.png           (180×180)
  /assets/images/logos/aarambha-logo-512.webp
  /assets/images/logos/aarambha-logo-96.webp   (nav)
  /assets/images/logos/aarambha-logo-192.png   (manifest)
  /assets/images/logos/aarambha-logo-512.png   (manifest / OG fallback)
  /assets/images/logos/shrutam-logo-512.webp
  /assets/images/logos/shrutam-logo-256.webp   (product card)

Idempotent: overwrites outputs every run.
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = Path.home() / "Downloads"
LOGO_A = DOWNLOADS / "AarambhamX-logo.png"
LOGO_S = DOWNLOADS / "Shrutam-logo.png"

LOGOS_DIR = ROOT / "assets" / "images" / "logos"
LOGOS_DIR.mkdir(parents=True, exist_ok=True)


def _resize(src: Image.Image, size: int) -> Image.Image:
    out = src.copy()
    out.thumbnail((size, size), Image.LANCZOS)
    # make exact square
    w, h = out.size
    if (w, h) != (size, size):
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.paste(out, ((size - w) // 2, (size - h) // 2), out if out.mode == "RGBA" else None)
        out = canvas
    return out


def save_webp(img: Image.Image, path: Path, quality: int = 88) -> int:
    img.save(path, "WEBP", quality=quality, method=6)
    return path.stat().st_size


def save_png(img: Image.Image, path: Path) -> int:
    img.save(path, "PNG", optimize=True)
    return path.stat().st_size


def main() -> int:
    if not LOGO_A.exists():
        print(f"ERROR: {LOGO_A} not found", file=sys.stderr); return 2
    if not LOGO_S.exists():
        print(f"ERROR: {LOGO_S} not found", file=sys.stderr); return 2

    a = Image.open(LOGO_A).convert("RGBA")
    s = Image.open(LOGO_S).convert("RGBA")

    # --- Aarambha ---
    for size, ext in [(96, "webp"), (512, "webp")]:
        out = LOGOS_DIR / f"aarambha-logo-{size}.{ext}"
        save_webp(_resize(a, size), out)
        print(f"  wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

    # PNG variants for manifest / OG
    for size in (192, 512):
        out = LOGOS_DIR / f"aarambha-logo-{size}.png"
        save_png(_resize(a, size), out)
        print(f"  wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

    # Apple touch icon (180×180) at repo root
    apple = ROOT / "apple-touch-icon.png"
    save_png(_resize(a, 180), apple)
    print(f"  wrote {apple.relative_to(ROOT)} ({apple.stat().st_size // 1024} KB)")

    # Favicon .ico with multiple sizes
    ico = ROOT / "favicon.ico"
    sizes = [(16, 16), (32, 32), (48, 48)]
    # PIL can write multi-size ICO via sizes=
    ico_img = _resize(a, 48)
    ico_img.save(ico, format="ICO", sizes=sizes)
    print(f"  wrote {ico.relative_to(ROOT)} ({ico.stat().st_size // 1024} KB)")

    # --- Shrutam ---
    for size in (256, 512):
        out = LOGOS_DIR / f"shrutam-logo-{size}.webp"
        save_webp(_resize(s, size), out)
        print(f"  wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
