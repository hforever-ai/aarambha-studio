#!/usr/bin/env python3
"""
Wrap bare text nodes inside <div class="prose hindi"> in <p> tags.

Bug: Gemini output for Hindi bodies often produces naked paragraphs separated
by blank lines rather than <p>...</p>. The .prose CSS selectors target <p>,
so bare text inherits no line-height/color → unreadable wall of text.

Fix: inside each .prose.hindi container, any block of text that is NOT already
inside a block element (<h1-6>, <p>, <ul>, <ol>, <blockquote>, <table>, etc.)
gets wrapped in <p>.

Idempotent: only wraps bare text that isn't already a child of a block element.
"""
from __future__ import annotations
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent.parent

BLOCK_TAGS = {"h1","h2","h3","h4","h5","h6","p","ul","ol","li","blockquote",
              "table","thead","tbody","tr","td","th","figure","pre","div","hr"}


def wrap_bare_text(container, soup: BeautifulSoup) -> int:
    """Walk direct children; wrap consecutive bare text nodes into <p>."""
    wrapped = 0
    # collect children as list to mutate safely
    children = list(container.children)
    buffer = []

    def flush():
        nonlocal wrapped
        if not buffer:
            return
        # Trim empty strings
        text_parts = [str(b) for b in buffer]
        joined = "".join(text_parts).strip()
        if not joined:
            buffer.clear()
            return
        # Each blank-line-separated block becomes its own <p>
        paragraphs = [p.strip() for p in joined.split("\n\n") if p.strip()]
        # insert before first buffered node
        anchor = buffer[0]
        for p_text in paragraphs:
            new_p = soup.new_tag("p")
            # parse inner fragment so inline <a>, <strong> etc. survive
            frag = BeautifulSoup(p_text, "html.parser")
            for node in list(frag.children):
                new_p.append(node)
            anchor.insert_before(new_p)
            wrapped += 1
        # remove buffered originals
        for node in buffer:
            node.extract()
        buffer.clear()

    for child in children:
        if isinstance(child, NavigableString):
            if child.strip():
                buffer.append(child)
            else:
                # whitespace node — keep in buffer only if we've started buffering text
                if buffer:
                    buffer.append(child)
        else:
            if child.name in BLOCK_TAGS:
                flush()
            else:
                # inline element (<a>, <strong>, <em>, <span>, <br>) — bundle into buffer
                buffer.append(child)
    flush()
    return wrapped


def patch_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    containers = soup.select("div.prose.hindi")
    if not containers:
        return 0
    total = 0
    for c in containers:
        total += wrap_bare_text(c, soup)
    if total > 0:
        # write back with minimal impact — use str(soup). Blog posts are fully
        # machine-generated, so reformatting noise is tolerable here.
        path.write_text(str(soup), encoding="utf-8")
    return total


def main() -> int:
    blog_dir = ROOT / "blog"
    total_paragraphs = 0
    total_files = 0
    for p in sorted(blog_dir.rglob("*.html")):
        if p.name != "index.html" or p.parent == blog_dir:
            continue
        n = patch_file(p)
        if n > 0:
            total_files += 1
            total_paragraphs += n
            print(f"{p.relative_to(ROOT)}: wrapped {n} paragraphs")
    print(f"\ntotal: {total_paragraphs} paragraphs across {total_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
