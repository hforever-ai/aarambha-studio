#!/usr/bin/env python3
"""
Improve blog post legibility:
  - Bump body paragraph color from slate-400 to slate-300 (cleaner read on dark bg)
  - Increase prose font-size
  - Give Hindi its own larger size (Devanagari conjuncts need more baseline room)
  - Relax line-height for Hindi prose specifically
  - Add a subtle serif'ish feel with tighter tracking on body

Idempotent: looks for the existing CSS block and rewrites it entirely, delimited
by a sentinel comment.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NEW_PROSE_CSS = """  html { scroll-behavior: smooth; }
  body { font-family: 'Sora', sans-serif; background: #0a1121; color: #e8eef7; }
  .hindi { font-family: 'Noto Sans Devanagari', sans-serif; }
  .grad { background: linear-gradient(135deg, #0ea5e9, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  .prose { max-width: 44rem; margin: 0 auto; font-size: 1.0625rem; }
  .prose h2 { font-size: 1.5rem; font-weight: 800; color: #f8fafc; margin: 2.75rem 0 1rem; letter-spacing: -0.015em; line-height: 1.3; }
  .prose h3 { font-size: 1.1875rem; font-weight: 700; color: #e2e8f0; margin: 2rem 0 0.75rem; line-height: 1.4; }
  .prose p  { color: #d2dbe7; line-height: 1.75; margin-bottom: 1.15rem; }
  .prose ul, .prose ol { color: #d2dbe7; margin: 0 0 1.25rem 1.25rem; line-height: 1.7; }
  .prose li { margin-bottom: 0.5rem; }
  .prose a  { color: #38bdf8; text-decoration: underline; text-decoration-color: rgba(56,189,248,.45); text-underline-offset: 3px; }
  .prose a:hover { color: #fbbf24; text-decoration-color: rgba(251,191,36,.7); }
  .prose blockquote { border-left: 4px solid #f59e0b; padding: 0.75rem 0 0.75rem 1.4rem; margin: 2.25rem 0; font-style: italic; color: #f8fafc; font-size: 1.25rem; line-height: 1.6; }
  .prose strong { color: #f1f5f9; font-weight: 700; }
  /* Hindi-specific tuning: Devanagari needs more vertical breathing room and
     a slightly larger base size for conjunct legibility. */
  .prose.hindi { font-size: 1.125rem; }
  .prose.hindi p,
  .prose.hindi li { line-height: 2.0; color: #dbe3ee; }
  .prose.hindi h2 { line-height: 1.4; }
  .prose.hindi h3 { line-height: 1.5; }
  .prose.hindi blockquote { line-height: 1.8; }
  ::selection { background: #f59e0b; color: #060d1a; }"""

# Match the current <style>...</style> content block we want to replace.
# We target the whitespace + rules between the `html { scroll-behavior` line and
# the `::selection` line, inclusive.
PATTERN = re.compile(
    r'  html \{ scroll-behavior: smooth; \}.*?::selection \{ background: #f59e0b; color: #060d1a; \}',
    re.DOTALL
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = PATTERN.subn(NEW_PROSE_CSS, text, count=1)
    if n == 0:
        return False
    # Skip if already matches the new content exactly
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    blog_dir = ROOT / "blog"
    count = 0
    for p in sorted(blog_dir.rglob("*.html")):
        if p.name != "index.html" or p.parent == blog_dir:
            continue
        if patch_file(p):
            count += 1
            print(f"updated {p.relative_to(ROOT)}")
    print(f"\ntotal posts updated: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
