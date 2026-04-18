#!/usr/bin/env python3
"""
Inject schema.org BreadcrumbList JSON-LD into every non-homepage HTML.

Breadcrumb shape:
  /about/                     Home › About
  /products/                  Home › Products
  /philosophy/                Home › Philosophy
  /blog/                      Home › Blog
  /contact/                   Home › Contact
  /blog/<slug>/               Home › Blog › <Post Title>
  /404.html                   (skipped — 404 has no breadcrumb)

Idempotent.
"""
from __future__ import annotations
import re, sys, yaml, html as hlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = {p["slug"]: p for p in yaml.safe_load((ROOT / "content" / "briefs.yaml").read_text())["posts"]}

MARKER_BEGIN = "<!-- BREADCRUMB_SCHEMA_BEGIN -->"
MARKER_END   = "<!-- BREADCRUMB_SCHEMA_END -->"


def _breadcrumb_json(items: list[tuple[str, str]]) -> str:
    elements = []
    for i, (name, url) in enumerate(items, 1):
        elements.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url,
        })
    obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements,
    }
    import json
    return json.dumps(obj, ensure_ascii=False, indent=2)


def _crumbs_for(path: Path) -> list[tuple[str, str]] | None:
    """Return breadcrumbs for the given HTML file, or None to skip."""
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if parts == ("index.html",):
        return None  # homepage
    if parts == ("404.html",):
        return None  # no crumbs on 404

    home = ("Home", "https://aarambhax.ai/")

    if len(parts) == 2 and parts[1] == "index.html":
        # /<section>/
        section = parts[0]
        label = {
            "about":      "Our Story",
            "products":   "Products",
            "philosophy": "Philosophy",
            "blog":       "Blog",
            "contact":    "Contact",
        }.get(section, section.capitalize())
        return [home, (label, f"https://aarambhax.ai/{section}/")]

    if len(parts) == 3 and parts[0] == "blog" and parts[2] == "index.html":
        slug = parts[1]
        post = POSTS.get(slug)
        title = post["title_en"] if post else slug.replace("-", " ").title()
        return [
            home,
            ("Blog", "https://aarambhax.ai/blog/"),
            (title, f"https://aarambhax.ai/blog/{slug}/"),
        ]

    return None


def patch_file(path: Path) -> bool:
    crumbs = _crumbs_for(path)
    if not crumbs:
        return False
    text = path.read_text(encoding="utf-8")
    # Idempotent: if already has our marker, skip
    if MARKER_BEGIN in text:
        return False
    block = (
        f"\n{MARKER_BEGIN}\n"
        '<script type="application/ld+json">\n'
        + _breadcrumb_json(crumbs)
        + f"\n</script>\n{MARKER_END}\n"
    )
    # Inject right before </head>
    if "</head>" not in text:
        return False
    new_text = text.replace("</head>", block + "</head>", 1)
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    count = 0
    for p in sorted(ROOT.rglob("*.html")):
        if any(s in p.parts for s in (".git", "node_modules", "docs")):
            continue
        if patch_file(p):
            count += 1
            print(f"patched: {p.relative_to(ROOT)}")
    print(f"\nbreadcrumb schemas added: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
