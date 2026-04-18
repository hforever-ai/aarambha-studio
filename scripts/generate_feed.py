#!/usr/bin/env python3
"""Generate /feed.xml (Atom) from content/briefs.yaml."""
from __future__ import annotations
import html as hlib, sys, yaml
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
POSTS = yaml.safe_load((ROOT / "content" / "briefs.yaml").read_text())["posts"]

SITE_URL = "https://aarambhax.ai"


def _to_iso(date_str: str) -> str:
    # briefs use YYYY-MM-DD; Atom wants RFC 3339 timestamps
    dt = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc, hour=9, minute=0)
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2] + ":" + dt.strftime("%z")[-2:]


def main() -> int:
    sorted_posts = sorted(POSTS, key=lambda p: p["published_at"], reverse=True)
    updated = _to_iso(sorted_posts[0]["published_at"]) if sorted_posts else _to_iso("2026-04-17")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-IN">',
        f'  <title>Aarambha Blog — Seekhte Rahenge</title>',
        f'  <subtitle>India\'s AI Studio — building AI for Bharat.</subtitle>',
        f'  <link href="{SITE_URL}/blog/" rel="alternate" type="text/html"/>',
        f'  <link href="{SITE_URL}/feed.xml" rel="self" type="application/atom+xml"/>',
        f'  <id>{SITE_URL}/</id>',
        f'  <updated>{updated}</updated>',
        '  <author>',
        '    <name>Aarambha</name>',
        f'    <email>hello@aarambhax.ai</email>',
        f'    <uri>{SITE_URL}/</uri>',
        '  </author>',
        f'  <rights>© 2026 Aarambha · aarambhax.ai</rights>',
        f'  <icon>{SITE_URL}/favicon.svg</icon>',
        f'  <logo>{SITE_URL}/assets/images/og-default.webp</logo>',
    ]

    for p in sorted_posts:
        slug = p["slug"]
        title_en = hlib.escape(p["title_en"])
        title_hi = hlib.escape(p["title_hi"])
        summary_en = hlib.escape(p["og_description_en"])
        summary_hi = hlib.escape(p["og_description_hi"])
        url = f"{SITE_URL}/blog/{slug}/"
        img = f"{SITE_URL}/assets/images/blog/{slug}-hero.webp"
        pub = _to_iso(p["published_at"])
        vertical = hlib.escape(p["vertical"])
        keywords = p.get("keywords", [])

        lines.append("  <entry>")
        lines.append(f"    <title>{title_en}</title>")
        lines.append(f'    <link href="{url}" rel="alternate" type="text/html"/>')
        lines.append(f"    <id>{url}</id>")
        lines.append(f"    <published>{pub}</published>")
        lines.append(f"    <updated>{pub}</updated>")
        lines.append(f'    <category term="{vertical}"/>')
        for kw in keywords:
            lines.append(f'    <category term="{hlib.escape(kw)}"/>')
        lines.append(
            f"    <summary>{summary_en} — हिंदी में: {summary_hi}</summary>"
        )
        content = (
            f'<p><img src="{img}" alt="{summary_en}"/></p>'
            f"<p><strong>EN:</strong> {summary_en}</p>"
            f'<p><strong>हिंदी:</strong> {summary_hi}</p>'
            f'<p><a href="{url}">Read the full post →</a></p>'
        )
        lines.append(f'    <content type="html">{hlib.escape(content)}</content>')
        lines.append("  </entry>")

    lines.append("</feed>")

    out = ROOT / "feed.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB, {len(sorted_posts)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
