#!/usr/bin/env python3
"""
Tune oversized page-hero <h1> headings across core pages.

Replacements (h1 only — homepage hero headline stays hero-scale):
  text-4xl md:text-6xl   (36 → 60px) → text-[32px] md:text-5xl  (32 → 48px)
  text-5xl md:text-7xl   (48 → 72px) → text-4xl md:text-5xl     (36 → 48px)

Also tone down stat numbers on homepage:
  text-5xl md:text-6xl   (48 → 60px) → text-4xl md:text-5xl     (36 → 48px)

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

# (regex, replacement) pairs — order matters
REPLACEMENTS = [
    # h1 page heroes
    (re.compile(r'(<h1[^>]*\bclass="[^"]*?)\btext-4xl\s+md:text-6xl\b'),
     r'\1text-[32px] md:text-5xl'),
    (re.compile(r'(<h1[^>]*\bclass="[^"]*?)\btext-5xl\s+md:text-7xl\b'),
     r'\1text-4xl md:text-5xl'),
    # stats (numbers in homepage stat blocks)
    (re.compile(r'(<div[^>]*\bclass="[^"]*?)\btext-5xl\s+md:text-6xl\b'),
     r'\1text-4xl md:text-5xl'),
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
        print(f"{p.relative_to(ROOT)}: tuned {n} elements")
        grand += n
    print(f"\ntotal: {grand}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
