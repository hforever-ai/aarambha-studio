#!/usr/bin/env python3
"""
Tune product/feature card <h2> sizes. Cards are smaller than section heads.

Replacements:
  text-3xl md:text-4xl   (30 → 36px) → text-2xl md:text-3xl  (24 → 30px)
  text-[26px] md:text-4xl (26 → 36px) → text-2xl md:text-3xl (24 → 30px)

Only applies to h2 elements (section headings already sized separately).

Idempotent.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    ROOT / "index.html",
    ROOT / "about" / "index.html",
    ROOT / "products" / "index.html",
    ROOT / "philosophy" / "index.html",
    ROOT / "contact" / "index.html",
]

REPLACEMENTS = [
    (re.compile(r'(<h2[^>]*\bclass="[^"]*?)\btext-3xl\s+md:text-4xl\b'),
     r'\1text-2xl md:text-3xl'),
    (re.compile(r'(<h2[^>]*\bclass="[^"]*?)\btext-\[26px\]\s+md:text-4xl\b'),
     r'\1text-2xl md:text-3xl'),
]


def patch_file(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    total = 0
    for pat, rep in REPLACEMENTS:
        text, n = pat.subn(rep, text)
        total += n
    if total > 0:
        path.write_text(text, encoding="utf-8")
    return total


def main() -> int:
    grand = 0
    for p in PAGES:
        n = patch_file(p)
        print(f"{p.relative_to(ROOT)}: tuned {n} h2s")
        grand += n
    print(f"\ntotal: {grand}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
