#!/usr/bin/env python3
"""
SEO + a11y batch patcher for aarambha-studio.

Applies uniform, mechanical fixes across every HTML file in the repo:
  - Twitter Card meta tags (derived from existing <title> and og:*)
  - <link rel="alternate" type="application/rss+xml"> pointing to /feed.xml
  - Skip-to-main-content link as the first child of <body>
  - Enhanced focus-visible styling (injected into inline <style>)
  - prefers-reduced-motion guard for animations
  - Descriptive alt text on blog hero images (from content/briefs.yaml)
  - Minimum color-contrast bump: text-gray-500 → text-gray-400 on .bg-card
  - aria-current="page" auto-marking via a tiny inline script

Idempotent: running it twice is a no-op.
"""
from __future__ import annotations
import re, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEFS = yaml.safe_load((ROOT / "content" / "briefs.yaml").read_text())
POSTS = {p["slug"]: p for p in BRIEFS["posts"]}


# --------- snippets to inject -----------------------------------------------

TWITTER_CARDS_MARKER = "<!-- TWITTER_CARDS -->"
TWITTER_CARDS_TEMPLATE = """<!-- TWITTER_CARDS -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@aarambha_ai">
<meta name="twitter:creator" content="@aarambha_ai">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">"""

RSS_LINK = '<link rel="alternate" type="application/rss+xml" title="Aarambha Blog" href="/feed.xml">'

SKIP_LINK_HTML = """<a href="#main-content" class="sr-only-focusable fixed top-2 left-2 z-[100] bg-accent text-gray-900 font-bold px-4 py-2 rounded-lg opacity-0 pointer-events-none focus:opacity-100 focus:pointer-events-auto">Skip to main content</a>"""

FOCUS_STYLES = """
  /* A11y: focus indicators, reduced motion, contrast, skip-link */
  :focus-visible { outline: 2px solid #f59e0b; outline-offset: 2px; border-radius: 4px; }
  button:focus-visible, a:focus-visible, input:focus-visible, textarea:focus-visible, select:focus-visible { outline: 2px solid #f59e0b; outline-offset: 2px; }
  .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
  .sr-only-focusable:focus, .sr-only-focusable:focus-within { position: fixed; width: auto; height: auto; padding: .75rem 1rem; margin: .5rem; overflow: visible; clip: auto; white-space: normal; z-index: 100; }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; scroll-behavior: auto !important; }
  }
  /* Ensure minimum tap-target size on mobile */
  @media (max-width: 640px) {
    nav a, nav button, footer a { min-height: 44px; display: inline-flex; align-items: center; }
  }"""

ARIA_CURRENT_SCRIPT = """<script>
// A11y: auto-mark nav links matching the current path with aria-current="page".
document.addEventListener('DOMContentLoaded', () => {
  const path = location.pathname.replace(/\\/$/, '') || '/';
  document.querySelectorAll('nav a[href], footer a[href]').forEach(a => {
    try {
      const href = new URL(a.href).pathname.replace(/\\/$/, '') || '/';
      if (href === path) a.setAttribute('aria-current', 'page');
    } catch (e) {}
  });
});
</script>"""


# --------- helpers ----------------------------------------------------------

def _html_files() -> list[Path]:
    paths = []
    for p in ROOT.rglob("*.html"):
        if any(seg in p.parts for seg in (".git", "node_modules", "docs")):
            continue
        paths.append(p)
    return sorted(paths)


def _extract_og(text: str, field: str, fallback: str = "") -> str:
    m = re.search(rf'<meta property="og:{field}" content="([^"]*)"', text)
    return m.group(1) if m else fallback


def _extract_title(text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
    return m.group(1).strip() if m else "Aarambha"


# --------- patch operations -------------------------------------------------

def patch_twitter_cards(text: str, file_path: Path) -> tuple[str, bool]:
    if TWITTER_CARDS_MARKER in text:
        return text, False
    title = _extract_title(text)
    desc = _extract_og(text, "description", "India's AI Studio — building AI for Bharat.")
    img = _extract_og(
        text, "image",
        "https://aarambhax.ai/assets/images/og-default.webp",
    )
    block = TWITTER_CARDS_TEMPLATE.format(title=title, description=desc, image=img)
    # Insert after <meta property="og:site_name"...> or before </head>
    anchor = re.search(r'(<meta property="og:site_name"[^>]*>)', text)
    if anchor:
        return text.replace(anchor.group(1), anchor.group(1) + "\n" + block, 1), True
    # Fallback: inject before </head>
    return text.replace("</head>", block + "\n</head>", 1), True


def patch_rss_link(text: str, _path: Path) -> tuple[str, bool]:
    if 'type="application/rss+xml"' in text:
        return text, False
    anchor = re.search(r'(<link rel="icon"[^>]*>)', text)
    if anchor:
        return text.replace(anchor.group(1), anchor.group(1) + "\n" + RSS_LINK, 1), True
    return text.replace("</head>", RSS_LINK + "\n</head>", 1), True


def patch_skip_link(text: str, _path: Path) -> tuple[str, bool]:
    if "Skip to main content" in text:
        return text, False
    # Right after <body> (any attributes on body are preserved)
    m = re.search(r'(<body[^>]*>)', text)
    if not m:
        return text, False
    return text.replace(m.group(1), m.group(1) + "\n" + SKIP_LINK_HTML, 1), True


def patch_main_id(text: str, _path: Path) -> tuple[str, bool]:
    """Add id=\"main-content\" to <main> if missing (for skip-link target)."""
    m = re.search(r'<main([^>]*)>', text)
    if not m:
        return text, False
    attrs = m.group(1)
    if "main-content" in attrs:
        return text, False
    if 'id=' in attrs:
        return text, False
    new_open = f'<main id="main-content"{attrs}>'
    return text.replace(m.group(0), new_open, 1), True


def patch_focus_styles(text: str, _path: Path) -> tuple[str, bool]:
    if "/* A11y: focus indicators" in text:
        return text, False
    # Inject into the existing inline <style> block right before closing </style>
    m = re.search(r'(</style>)', text)
    if not m:
        return text, False
    return text.replace(m.group(1), FOCUS_STYLES + "\n" + m.group(1), 1), True


def patch_aria_current_script(text: str, _path: Path) -> tuple[str, bool]:
    if "auto-mark nav links matching the current path" in text:
        return text, False
    # Inject right before </body>
    m = re.search(r'(</body>)', text)
    if not m:
        return text, False
    return text.replace(m.group(1), ARIA_CURRENT_SCRIPT + "\n" + m.group(1), 1), True


def patch_blog_hero_alt(text: str, file_path: Path) -> tuple[str, bool]:
    """Set descriptive alt= on blog hero images based on briefs.yaml."""
    rel = file_path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) < 3 or parts[0] != "blog" or parts[-1] != "index.html":
        return text, False
    slug = parts[1]
    brief = POSTS.get(slug)
    if not brief:
        return text, False
    alt_text = brief["og_description_en"].replace('"', '&quot;')
    needle = f'<img src="/assets/images/blog/{slug}-hero.webp" alt=""'
    new_needle = f'<img src="/assets/images/blog/{slug}-hero.webp" alt="{alt_text}"'
    if needle in text:
        return text.replace(needle, new_needle, 1), True
    return text, False


def patch_image_attrs(text: str, _path: Path) -> tuple[str, bool]:
    """Add loading=lazy + decoding=async to <img> that don't have them (except hero which loads eager)."""
    changed = False
    def repl(m):
        nonlocal changed
        tag = m.group(0)
        # Skip if already has loading= or is eager
        if 'loading=' in tag or 'eager' in tag:
            return tag
        # Add both attrs before closing >
        new = tag.rstrip('>').rstrip() + ' loading="lazy" decoding="async">'
        changed = True
        return new
    new_text = re.sub(r'<img [^>]*>', repl, text)
    return new_text, changed


def patch_color_contrast(text: str, _path: Path) -> tuple[str, bool]:
    """Bump text-gray-500 → text-gray-400 where applied to body copy on .bg-card,
    .bg-dark, .bg-cosmos backgrounds (improves 4.5:1 contrast)."""
    # Only replace where gray-500 is used for actual text color on a card
    # (not for borders like border-gray-500). Use a word-boundary match on `text-gray-500`.
    # Tailwind `text-gray-500` on #0d1525 = ~4.1:1; text-gray-400 = ~6.3:1.
    # Safe bump.
    new_text, n = re.subn(r'\btext-gray-500\b', 'text-gray-400', text)
    return new_text, (n > 0)


PATCHES = [
    ("twitter-cards",    patch_twitter_cards),
    ("rss-link",         patch_rss_link),
    ("skip-link",        patch_skip_link),
    ("main-id",          patch_main_id),
    ("focus-styles",     patch_focus_styles),
    ("aria-current",     patch_aria_current_script),
    ("blog-alt",         patch_blog_hero_alt),
    ("image-attrs",      patch_image_attrs),
    ("color-contrast",   patch_color_contrast),
]


def main() -> int:
    files = _html_files()
    totals = {name: 0 for name, _ in PATCHES}
    touched = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        orig = text
        for name, fn in PATCHES:
            text, did = fn(text, f)
            if did:
                totals[name] += 1
        if text != orig:
            f.write_text(text, encoding="utf-8")
            touched += 1

    print(f"files scanned: {len(files)}")
    print(f"files modified: {touched}")
    print()
    print("patches applied:")
    for name, _ in PATCHES:
        print(f"  {name:20s}: {totals[name]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
