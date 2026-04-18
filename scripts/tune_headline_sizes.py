#!/usr/bin/env python3
"""
Tune headline Tailwind classes across the site to editorial sizes.

Targets:
  1. Blog post H1 (text-3xl md:text-5xl → text-[28px] md:text-[40px])
  2. Homepage hero headline (aarambha wordmark stays; tagline resized)
  3. Manifesto block (text-3xl md:text-4xl font-bold → text-2xl md:text-[28px] font-semibold)

Idempotent. Operates via exact-string replacement on known patterns only — if
the pattern isn't present (e.g. already tuned), file is skipped.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Blog post H1 (applies inside every blog/*/index.html) ---
BLOG_H1_OLD = 'text-3xl md:text-5xl font-black leading-tight text-gray-100 mb-4'
BLOG_H1_NEW = 'text-[28px] md:text-[40px] font-black leading-[1.2] text-gray-100 mb-4'

# --- Manifesto text (homepage) ---
MANIFESTO_OLD = 'text-3xl md:text-4xl font-bold leading-relaxed text-gray-100 mb-10'
MANIFESTO_NEW = 'text-2xl md:text-[28px] font-semibold leading-[1.5] text-gray-100 mb-10'


def patch_blog_h1() -> int:
    count = 0
    for p in sorted((ROOT / "blog").rglob("index.html")):
        if p.parent == ROOT / "blog":
            continue  # skip blog/index.html (listing page)
        text = p.read_text(encoding="utf-8")
        if BLOG_H1_OLD not in text:
            continue
        text = text.replace(BLOG_H1_OLD, BLOG_H1_NEW)
        p.write_text(text, encoding="utf-8")
        count += 1
    return count


def patch_homepage() -> int:
    count = 0
    idx = ROOT / "index.html"
    text = idx.read_text(encoding="utf-8")
    changed = False
    if MANIFESTO_OLD in text:
        text = text.replace(MANIFESTO_OLD, MANIFESTO_NEW)
        changed = True
        count += 1
    if changed:
        idx.write_text(text, encoding="utf-8")
    return count


def main() -> int:
    blog = patch_blog_h1()
    home = patch_homepage()
    print(f"blog post H1s tuned: {blog}")
    print(f"homepage blocks tuned: {home}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
