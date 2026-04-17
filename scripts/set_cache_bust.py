#!/usr/bin/env python3
"""
Rewrite /assets/js/translations.js references in every HTML file with
?v=<bust> so the CDN fronting GitHub Pages doesn't serve a stale copy
after we push translation changes.

Dev mode (default):
  v = "<time_ns[-10:]>-<sha256[:8]>"
  — time_ns rotates on every run so every commit gets a unique URL
    even when nothing in translations.js changed (stops an identical
    hash ever sticking to cached stale HTML).

Production / release:
  AARAMBHA_BUST_MODE=content  ->  v = first 12 hex chars of sha256 only.

Run manually:
  python3 scripts/set_cache_bust.py
"""
from __future__ import annotations
import hashlib, os, re, secrets, sys, time
from pathlib import Path

JS_SRC = re.compile(r'src="/assets/js/translations\.js(?:\?v=[^"#]*)?"')


def _webroot() -> Path:
    return Path(__file__).resolve().parent.parent


def _translations_hash(webroot: Path) -> str:
    p = webroot / "assets" / "js" / "translations.js"
    if not p.exists():
        return secrets.token_hex(16)
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _cache_bust_token(webroot: Path) -> str:
    full = _translations_hash(webroot)
    mode = os.environ.get("AARAMBHA_BUST_MODE", "dev").lower().strip()
    if mode in ("content", "release", "prod"):
        return full[:12]
    ns = str(time.time_ns())[-10:]
    return f"{ns}-{full[:8]}"


def main() -> int:
    webroot = _webroot()
    v = _cache_bust_token(webroot)
    replacement = f'src="/assets/js/translations.js?v={v}"'

    html_paths = list(webroot.rglob("*.html"))
    changed = 0
    for path in sorted(html_paths):
        if any(seg in path.parts for seg in (".git", "node_modules")):
            continue
        text = path.read_text(encoding="utf-8")
        new, n = JS_SRC.subn(replacement, text)
        if n and new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(webroot)} ({n}x) -> v={v}")
    if not changed:
        print(f"no changes (already v={v} or no matches)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
