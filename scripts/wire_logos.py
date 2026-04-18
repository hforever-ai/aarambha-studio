#!/usr/bin/env python3
"""
Wire the installed logos into every HTML page:

  1. Replace the nav brand (the <span>आरम्भ</span>) with a circular logo
     image + Aarambha wordmark.
  2. Update favicon links to include apple-touch-icon.
  3. On /products/index.html, replace the Shrutam card emoji with the Shrutam
     circular logo.

Idempotent: uses unique class markers so re-running is safe.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# 1. Nav brand: replace the text wordmark with <img> + text
# ------------------------------------------------------------------
# Current pattern (we saw this on every page):
#   <span class="hindi text-2xl font-black text-accent leading-none">आरम्भ</span>
# followed by:
#   <span class="text-xs font-bold text-gray-400 tracking-[.14em] uppercase hidden sm:block">Aarambha</span>
# or similar. We'll surgically replace the first span with an <img>.

NAV_BRAND_OLD = '<span class="hindi text-2xl font-black text-accent leading-none">आरम्भ</span>'
NAV_BRAND_NEW = (
    '<img src="/assets/images/logos/aarambha-logo-96.webp" '
    'alt="Aarambha logo" '
    'width="36" height="36" '
    'class="aarambha-nav-logo w-9 h-9 rounded-full ring-1 ring-accent/40 shadow-sm shadow-accent/20" '
    'loading="eager">'
)

# ------------------------------------------------------------------
# 2. Favicon: ensure modern favicon links exist. We keep favicon.svg if
#    present but add apple-touch + explicit 192/512.
# ------------------------------------------------------------------
OLD_FAV_BLOCK = (
    '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
)
NEW_FAV_BLOCK = (
    '<link rel="icon" href="/favicon.ico" sizes="any">\n'
    '<link rel="icon" href="/assets/images/logos/aarambha-logo-192.png" type="image/png" sizes="192x192">\n'
    '<link rel="icon" href="/assets/images/logos/aarambha-logo-512.png" type="image/png" sizes="512x512">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">'
)

# Old-style favicon.ico line we want to drop (we inserted it above now)
OLD_ICO_LINE = '<link rel="icon" href="/favicon.ico" sizes="any">'

MARKER = "<!-- FAVICON_V2 -->"


def patch_nav_brand(text: str) -> tuple[str, int]:
    if NAV_BRAND_OLD not in text:
        return text, 0
    new_text = text.replace(NAV_BRAND_OLD, NAV_BRAND_NEW)
    return new_text, 1


def patch_favicon(text: str) -> tuple[str, int]:
    if MARKER in text:
        return text, 0
    if OLD_FAV_BLOCK not in text:
        return text, 0
    block = MARKER + "\n" + NEW_FAV_BLOCK
    new_text = text.replace(OLD_FAV_BLOCK, block, 1)
    # remove duplicate ico line (added separately earlier) if now-redundant
    # the OLD_ICO_LINE may appear twice: once in NEW_FAV_BLOCK and once original.
    # dedupe by replacing the second occurrence.
    first = new_text.find(OLD_ICO_LINE)
    if first >= 0:
        second = new_text.find(OLD_ICO_LINE, first + len(OLD_ICO_LINE))
        if second >= 0:
            new_text = new_text[:second] + new_text[second + len(OLD_ICO_LINE):]
    return new_text, 1


# ------------------------------------------------------------------
# 3. Shrutam card on /products/ — replace emoji tag with logo thumb.
# ------------------------------------------------------------------
# Old shrutam card prefix:
#   <h2 class="text-2xl md:text-3xl font-black mb-3"><span class="hindi text-accent mr-2">श्रुतम्</span><span class="text-gray-100">SHRUTAM</span></h2>
# Just add a logo <img> before the h2 inside its parent.

SHRUTAM_CARD_ANCHOR = '<h2 class="text-2xl md:text-3xl font-black mb-3"><span class="hindi text-accent mr-2">श्रुतम्</span><span class="text-gray-100">SHRUTAM</span></h2>'
SHRUTAM_CARD_LOGO = (
    '<img src="/assets/images/logos/shrutam-logo-256.webp" '
    'alt="Shrutam product logo" width="64" height="64" '
    'class="shrutam-card-logo w-16 h-16 rounded-full ring-1 ring-primary/30 mb-3" '
    'loading="lazy">\n          '
)


def patch_shrutam_card(text: str) -> tuple[str, int]:
    if "shrutam-card-logo" in text:
        return text, 0
    if SHRUTAM_CARD_ANCHOR not in text:
        return text, 0
    new_text = text.replace(
        SHRUTAM_CARD_ANCHOR,
        SHRUTAM_CARD_LOGO + SHRUTAM_CARD_ANCHOR
    )
    return new_text, 1


def patch_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    stats = {}
    text, n = patch_nav_brand(text);   stats["nav"]      = n
    text, n = patch_favicon(text);     stats["favicon"]  = n
    text, n = patch_shrutam_card(text); stats["shrutam"] = n
    if any(stats.values()):
        path.write_text(text, encoding="utf-8")
    return stats


def main() -> int:
    touched = 0
    for p in sorted(ROOT.rglob("*.html")):
        if any(s in p.parts for s in (".git", "node_modules", "docs")):
            continue
        stats = patch_file(p)
        if any(stats.values()):
            touched += 1
            print(f"  {p.relative_to(ROOT)}: {stats}")
    print(f"\ntouched {touched} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
