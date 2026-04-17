#!/usr/bin/env python3
"""Generate the 7 product-card illustrations + site OG default."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_client import gen_image
from lib_image  import save_as_webp, PRESETS

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "assets" / "images" / "products"

STYLE = (
    "Editorial dark illustration, cosmos-navy #060d1a background with subtle depth. "
    "Warm amber #f59e0b and sky-blue #0ea5e9 as singular accent lights. "
    "Premium magazine quality, restrained, one subject centered, generous negative space. "
    "NO text, NO logos, NO watermarks. Square composition."
)

SUBJECTS = {
    "shrutam":   "A single phone on a wooden village desk at dusk, its screen emitting a soft amber glow of audio learning, a notebook and pen beside it.",
    "commerce":  "A shopkeeper's hand holding a phone with a WhatsApp-like chat glowing, against a kirana shop shelf backdrop, dusk lighting.",
    "karta":     "A clean stack of invoices on a desk being read by an invisible presence — a single sky-blue scan line across them, small amber desk lamp.",
    "pashu":     "A calm cow in a rural Indian stable at dawn, a subtle sky-blue diagnostic outline on the animal's flank, misty amber light.",
    "bima":      "A medical bill document softly highlighted in sky-blue as if AI is reading it, on a dark table with warm amber ambient light.",
    "svayam":    "A blank Indian government form being filled by an invisible voice — field outlines gently glowing sky-blue, warm amber ambient.",
    "adhikar":   "An elderly hand holding a simple phone that emits a gentle sky-blue voice indicator, the background a blurred veranda at dusk.",
}

OG_DEFAULT = (
    "A single amber diya glowing softly at the foot of a dark cosmic sky with scattered stars, "
    "a faint horizon line suggesting an Indian village, editorial minimalist composition. "
    "Restrained, ceremonial, no text."
)

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "images").mkdir(parents=True, exist_ok=True)

    for slug, subject in SUBJECTS.items():
        out = OUT / f"{slug}.webp"
        if out.exists():
            print(f"exists: {out.relative_to(ROOT)} — skip (delete to regenerate)")
            continue
        print(f"generating {slug}...")
        png = gen_image(f"{STYLE}\n\nSubject: {subject}")
        size = save_as_webp(png, out, **PRESETS["product-card"])
        print(f"  saved {size // 1024} KB")

    # Site-wide OG default (1200x630)
    og_out = ROOT / "assets" / "images" / "og-default.webp"
    if og_out.exists():
        print(f"exists: {og_out.relative_to(ROOT)} — skip")
    else:
        print("generating og-default ...")
        png = gen_image(f"{STYLE}\n\nSubject: {OG_DEFAULT}")
        size = save_as_webp(png, og_out, **PRESETS["og-default"])
        print(f"  saved {size // 1024} KB")

    return 0

if __name__ == "__main__":
    sys.exit(main())
