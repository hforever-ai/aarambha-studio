#!/usr/bin/env python3
"""Generate a bilingual blog post (EN + HI + Nano Banana hero) from a brief."""
from __future__ import annotations
import argparse, sys, html, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_client import gen_text, gen_image
from lib_image  import save_as_webp, PRESETS

try:
    import yaml
except ImportError:
    print("pip install pyyaml", file=sys.stderr); sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
BRIEFS = yaml.safe_load((ROOT / "content" / "briefs.yaml").read_text())


# --------- prompt templates ---------
def prompt_en(post: dict, common: dict) -> str:
    bullets = "\n".join(f"  - {b}" for b in post["bullets_en"])
    return f"""You are Aarambha's content writer. Audience: Indian readers thinking about {post['vertical']}.
Voice: {common['brand_voice']}

Topic: {post['title_en']}
Vertical: {post['vertical']}
Key points to cover:
{bullets}

Target length: {common['target_length'][0]}-{common['target_length'][1]} words

Output ONLY the HTML article body (no <!DOCTYPE>, <html>, <head>, or <body> tags). Structure:
- 3-5 <h2> section headings
- <h3> for subsections where helpful
- <p> paragraphs; <ul>/<ol> for lists; one <blockquote> pullquote somewhere in the middle
- 2-3 internal links among: <a href="/products/">our products</a>, <a href="/philosophy/">philosophy</a>, <a href="/about/">our story</a>, and where relevant the specific product anchor (e.g. /products/#{post.get('product','')})
- Start DIRECTLY with the first <h2>. No preamble, no explanation, no markdown fences."""


def prompt_hi(post: dict, common: dict) -> str:
    bullets = "\n".join(f"  - {b}" for b in post["bullets_hi"])
    # The Hindi prompt is deliberately in Hindi. This tells the model to write
    # natively, not translate.
    return f"""आप Aarambha के लिए content लिखते हैं। पाठक: भारतीय जो {post['vertical']} के बारे में सोच रहे हैं।
आवाज़: आत्मविश्वासी founder-tone, गर्मजोशी भरी, data-backed, कभी corporate नहीं। Hinglish ठीक है।
किसी का नाम, company, शहर मत लिखें। "हम" या "Aarambha" लिखें।

विषय: {post['title_hi']}
क्षेत्र: {post['vertical']}
मुख्य बिंदु:
{bullets}

लक्ष्य लंबाई: {common['target_length'][0]}-{common['target_length'][1]} शब्द

केवल HTML article body दें (कोई <!DOCTYPE>, <html>, <head>, <body> नहीं)। संरचना:
- 3-5 <h2> section headings
- जहाँ ज़रूरी हो <h3>
- <p> paragraphs; <ul>/<ol> for lists; बीच में एक <blockquote> pullquote
- 2-3 internal links: <a href="/products/">उत्पाद</a>, <a href="/philosophy/">दर्शन</a>, <a href="/about/">कहानी</a>, और जहाँ उपयुक्त हो विशिष्ट product anchor (जैसे /products/#{post.get('product','')})
- सीधे पहले <h2> से शुरू करें। कोई preamble, explanation, markdown fence नहीं।

महत्वपूर्ण: यह अंग्रेज़ी का अनुवाद नहीं है। यह अपनी आवाज़ में, हिंदी में सोचने वाले पाठक के लिए लिखें। उदाहरण, मुहावरे, rhythm — सब मौलिक रूप से हिंदी।"""


def image_prompt(post: dict, common: dict) -> str:
    return f"{common['image_style']}\n\nSubject: {post['image_prompt']}"


# --------- HTML emitter ---------
def render_post(post: dict, en_body: str, hi_body: str, hero_path: str) -> str:
    slug = post["slug"]
    title_en = html.escape(post["title_en"])
    title_hi = html.escape(post["title_hi"])
    og_en    = html.escape(post["og_description_en"])
    og_hi    = html.escape(post["og_description_hi"])
    pub_date = post["published_at"]
    vertical = post["vertical"]
    canonical = f"https://aarambhax.ai/blog/{slug}/"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{title_en} | Aarambha</title>
<meta name="description" content="{og_en}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en-IN" href="{canonical}">
<link rel="alternate" hreflang="hi-IN" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title_en}">
<meta property="og:description" content="{og_en}">
<meta property="og:image" content="https://aarambhax.ai{hero_path}">
<meta property="og:site_name" content="Aarambha">
<meta property="article:published_time" content="{pub_date}">
<meta property="article:section" content="{vertical}">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap" rel="stylesheet">

<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{ theme: {{ extend: {{
    colors: {{ primary: '#0ea5e9', 'primary-dark': '#0284c7', accent: '#f59e0b', 'accent-dark': '#d97706', cosmos: '#020710', dark: '#060d1a', card: '#0d1525' }},
    fontFamily: {{ sora: ['Sora', 'sans-serif'], hindi: ['Noto Sans Devanagari', 'sans-serif'] }}
  }} }} }}
</script>

<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script src="/assets/js/translations.js"></script>

<style>
  html {{ scroll-behavior: smooth; }}
  body {{ font-family: 'Sora', sans-serif; background: #060d1a; color: #e2e8f0; }}
  .hindi {{ font-family: 'Noto Sans Devanagari', sans-serif; }}
  .grad {{ background: linear-gradient(135deg, #0ea5e9, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
  .prose {{ max-width: 44rem; margin: 0 auto; }}
  .prose h2 {{ font-size: 1.75rem; font-weight: 800; color: #f1f5f9; margin: 2.5rem 0 1rem; letter-spacing: -0.02em; }}
  .prose h3 {{ font-size: 1.25rem; font-weight: 700; color: #cbd5e1; margin: 2rem 0 0.75rem; }}
  .prose p  {{ color: #94a3b8; line-height: 1.8; margin-bottom: 1.1rem; }}
  .prose ul, .prose ol {{ color: #94a3b8; margin: 0 0 1.25rem 1.25rem; line-height: 1.75; }}
  .prose li {{ margin-bottom: 0.5rem; }}
  .prose a  {{ color: #0ea5e9; text-decoration: underline; text-decoration-color: rgba(14,165,233,.4); text-underline-offset: 3px; }}
  .prose a:hover {{ color: #f59e0b; text-decoration-color: rgba(245,158,11,.6); }}
  .prose blockquote {{ border-left: 4px solid #f59e0b; padding: 0.5rem 0 0.5rem 1.25rem; margin: 2rem 0; font-style: italic; color: #f1f5f9; font-size: 1.1rem; }}
  .prose strong {{ color: #e2e8f0; font-weight: 700; }}
  ::selection {{ background: #f59e0b; color: #060d1a; }}
</style>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title_en}",
  "description": "{og_en}",
  "inLanguage": "en-IN",
  "datePublished": "{pub_date}",
  "image": "https://aarambhax.ai{hero_path}",
  "author": {{ "@type": "Organization", "name": "Aarambha", "url": "https://aarambhax.ai/" }},
  "publisher": {{ "@type": "Organization", "name": "Aarambha", "url": "https://aarambhax.ai/" }},
  "mainEntityOfPage": "{canonical}",
  "articleSection": "{vertical}"
}}
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title_hi}",
  "description": "{og_hi}",
  "inLanguage": "hi-IN",
  "datePublished": "{pub_date}",
  "image": "https://aarambhax.ai{hero_path}",
  "author": {{ "@type": "Organization", "name": "Aarambha", "url": "https://aarambhax.ai/" }},
  "publisher": {{ "@type": "Organization", "name": "Aarambha", "url": "https://aarambhax.ai/" }},
  "mainEntityOfPage": "{canonical}",
  "articleSection": "{vertical}"
}}
</script>
</head>
<body>

<!-- NAV: same markup as every other page — copy verbatim from /index.html -->
<!-- NAV_PLACEHOLDER -->

<main>
<article class="px-4 md:px-8 py-12 md:py-20">
  <div class="max-w-4xl mx-auto mb-8">
    <p class="text-xs font-bold text-accent tracking-[.20em] uppercase mb-3">{vertical.upper()}</p>
    <h1 x-show="$store.lang.current === 'en'" lang="en" class="text-3xl md:text-5xl font-black leading-tight text-gray-100 mb-4">{title_en}</h1>
    <h1 x-show="$store.lang.current === 'hi'" lang="hi" class="hindi text-3xl md:text-5xl font-black leading-tight text-gray-100 mb-4">{title_hi}</h1>
    <p class="text-sm text-gray-500 mb-8">
      <span x-show="$store.lang.current === 'en'">Published {pub_date} · Aarambha</span>
      <span x-show="$store.lang.current === 'hi'" class="hindi">प्रकाशित {pub_date} · आरम्भ</span>
    </p>
    <img src="{hero_path}" alt="" class="w-full h-auto aspect-[1200/630] object-cover rounded-2xl border border-white/[.07]" loading="eager" width="1200" height="630">
  </div>

  <div class="prose" x-show="$store.lang.current === 'en'" lang="en">
    {en_body}
  </div>
  <div class="prose hindi" x-show="$store.lang.current === 'hi'" lang="hi">
    {hi_body}
  </div>

  <div class="max-w-4xl mx-auto mt-14 pt-8 border-t border-white/[.07]">
    <a href="/blog/" class="text-sm text-primary hover:text-accent transition-colors">← Back to blog</a>
  </div>
</article>
</main>

<!-- FOOTER: same markup as every other page — copy verbatim from /index.html -->
<!-- FOOTER_PLACEHOLDER -->

</body>
</html>
"""


def inject_nav_footer(html_text: str) -> str:
    """Replace NAV_PLACEHOLDER / FOOTER_PLACEHOLDER with the real partials from /index.html."""
    idx_html = (ROOT / "index.html").read_text(encoding="utf-8")
    nav_match = re.search(r'(<!-- NAV[^>]*?-->.*?</nav>\s*)', idx_html, flags=re.DOTALL)
    foot_match = re.search(r'(<!-- FOOTER[^>]*?-->.*?</footer>\s*)', idx_html, flags=re.DOTALL)
    if not nav_match or not foot_match:
        raise RuntimeError("Could not extract nav/footer from index.html")
    html_text = html_text.replace("<!-- NAV_PLACEHOLDER -->", nav_match.group(1))
    html_text = html_text.replace("<!-- FOOTER_PLACEHOLDER -->", foot_match.group(1))
    return html_text


def clean_body(raw: str) -> str:
    """Strip markdown fences and any preamble Gemini might prepend."""
    t = raw.strip()
    t = re.sub(r'^```(?:html)?\s*', '', t)
    t = re.sub(r'\s*```$', '', t)
    return t.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug",   help="generate just this slug; default: all not-yet-generated")
    ap.add_argument("--all",    action="store_true", help="(re)generate all posts; overwrites existing")
    ap.add_argument("--dry",    action="store_true", help="show planned work, no API calls")
    args = ap.parse_args()

    common = BRIEFS["common"]
    posts  = BRIEFS["posts"]
    if args.slug:
        posts = [p for p in posts if p["slug"] == args.slug]

    blog_dir = ROOT / "blog"
    img_dir  = ROOT / "assets" / "images" / "blog"

    for i, post in enumerate(posts, 1):
        slug = post["slug"]
        post_path = blog_dir / slug / "index.html"
        hero_rel  = f"/assets/images/blog/{slug}-hero.webp"
        hero_abs  = img_dir / f"{slug}-hero.webp"

        if post_path.exists() and not args.all:
            print(f"[{i}/{len(posts)}] {slug} — exists, skipping (use --all to regenerate)")
            continue

        print(f"[{i}/{len(posts)}] {slug} ...")
        if args.dry:
            print("  would call: gen_text(en), gen_text(hi), gen_image")
            continue

        en_body = clean_body(gen_text(prompt_en(post, common), max_tokens=8192, temperature=0.65))
        hi_body = clean_body(gen_text(prompt_hi(post, common), max_tokens=8192, temperature=0.65))
        png     = gen_image(image_prompt(post, common))

        size = save_as_webp(png, hero_abs, **PRESETS["blog-hero"])
        print(f"  hero: {hero_abs.relative_to(ROOT)} ({size // 1024} KB)")

        rendered = render_post(post, en_body, hi_body, hero_rel)
        rendered = inject_nav_footer(rendered)
        post_path.parent.mkdir(parents=True, exist_ok=True)
        post_path.write_text(rendered, encoding="utf-8")
        print(f"  post: {post_path.relative_to(ROOT)} ({post_path.stat().st_size // 1024} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
