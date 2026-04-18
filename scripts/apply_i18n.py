#!/usr/bin/env python3
"""
Apply i18n-cache.yaml to the 5 core pages — preserving original formatting.

Strategy:
  1. Scan source for <section ...> opening tags via regex.
  2. For each, balance-count forward until matching </section> to get raw slice.
  3. Parse slice with BS4 → hash of normalized form → look up in cache.
  4. If found: mutate the ORIGINAL RAW SLICE (inject x-show into opening tag)
     and splice in the HI section after it. Write back with minimal diff.

Idempotent: skips sections whose opening tag already contains x-show.
"""
from __future__ import annotations
import hashlib, re, sys, yaml
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / "content" / "i18n-cache.yaml"
CACHE = yaml.safe_load(CACHE_PATH.read_text()) or {}

PAGES = [
    "index.html",
    "about/index.html",
    "products/index.html",
    "philosophy/index.html",
    "contact/index.html",
]

OPEN_RE  = re.compile(r'<section\b[^>]*>', re.IGNORECASE)
CLOSE_RE = re.compile(r'</section\s*>', re.IGNORECASE)


def _hash(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


def _find_section_ranges(text: str) -> list[tuple[int, int]]:
    """Return (start, end) byte offsets for each top-level <section>...</section>.
    Handles nesting via a depth counter."""
    ranges = []
    i = 0
    n = len(text)
    while i < n:
        om = OPEN_RE.search(text, i)
        if not om:
            break
        start = om.start()
        depth = 1
        pos = om.end()
        while pos < n and depth > 0:
            next_open  = OPEN_RE.search(text, pos)
            next_close = CLOSE_RE.search(text, pos)
            if not next_close:
                break  # malformed
            if next_open and next_open.start() < next_close.start():
                depth += 1
                pos = next_open.end()
            else:
                depth -= 1
                pos = next_close.end()
                if depth == 0:
                    ranges.append((start, pos))
                    break
        i = pos
    return ranges


def _only_inside_main(text: str, ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    main_start = text.find("<main")
    main_end   = text.find("</main>", main_start + 1) if main_start >= 0 else -1
    if main_start < 0 or main_end < 0:
        return []
    return [(s, e) for (s, e) in ranges if s >= main_start and e <= main_end]


def _inject_xshow_en(opening: str) -> str:
    """Insert x-show='en' into a <section ...> opening tag."""
    return re.sub(
        r'^<section\b',
        '<section x-show="$store.lang.current === \'en\'"',
        opening,
        count=1,
    )


def _inject_xshow_hi_cloak(section_html: str) -> str:
    """Insert x-cloak + x-show='hi' into the HI <section ...> opening tag."""
    return re.sub(
        r'^<section\b',
        '<section x-cloak x-show="$store.lang.current === \'hi\'"',
        section_html,
        count=1,
    )


def patch_file(rel_path: str) -> int:
    path = ROOT / rel_path
    text = path.read_text(encoding="utf-8")

    ranges = _only_inside_main(text, _find_section_ranges(text))
    # Process from the END so earlier offsets stay valid
    count = 0
    for start, end in reversed(ranges):
        raw_slice = text[start:end]

        # Skip if already patched (opening tag already carries x-show)
        opening_tag_match = re.match(r'<section\b[^>]*>', raw_slice)
        if not opening_tag_match:
            continue
        opening_tag = opening_tag_match.group(0)
        if "x-show=" in opening_tag:
            continue

        # Compute hash of this section via BS4 normalization (same as generator)
        frag = BeautifulSoup(raw_slice, "html.parser")
        sec = frag.find("section")
        if sec is None:
            continue
        h = _hash(str(sec))
        if h not in CACHE:
            continue
        hi_html = CACHE[h]["hi"].strip()
        # Strip any accidental code fences
        for fence in ("```html", "```xml", "```"):
            if hi_html.startswith(fence):
                hi_html = hi_html[len(fence):].lstrip()
            if hi_html.endswith("```"):
                hi_html = hi_html[:-3].rstrip()

        # Verify hi payload has a <section> opener
        if not re.match(r'<section\b', hi_html):
            print(f"  WARN {rel_path}: hi payload missing <section> for {h}", file=sys.stderr)
            continue

        new_en = _inject_xshow_en(opening_tag) + raw_slice[len(opening_tag):]
        new_hi = _inject_xshow_hi_cloak(hi_html)

        replacement = new_en + "\n\n" + new_hi + "\n"
        text = text[:start] + replacement + text[end:]
        count += 1

    if count > 0:
        path.write_text(text, encoding="utf-8")
    return count


def main() -> int:
    total = 0
    for rel in PAGES:
        n = patch_file(rel)
        print(f"{rel}: patched {n} sections")
        total += n
    print(f"\ntotal sections patched: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
