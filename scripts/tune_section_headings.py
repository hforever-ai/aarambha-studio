#!/usr/bin/env python3
"""
Tune oversized section <h2> headings across all core pages.

Target pattern:
  h2 class="text-3xl md:text-5xl ..."   (30 → 48px)  — section headings at hero size
Replace with:
  h2 class="text-[26px] md:text-4xl ..."(26 → 36px)  — editorial section size

Also touches text-3xl md:text-4xl on h2 (keeps hero-level h1s like the homepage
main headline unchanged — they're on h1 elements, not h2).

Idempotent.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Core pages + their HI mirrors (apply_i18n already duplicated sections)
PAGES = [
    ROOT / "index.html",
    ROOT / "about" / "index.html",
    ROOT / "products" / "index.html",
    ROOT / "philosophy" / "index.html",
    ROOT / "contact" / "index.html",
    ROOT / "blog" / "index.html",
]

# Match <h2 ...class="...text-3xl md:text-5xl..." ...> regardless of other classes/attrs
H2_PATTERN = re.compile(
    r'(<h2[^>]*\bclass="[^"]*?)\btext-3xl\s+md:text-5xl\b'
)


def patch_file(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    new_text, n = H2_PATTERN.subn(
        r'\1text-[26px] md:text-4xl',
        text
    )
    if n > 0:
        path.write_text(new_text, encoding="utf-8")
    return n


def main() -> int:
    total = 0
    for p in PAGES:
        n = patch_file(p)
        print(f"{p.relative_to(ROOT)}: tuned {n} h2s")
        total += n
    print(f"\ntotal: {total} h2s retuned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
