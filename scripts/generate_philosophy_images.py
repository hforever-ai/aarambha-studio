#!/usr/bin/env python3
"""Generate 6 editorial images: Pancha Bhoota 5 elements + 22/7 woodcutter."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_client import gen_image
from lib_image  import save_as_webp, PRESETS

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "assets" / "images" / "philosophy"

STYLE = (
    "Editorial dark illustration, cosmos-navy #060d1a background with subtle depth. "
    "Warm amber #f59e0b and sky-blue #0ea5e9 as singular accent lights. "
    "Premium magazine quality, ceremonial, one symbolic subject, negative space. "
    "NO text, NO logos, NO watermarks."
)

SUBJECTS = {
    "prithvi":    "A single leaf on dark earth, with a soft amber light from below as if the leaf itself glows with life — knowledge grounding everything.",
    "vayu":       "A wisp of luminous wind carrying a paisley-pattern trail across the dark sky, sky-blue highlights, amber accents — commerce flowing like air.",
    "tejas":      "A small brilliant amber flame alone in the dark, casting faint sky-blue ripples around it — clarity igniting.",
    "jal":        "A single drop of water suspended mid-air, reflecting amber and sky-blue lights inside it, dark background, ceremonial — life-giving.",
    "akasha":     "A constellation of tiny sky-blue pinpoints against the cosmos, loosely connecting like a web, one amber pinpoint brighter in the centre — the connective space.",
    "woodcutter": "A single axe standing upright next to a small whetstone and a coiled rope, on dark earth-toned table, warm amber side light, cinematic and meditative.",
}

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, subject in SUBJECTS.items():
        out = OUT / f"{slug}.webp"
        if out.exists():
            print(f"exists: {out.relative_to(ROOT)} — skip (delete to regenerate)")
            continue
        print(f"generating {slug}...")
        png = gen_image(f"{STYLE}\n\nSubject: {subject}")
        size = save_as_webp(png, out, **PRESETS["philosophy"])
        print(f"  saved {size // 1024} KB")
    return 0

if __name__ == "__main__":
    sys.exit(main())
