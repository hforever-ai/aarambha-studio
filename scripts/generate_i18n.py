#!/usr/bin/env python3
"""
Generate native Hindi versions of each <section> inside <main> for the 5 core
pages. Uses Gemini with brand_voice rules from briefs.yaml. Caches results by
content hash in content/i18n-cache.yaml to avoid re-billing.

Does NOT modify the HTML files. That is apply_i18n.py's job.
"""
from __future__ import annotations
import hashlib, sys, yaml
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_client import gen_text  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / "content" / "i18n-cache.yaml"
BRIEFS = yaml.safe_load((ROOT / "content" / "briefs.yaml").read_text())
BRAND_VOICE = BRIEFS["common"]["brand_voice"]

PAGES = [
    ("index.html",            "homepage"),
    ("about/index.html",      "our story"),
    ("products/index.html",   "products"),
    ("philosophy/index.html", "philosophy"),
    ("contact/index.html",    "contact"),
]


def _hash(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        return yaml.safe_load(CACHE_PATH.read_text()) or {}
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_PATH.write_text(yaml.safe_dump(cache, allow_unicode=True, sort_keys=False, width=120))


def _extract_sections(html_path: Path) -> list[str]:
    """Return outer-HTML strings for each <section> that is a descendant of <main>."""
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main")
    if not main:
        return []
    return [str(s) for s in main.find_all("section", recursive=True)]


def _build_prompt(page_kind: str, section_html: str) -> str:
    return f"""You are translating content for Aarambha — India's AI studio building AI for Bharat's 1.4 billion.

BRAND VOICE (mandatory, applies to BOTH EN and HI versions):
{BRAND_VOICE}

YOUR TASK:
Rewrite the <section> below into NATIVE HINDI (Devanagari). This is NOT a translation — it is a parallel native rewrite that would read naturally to a Hindi speaker who has never seen the English.

CRITICAL OUTPUT RULES:
1. Output ONLY the rewritten <section>...</section> HTML. No prose, no explanations, no markdown fences, no preamble.
2. Preserve the ORIGINAL HTML structure EXACTLY — every tag, class, id, href, src, alt, data-*, x-*, @click, aria-*. Only the text content inside elements changes.
3. Keep all Alpine directives, x-text bindings, x-show conditions, template tags AS-IS (do not translate their expressions).
4. For elements that are already x-text bindings (like `x-text="$store.lang.t('...')"` or `x-text="$store.lang.current"`), leave them empty (no text content) — translations.js handles them.
5. English technical terms/brand names that Hindi speakers recognise natively (AI, WhatsApp, Aadhaar, GST, ITR, UPI, Shrutam, Aarambha, Pancha Bhoota, etc.) STAY in English/transliterated form. Do NOT Sanskritise.
6. Hinglish is GOOD — natural code-switch, not pure Sanskrit Hindi. Write like an educated Indian speaks, not like a 1950s All India Radio bulletin.
7. Any HTML comments stay intact.
8. For <img alt="..."> attributes, translate alt text to Hindi.
9. Add `class="hindi"` (append, don't replace) to the OUTER <section> element and to any h1/h2/h3/h4/p/li/span/blockquote/button text elements — so Noto Sans Devanagari font applies. If class already exists, append "hindi" with a space separator.

Page context: this section is part of the "{page_kind}" page.

ORIGINAL EN SECTION:
{section_html}

OUTPUT (Hindi <section> only, nothing else):"""


def main() -> int:
    cache = _load_cache()
    total_new = 0
    total_cached = 0

    for rel_path, kind in PAGES:
        path = ROOT / rel_path
        if not path.exists():
            print(f"skip (missing): {rel_path}")
            continue
        sections = _extract_sections(path)
        print(f"\n== {rel_path} — {len(sections)} sections")
        for i, en_html in enumerate(sections):
            h = _hash(en_html)
            if h in cache:
                total_cached += 1
                print(f"  [{i+1}/{len(sections)}] cache hit ({h})")
                continue
            print(f"  [{i+1}/{len(sections)}] generating ({h}, {len(en_html)} bytes)...", flush=True)
            prompt = _build_prompt(kind, en_html)
            try:
                hi_html = gen_text(prompt, temperature=0.7, max_tokens=8192)
            except Exception as e:
                print(f"    ERROR: {e}", file=sys.stderr)
                continue
            # strip any accidental fences
            hi_html = hi_html.strip()
            for fence in ("```html", "```xml", "```"):
                if hi_html.startswith(fence):
                    hi_html = hi_html[len(fence):].lstrip()
                if hi_html.endswith("```"):
                    hi_html = hi_html[:-3].rstrip()
            cache[h] = {
                "page": rel_path,
                "en": en_html,
                "hi": hi_html,
            }
            total_new += 1
            _save_cache(cache)  # save incrementally
            print(f"    wrote {len(hi_html)} bytes")

    print(f"\nDONE. new={total_new}, cache_hits={total_cached}, total entries={len(cache)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
