#!/usr/bin/env python3
"""
Inject the GA4 Google tag into every HTML page's <head>.

Idempotent: uses marker comments so re-runs don't duplicate the snippet.
Safe: injects `anonymize_ip: true` to minimise PII exposure.

Run after adding new pages to keep GA coverage complete.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GA_ID = "G-YXJ32LD3H6"

MARKER_BEGIN = "<!-- GA4_BEGIN -->"
MARKER_END   = "<!-- GA4_END -->"

GA_SNIPPET = f"""{MARKER_BEGIN}
<!-- Google tag (gtag.js) — Aarambha GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}', {{ 'anonymize_ip': true }});
</script>
{MARKER_END}"""


def patch_file(path: Path) -> str:
    """Return status string. Inserts GA snippet right before </head>."""
    text = path.read_text(encoding="utf-8")
    if MARKER_BEGIN in text:
        return "skip (already patched)"
    if "</head>" not in text:
        return "skip (no </head>)"
    new_text = text.replace("</head>", GA_SNIPPET + "\n</head>", 1)
    path.write_text(new_text, encoding="utf-8")
    return "patched"


def main() -> int:
    touched = 0
    for p in sorted(ROOT.rglob("*.html")):
        if any(s in p.parts for s in (".git", "node_modules", "docs")):
            continue
        status = patch_file(p)
        if status == "patched":
            touched += 1
            print(f"  {p.relative_to(ROOT)}: {status}")
    print(f"\nGA4 tag injected into {touched} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
