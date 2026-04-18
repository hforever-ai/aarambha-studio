#!/usr/bin/env python3
"""Fix bilingual lang toggle.

Root cause: Alpine only evaluates directives (x-show, x-text) on elements
inside an `x-data` scope. Blog article content has no enclosing x-data,
so x-show="$store.lang.current === 'hi'" never binds — toggling the store
changes no DOM.

Fix: add `x-data` (empty scope is fine) to <main id="main-content"> so
all directives inside the main content get evaluated. Also keeps FOUC fix
via x-cloak + global CSS rule. Idempotent.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Clean up any earlier broken patches: inline style="display:none" on hi-xshow tags
STYLE_CLEANUP = re.compile(
    r'(<[a-zA-Z][^>]*?x-show="\$store\.lang\.current === \'hi\'"[^>]*?)\s*style="display:none"'
)

# Add x-cloak to hi-xshow tags (idempotent)
XCLOAK_PATTERN = re.compile(
    r'(<[a-zA-Z][^>]*?)(x-show="\$store\.lang\.current === \'hi\'")([^>]*?>)'
)

# Add x-data to <main id="main-content"> so child directives are evaluated
MAIN_PATTERN = re.compile(r'(<main\s+id="main-content"(?![^>]*x-data))')


def patch(text: str) -> dict:
    stats = {'cleanup': 0, 'cloak': 0, 'main': 0, 'css': 0}

    # cleanup stale style
    text, n = STYLE_CLEANUP.subn(r'\1', text)
    stats['cleanup'] = n

    # x-cloak
    def cloak_repl(m):
        full = m.group(0)
        if 'x-cloak' in full:
            return full
        stats['cloak'] += 1
        return m.group(1) + 'x-cloak ' + m.group(2) + m.group(3)
    text = XCLOAK_PATTERN.sub(cloak_repl, text)

    # x-data on main
    def main_repl(m):
        stats['main'] += 1
        return m.group(1) + ' x-data'
    text = MAIN_PATTERN.sub(main_repl, text)

    # global cloak CSS
    if '[x-cloak]' not in text and '</head>' in text:
        marker = '<style id="a11y-cloak">[x-cloak]{display:none!important}</style>'
        text = text.replace('</head>', marker + '\n</head>', 1)
        stats['css'] = 1

    return text, stats


def main() -> int:
    touched = 0
    for p in sorted(ROOT.rglob("*.html")):
        if any(s in p.parts for s in (".git", "node_modules", "docs")):
            continue
        original = p.read_text(encoding="utf-8")
        new_text, stats = patch(original)
        if new_text != original:
            p.write_text(new_text, encoding="utf-8")
            touched += 1
            print(f"{p.relative_to(ROOT)}: {stats}")
    print(f"\ntotal files touched: {touched}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
