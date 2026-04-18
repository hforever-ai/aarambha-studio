# Aarambha Studio v1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a five-page Aarambha Studio website (aarambhax.ai) positioning the brand as India's AI Studio, with Shrutam as the flagship product and WhatsApp Commerce AI as the in-development sibling under a Pancha Bhoota narrative frame.

**Architecture:** Multi-page static HTML built on Tailwind CSS v3 CDN + Alpine.js 3 CDN + Google Fonts. No local CSS files, no build tooling, no backend. A single `/assets/js/translations.js` file holds the Alpine `lang` store and EN/हिंदी strings for brand-voice copy. Deploys via GitHub Pages from `main`.

**Tech Stack:** HTML5, Tailwind v3 (CDN runtime), Alpine.js 3.x (CDN), Google Fonts (Sora + Noto Sans Devanagari), Python 3 (for the cache-bust helper), zsh/bash (for the pre-commit hook).

**Spec:** [docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md](../specs/2026-04-17-aarambha-studio-v1-design.md)

---

## File Structure

All paths are relative to repo root (`/Users/ajayagrawal/aarambhax/`, tracked as `hforever-ai/aarambha-studio` on GitHub).

```
CNAME                                         Task 1 — "aarambhax.ai" one line
favicon.svg                                   Task 1 — copied from aarambhax-backup-2026-04-17/
favicon.ico                                   Task 1 — copied from aarambhax-backup-2026-04-17/
robots.txt                                    Task 1
sitemap.xml                                   Task 1 (stub), Task 7 (final)
assets/js/translations.js                     Task 1 — Alpine store + ~20 EN/HI strings
scripts/set_cache_bust.py                     Task 1 — versions translations.js in HTML
scripts/pre-commit.sh                         Task 1 — shell wrapper for the hook
.git/hooks/pre-commit                         Task 1 — symlink to scripts/pre-commit.sh
index.html                                    Task 2 — homepage, 7 sections + waitlist form
about/index.html                              Task 3 — Our Story (timeline + values)
products/index.html                           Task 4 — Shrutam + Commerce + Pancha Bhoota
philosophy/index.html                         Task 5 — 22/7 + Pancha Bhoota deep
blog/index.html                               Task 6 — minimal empty-state
404.html                                      Task 7 — branded 404
```

**File responsibilities:**
- `CNAME` — GitHub Pages reads this to route `aarambhax.ai` to the repo. One line. No trailing content.
- `translations.js` — single source of EN/HI brand-voice copy + Alpine store. Never split. Every page loads this one file.
- `set_cache_bust.py` — single-purpose: regex-rewrite every `<script src="/assets/js/translations.js...">` in every `*.html` under repo root to carry a `?v=<version>` query string. That's it.
- Each HTML page — self-contained: loads Tailwind+Alpine+Fonts from CDN, inlines the nav partial and footer partial verbatim, loads `translations.js`, renders its own unique content.

**Testing approach:** No unit/integration test framework. Verification for each task is:
1. Local HTTP server: `python3 -m http.server 8000` → `curl` each page, expect HTTP 200.
2. Headless Chrome screenshot at 1440×900 and 375×2400 → save to `/tmp/` for user visual review.
3. `grep`-based DOM checks for key class selectors (e.g., `astro-hero`, `paradox-card`) to confirm sections rendered.

---

## Task 1 — Foundation

**Goal:** Scaffold everything that every later page depends on. No page content yet.

**Files:**
- Create: `CNAME`
- Create: `favicon.svg` (copy from backup)
- Create: `favicon.ico` (copy from backup)
- Create: `robots.txt`
- Create: `sitemap.xml` (stub)
- Create: `assets/js/translations.js`
- Create: `scripts/set_cache_bust.py`
- Create: `scripts/pre-commit.sh`
- Link: `.git/hooks/pre-commit` → `../../scripts/pre-commit.sh`

### Steps

- [ ] **Step 1.1: Create `CNAME`**

```
aarambhax.ai
```

One line. No newline tricks — just the domain followed by a single `\n`.

- [ ] **Step 1.2: Copy favicons from the backup**

```bash
cp /Users/ajayagrawal/aarambhax-backup-2026-04-17/favicon.svg   favicon.svg
cp /Users/ajayagrawal/aarambhax-backup-2026-04-17/favicon.ico   favicon.ico
```

Verify the SVG renders the circle-mark and the ICO is ~2KB:
```bash
ls -la favicon.svg favicon.ico
# expect: favicon.svg ~300 bytes, favicon.ico ~2KB
```

- [ ] **Step 1.3: Create `robots.txt`**

```
User-agent: *
Allow: /

Sitemap: https://aarambhax.ai/sitemap.xml
```

- [ ] **Step 1.4: Create `sitemap.xml` (stub — populated fully in Task 7)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://aarambhax.ai/</loc>
    <priority>1.0</priority>
  </url>
</urlset>
```

- [ ] **Step 1.5: Create `assets/js/translations.js`**

```javascript
// AARAMBHA — translations.js
// Alpine store (lang) + brand-voice EN/HI strings.
// Only brand-voice copy toggles; long-form Hinglish stays mixed.

document.addEventListener('alpine:init', () => {
  Alpine.store('lang', {
    current: localStorage.getItem('aarambha_lang') || 'en',
    toggle() {
      this.current = this.current === 'en' ? 'hi' : 'en';
      localStorage.setItem('aarambha_lang', this.current);
    },
    t(key) {
      return (translations[this.current] || translations['en'])[key] || key;
    }
  });
});

const translations = {
  en: {
    // Nav
    nav_products:    "Products",
    nav_about:       "Our Story",
    nav_philosophy:  "Philosophy",
    nav_blog:        "Blog",
    nav_cta:         "Join Shrutam →",
    lang_toggle:     "हिंदी",

    // Hero
    hero_badge:      "🇮🇳 India's AI Studio",
    hero_tagline:    "Where Intelligence Begins",
    hero_sub:        "We build AI for India's 1.4 billion — in their languages, solving their problems. Not translated. Built from the ground up, for Bharat.",
    hero_cta1:       "See Our Products",
    hero_cta2:       "Join Shrutam Waitlist",

    // Manifesto
    manifesto:       "60 crore Indians deserve world-class AI. Not translated. Not watered down. Built FOR them. In their language.",

    // Founder
    founder_badge:   "Our Story",
    founder_quote:   "A small village. A big dream. 22 years building enterprise AI abroad. One message from home changed everything. That question — 'why hasn't any of this reached the villages?' — is Aarambha.",
    founder_cta:     "Read Full Story →",

    // Footer
    footer_tagline:  "Where Intelligence Begins",
    footer_copy:     "© 2026 Aarambha · aarambhax.ai",
    footer_india:    "Building AI for India's 1.4 billion 🇮🇳",
  },

  hi: {
    // Nav
    nav_products:    "उत्पाद",
    nav_about:       "हमारी कहानी",
    nav_philosophy:  "दर्शन",
    nav_blog:        "ब्लॉग",
    nav_cta:         "श्रुतम् जॉइन करें →",
    lang_toggle:     "English",

    // Hero
    hero_badge:      "🇮🇳 भारत का AI स्टूडियो",
    hero_tagline:    "जहाँ बुद्धिमत्ता की आरम्भ होती है",
    hero_sub:        "हम भारत के 1.4 अरब लोगों के लिए AI बना रहे हैं — उनकी भाषा में, उनकी समस्याएँ सुलझाते हुए। अनुवाद नहीं — नए सिरे से।",
    hero_cta1:       "हमारे उत्पाद देखें",
    hero_cta2:       "श्रुतम् वेटलिस्ट जॉइन करें",

    // Manifesto
    manifesto:       "60 करोड़ भारतीय world-class AI के हकदार हैं। अनुवाद नहीं। पतला नहीं। उनके लिए — उनकी भाषा में।",

    // Founder
    founder_badge:   "हमारी कहानी",
    founder_quote:   "एक छोटे से गाँव से निकले थे। बड़ा सपना था। 22 साल विदेश में enterprise AI बनाया। घर से एक message आया और सब बदल गया। वह सवाल — 'यह सब गाँव तक क्यों नहीं पहुँचा?' — वही है आरम्भ।",
    founder_cta:     "पूरी कहानी पढ़ें →",

    // Footer
    footer_tagline:  "जहाँ बुद्धिमत्ता की आरम्भ होती है",
    footer_copy:     "© 2026 आरम्भ · aarambhax.ai",
    footer_india:    "भारत के 1.4 अरब के लिए AI बना रहे हैं 🇮🇳",
  }
};
```

- [ ] **Step 1.6: Create `scripts/set_cache_bust.py`**

```python
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
```

- [ ] **Step 1.7: Create `scripts/pre-commit.sh`**

```bash
#!/usr/bin/env bash
# Pre-commit hook: rewrite cache-bust on translations.js references in HTML
# before every commit so HTML and JS stay in lockstep.

set -e
ROOT="$(git rev-parse --show-toplevel)"
python3 "$ROOT/scripts/set_cache_bust.py"
# Stage any HTML changes the script made so they land in this commit.
git add "$ROOT"/*.html "$ROOT"/*/*.html 2>/dev/null || true
```

Make it executable:
```bash
chmod +x scripts/pre-commit.sh scripts/set_cache_bust.py
```

- [ ] **Step 1.8: Install the pre-commit hook**

```bash
ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
ls -l .git/hooks/pre-commit
# expect: symlink pointing at ../../scripts/pre-commit.sh
```

- [ ] **Step 1.9: Dry-run the bust script (should be a no-op — no HTML yet)**

```bash
python3 scripts/set_cache_bust.py
# expect: "no changes (already v=... or no matches)"
```

- [ ] **Step 1.10: Commit foundation**

```bash
git add CNAME favicon.svg favicon.ico robots.txt sitemap.xml assets/ scripts/
git commit -m "$(cat <<'EOF'
feat: foundation — CNAME, favicons, translations.js, cache-bust pipeline

Scaffolds everything the 5 HTML pages will depend on:

  - CNAME → binds aarambhax.ai to this repo once Pages is enabled
  - favicon.svg + favicon.ico → circle-mark from the previous site,
    copied verbatim from /Users/ajayagrawal/aarambhax-backup-2026-04-17/
  - robots.txt + sitemap.xml stub
  - assets/js/translations.js → Alpine lang store + ~20 brand-voice EN/HI
    strings (nav, hero, manifesto, founder lede, footer). Body Hinglish
    copy on the pages themselves is intentionally unkeyed.
  - scripts/set_cache_bust.py → versions translations.js in every HTML
    <script src> via ?v=<timestamp-hash>. Single-file bust target, no
    CSS @import chain to worry about.
  - scripts/pre-commit.sh → shell wrapper; symlinked into .git/hooks.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expect: one commit created, pre-commit hook runs (prints "no changes yet"), no files skipped.

### Reusable markup — nav + footer (referenced by Tasks 2–7)

The following two blocks MUST be inserted verbatim into every HTML page. The first inside the top of `<body>` (sticky nav), the second just before `</body>` (site footer). They are the same character-for-character on every page. If you need to change them, change them in every file.

**Nav partial:**

```html
<!-- NAV — shared, identical per page -->
<nav x-data="{ open: false }" class="sticky top-0 z-50 bg-dark/90 backdrop-blur-xl border-b border-white/[.07]">
  <div class="max-w-6xl mx-auto px-4 md:px-8 h-[72px] flex items-center justify-between gap-4">
    <a href="/" class="flex items-center gap-2 flex-shrink-0">
      <span class="hindi text-2xl font-black text-accent leading-none">आरम्भ</span>
      <span class="text-xs font-bold text-gray-500 tracking-[.14em] uppercase hidden sm:block">Aarambha</span>
    </a>
    <div class="hidden md:flex items-center gap-0.5">
      <a href="/products/" x-text="$store.lang.t('nav_products')" class="text-sm font-medium text-gray-400 px-3.5 py-2 rounded-xl hover:text-primary hover:bg-primary/10 transition-all"></a>
      <a href="/about/" x-text="$store.lang.t('nav_about')" class="text-sm font-medium text-gray-400 px-3.5 py-2 rounded-xl hover:text-primary hover:bg-primary/10 transition-all"></a>
      <a href="/philosophy/" x-text="$store.lang.t('nav_philosophy')" class="text-sm font-medium text-gray-400 px-3.5 py-2 rounded-xl hover:text-primary hover:bg-primary/10 transition-all"></a>
      <a href="/blog/" x-text="$store.lang.t('nav_blog')" class="text-sm font-medium text-gray-400 px-3.5 py-2 rounded-xl hover:text-primary hover:bg-primary/10 transition-all"></a>
    </div>
    <div class="flex items-center gap-2 flex-shrink-0">
      <button @click="$store.lang.toggle()" x-text="$store.lang.t('lang_toggle')" class="hindi hidden sm:block text-xs font-bold text-gray-400 border border-white/[.12] px-2.5 py-1.5 rounded-lg hover:border-primary/50 hover:text-primary transition-all"></button>
      <a href="/#waitlist" x-text="$store.lang.t('nav_cta')" class="hidden md:inline-flex text-sm font-bold bg-primary text-white px-4 py-2 rounded-xl hover:bg-primary-dark transition-all shadow-lg shadow-primary/20"></a>
      <button @click="open = !open" class="md:hidden p-1.5 text-gray-400" aria-label="Menu">
        <svg x-show="!open" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        <svg x-show="open" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>
  </div>
  <div x-show="open" x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0 -translate-y-2" x-transition:enter-end="opacity-100 translate-y-0" class="md:hidden border-t border-white/[.07] bg-dark px-4 py-4 flex flex-col gap-1">
    <a href="/products/" x-text="$store.lang.t('nav_products')" class="text-gray-300 px-3 py-2.5 rounded-xl hover:bg-white/5 transition-colors"></a>
    <a href="/about/" x-text="$store.lang.t('nav_about')" class="text-gray-300 px-3 py-2.5 rounded-xl hover:bg-white/5 transition-colors"></a>
    <a href="/philosophy/" x-text="$store.lang.t('nav_philosophy')" class="text-gray-300 px-3 py-2.5 rounded-xl hover:bg-white/5 transition-colors"></a>
    <a href="/blog/" x-text="$store.lang.t('nav_blog')" class="text-gray-300 px-3 py-2.5 rounded-xl hover:bg-white/5 transition-colors"></a>
    <div class="border-t border-white/[.07] mt-2 pt-3 flex flex-col gap-2">
      <button @click="$store.lang.toggle()" x-text="$store.lang.t('lang_toggle')" class="hindi text-sm font-bold text-gray-400 border border-white/[.12] px-3 py-2 rounded-xl text-left hover:border-primary/50 transition-all"></button>
      <a href="/#waitlist" x-text="$store.lang.t('nav_cta')" class="bg-primary text-white font-bold text-center px-4 py-3 rounded-xl hover:bg-primary-dark transition-all"></a>
    </div>
  </div>
</nav>
```

**Footer partial:**

```html
<!-- FOOTER — shared, identical per page -->
<footer class="bg-cosmos border-t border-white/[.07] pt-16 pb-8">
  <div class="max-w-6xl mx-auto px-4 md:px-8">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-10 pb-10 border-b border-white/[.07] mb-8">
      <div>
        <div class="text-lg font-bold text-gray-100 mb-2">
          <span class="hindi text-accent">आरम्भ</span>
          <span class="text-gray-500 ml-1 text-sm">Aarambha</span>
        </div>
        <p x-text="$store.lang.t('footer_tagline')" class="text-sm text-gray-500 leading-relaxed mb-1"></p>
        <p x-text="$store.lang.t('footer_india')" class="text-xs text-gray-600"></p>
      </div>
      <div>
        <h4 class="text-xs font-bold uppercase tracking-[.14em] text-gray-500 mb-4">Products</h4>
        <a href="/products/" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors">All Products</a>
        <a href="/products/#shrutam" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors">Shrutam</a>
        <a href="/products/#commerce" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors">WhatsApp Commerce</a>
      </div>
      <div>
        <h4 class="text-xs font-bold uppercase tracking-[.14em] text-gray-500 mb-4">Company</h4>
        <a href="/about/" x-text="$store.lang.t('nav_about')" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors"></a>
        <a href="/philosophy/" x-text="$store.lang.t('nav_philosophy')" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors"></a>
        <a href="/blog/" x-text="$store.lang.t('nav_blog')" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors"></a>
      </div>
      <div>
        <h4 class="text-xs font-bold uppercase tracking-[.14em] text-gray-500 mb-4">Connect</h4>
        <a href="mailto:hello@aarambhax.ai" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors">hello@aarambhax.ai</a>
        <a href="/#waitlist" class="block text-sm text-gray-500 hover:text-primary mb-2.5 transition-colors">Join Waitlist</a>
        <span class="block text-sm text-gray-500 mb-2.5">shrutam.ai <span class="text-gray-700">(soon)</span></span>
      </div>
    </div>
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
      <span x-text="$store.lang.t('footer_copy')" class="text-xs text-gray-600"></span>
      <span class="text-xs text-gray-600">aarambhax.ai · shrutam.ai</span>
    </div>
  </div>
</footer>
```

### Reusable markup — `<head>` block (referenced by Tasks 2–7)

Every page's `<head>` has a shared top. The page-specific part is only `<title>`, `<meta name="description">`, `<meta name="keywords">`, `<link rel="canonical">`, and OG tags — those vary per page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- PAGE-SPECIFIC SEO (Title, description, canonical, OG) — fill per page -->
<title>[page-specific]</title>
<meta name="description" content="[page-specific]">
<link rel="canonical" href="https://aarambhax.ai/[page-path]">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aarambhax.ai/[page-path]">
<meta property="og:title" content="[page-specific]">
<meta property="og:description" content="[page-specific]">
<meta property="og:site_name" content="Aarambha">

<!-- Favicons -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap" rel="stylesheet">

<!-- Tailwind -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: '#0ea5e9',
          'primary-dark': '#0284c7',
          accent: '#f59e0b',
          'accent-dark': '#d97706',
          cosmos: '#020710',
          dark: '#060d1a',
          card: '#0d1525',
        },
        fontFamily: {
          sora: ['Sora', 'sans-serif'],
          hindi: ['Noto Sans Devanagari', 'sans-serif'],
        }
      }
    }
  }
</script>

<!-- Alpine.js -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Shared translations -->
<script src="/assets/js/translations.js"></script>

<!-- Global styles -->
<style>
  html { scroll-behavior: smooth; }
  body { font-family: 'Sora', sans-serif; background: #060d1a; color: #e2e8f0; }
  .hindi { font-family: 'Noto Sans Devanagari', sans-serif; }
  @keyframes twinkle { 0%, 100% { opacity: 0.15; } 50% { opacity: 0.85; } }
  .star { position: absolute; background: white; border-radius: 50%; animation: twinkle var(--d, 3s) ease-in-out infinite; pointer-events: none; }
  .grad { background: linear-gradient(135deg, #0ea5e9, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  /* Selection */
  ::selection { background: #f59e0b; color: #060d1a; }
</style>
</head>
```

---

## Task 2 — Homepage (`index.html`)

**Goal:** Ship the 7-section homepage with the `#waitlist` form target.

**Files:**
- Create: `index.html`

### Steps

- [ ] **Step 2.1: Scaffold `index.html` with head + nav + footer**

Start the file with this exact skeleton. Replace the `<!-- CONTENT -->` marker in Step 2.2.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Aarambha — Where Intelligence Begins | India's AI Studio | aarambhax.ai</title>
<meta name="description" content="Aarambha builds AI for India's 1.4 billion in their languages. First product: Shrutam — AI education for CG Board & CBSE students. aarambhax.ai">
<meta name="keywords" content="Aarambha, aarambhax, India AI studio, Shrutam, AI for Bharat, Hindi AI, rural education AI, WhatsApp commerce AI">
<link rel="canonical" href="https://aarambhax.ai/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aarambhax.ai/">
<meta property="og:title" content="Aarambha — Where Intelligence Begins">
<meta property="og:description" content="India's AI Studio. Building AI for 1.4 billion Indians in their own languages. Not translated. From the ground up.">
<meta property="og:site_name" content="Aarambha">

<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap" rel="stylesheet">

<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = { theme: { extend: {
    colors: { primary: '#0ea5e9', 'primary-dark': '#0284c7', accent: '#f59e0b', 'accent-dark': '#d97706', cosmos: '#020710', dark: '#060d1a', card: '#0d1525' },
    fontFamily: { sora: ['Sora', 'sans-serif'], hindi: ['Noto Sans Devanagari', 'sans-serif'] }
  } } }
</script>

<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<script src="/assets/js/translations.js"></script>

<style>
  html { scroll-behavior: smooth; }
  body { font-family: 'Sora', sans-serif; background: #060d1a; color: #e2e8f0; }
  .hindi { font-family: 'Noto Sans Devanagari', sans-serif; }
  @keyframes twinkle { 0%, 100% { opacity: 0.15; } 50% { opacity: 0.85; } }
  .star { position: absolute; background: white; border-radius: 50%; animation: twinkle var(--d, 3s) ease-in-out infinite; pointer-events: none; }
  .grad { background: linear-gradient(135deg, #0ea5e9, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  ::selection { background: #f59e0b; color: #060d1a; }
</style>
</head>
<body>

<!-- PASTE THE NAV PARTIAL FROM TASK 1 HERE -->

<main>
  <!-- CONTENT (7 sections, filled in Step 2.2) -->
</main>

<!-- PASTE THE FOOTER PARTIAL FROM TASK 1 HERE -->

<!-- Starfield generator (hero background) -->
<script>
  (function () {
    const host = document.getElementById('starfield');
    if (!host) return;
    for (let i = 0; i < 120; i++) {
      const s = document.createElement('div');
      s.className = 'star';
      const size = Math.random() < 0.8 ? 1 : 2;
      s.style.width = s.style.height = size + 'px';
      s.style.top = (Math.random() * 100).toFixed(2) + '%';
      s.style.left = (Math.random() * 100).toFixed(2) + '%';
      s.style.setProperty('--d', (2 + Math.random() * 4).toFixed(2) + 's');
      s.style.animationDelay = (Math.random() * 4).toFixed(2) + 's';
      host.appendChild(s);
    }
  })();
</script>

</body>
</html>
```

- [ ] **Step 2.2: Insert the 7-section main content**

Replace the `<!-- CONTENT (7 sections, filled in Step 2.2) -->` line with:

```html
<!-- 1. HERO -->
<section class="relative bg-cosmos min-h-screen flex items-center justify-center overflow-hidden px-4 md:px-8">
  <div id="starfield" class="absolute inset-0 overflow-hidden pointer-events-none"></div>
  <div class="absolute inset-0 pointer-events-none" style="background:
    radial-gradient(ellipse at 20% 20%, rgba(14,165,233,0.18), transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(245,158,11,0.14), transparent 55%);"></div>
  <div class="relative z-10 max-w-5xl mx-auto text-center py-24">
    <p class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-primary/30 bg-primary/5 text-xs font-semibold text-primary tracking-[.18em] uppercase mb-10"
       x-text="$store.lang.t('hero_badge')"></p>
    <h1 class="hindi text-[6rem] md:text-[10rem] font-black text-accent leading-none mb-4"
        style="text-shadow: 0 0 80px rgba(245,158,11,0.35);">आरम्भ</h1>
    <p class="text-xl md:text-2xl text-gray-400 tracking-wider font-medium mb-6"
       x-text="$store.lang.t('hero_tagline')"></p>
    <p class="text-gray-400 text-lg leading-relaxed max-w-2xl mx-auto mb-10"
       x-text="$store.lang.t('hero_sub')"></p>
    <div class="flex flex-col sm:flex-row items-center justify-center gap-3 mb-12">
      <a href="/products/" class="inline-flex items-center gap-2 bg-accent hover:bg-accent-dark text-gray-900 font-bold px-7 py-3.5 rounded-xl shadow-lg shadow-accent/20 transition-all"
         x-text="$store.lang.t('hero_cta1')"></a>
      <a href="/#waitlist" class="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-7 py-3.5 rounded-xl shadow-lg shadow-primary/20 transition-all"
         x-text="$store.lang.t('hero_cta2')"></a>
    </div>
    <div class="inline-flex flex-wrap items-center justify-center gap-6 md:gap-10 bg-card/60 backdrop-blur-sm border border-white/[.07] rounded-2xl px-6 md:px-10 py-5">
      <div class="text-center"><div class="text-2xl md:text-3xl font-black text-primary leading-none">1.2B+</div><div class="text-[10px] text-gray-500 tracking-[.14em] uppercase mt-1">Indians</div></div>
      <div class="text-center"><div class="text-2xl md:text-3xl font-black text-accent leading-none">2</div><div class="text-[10px] text-gray-500 tracking-[.14em] uppercase mt-1">Products</div></div>
      <div class="text-center"><div class="text-2xl md:text-3xl font-black text-primary leading-none">22+</div><div class="text-[10px] text-gray-500 tracking-[.14em] uppercase mt-1">Years AI</div></div>
      <div class="text-center"><div class="text-2xl md:text-3xl font-black text-accent leading-none">5</div><div class="text-[10px] text-gray-500 tracking-[.14em] uppercase mt-1">Languages</div></div>
    </div>
  </div>
</section>

<!-- 2. MANIFESTO -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-4xl mx-auto text-center">
    <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.18em] uppercase mb-8">Our Mission</p>
    <p class="text-3xl md:text-4xl font-bold leading-relaxed text-gray-100 mb-10"
       x-text="$store.lang.t('manifesto')"></p>
    <div class="flex flex-wrap justify-center gap-2.5">
      <span class="bg-white/5 border border-white/[.10] text-gray-300 rounded-full px-4 py-1.5 text-sm">🇮🇳 India First</span>
      <span class="bg-white/5 border border-white/[.10] text-gray-300 rounded-full px-4 py-1.5 text-sm">🗣️ Bhasha First</span>
      <span class="bg-white/5 border border-white/[.10] text-gray-300 rounded-full px-4 py-1.5 text-sm">🏘️ Bharat First</span>
      <span class="bg-white/5 border border-white/[.10] text-gray-300 rounded-full px-4 py-1.5 text-sm">♿ Accessible First</span>
    </div>
  </div>
</section>

<!-- 3. PROBLEM -->
<section class="bg-cosmos py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-5">The Opportunity</p>
    <h2 class="text-3xl md:text-5xl font-black mb-4">India Ka <span class="grad">AI Paradox</span></h2>
    <p class="text-gray-400 text-lg max-w-2xl mb-14">Three numbers explain the gap — and the opening we're building for.</p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <article class="bg-card border border-white/[.07] rounded-2xl p-8 relative overflow-hidden">
        <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-primary to-accent"></div>
        <div class="text-5xl md:text-6xl font-black text-primary mb-2 leading-none">1.2B+</div>
        <div class="text-gray-300 font-semibold mb-3">Indians without native AI</div>
        <p class="text-sm text-gray-500 leading-relaxed">1.4 billion total. 200 million speak English. 1.2 billion left behind by every AI company building for the West.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-8 relative overflow-hidden">
        <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-primary to-accent"></div>
        <div class="text-5xl md:text-6xl font-black text-accent mb-2 leading-none">68%</div>
        <div class="text-gray-300 font-semibold mb-3">Students rote-learn. Zero understanding.</div>
        <p class="text-sm text-gray-500 leading-relaxed">250M+ school students. Most can't afford a private tutor. The system teaches memorisation, not thinking.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-8 relative overflow-hidden">
        <div class="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-primary to-accent"></div>
        <div class="text-5xl md:text-6xl font-black text-gray-200 mb-2 leading-none">63M</div>
        <div class="text-gray-300 font-semibold mb-3">MSMEs with zero AI commerce tools</div>
        <p class="text-sm text-gray-500 leading-relaxed">WhatsApp + Excel. That's the stack. Aarambha's next product fixes this.</p>
      </article>
    </div>
    <p class="mt-12 text-center hindi text-xl md:text-2xl font-semibold text-accent">हम यहाँ हैं — यह gap मिटाने के लिए।</p>
  </div>
</section>

<!-- 4. PRODUCTS -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <div class="text-center max-w-2xl mx-auto mb-14">
      <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-5">Aarambha Studio</p>
      <h2 class="text-3xl md:text-5xl font-black mb-4">We build <span class="grad">AI products</span>. Not just apps.</h2>
      <p class="text-gray-400 text-lg leading-relaxed">Each solves a real Bharat problem — ignored because it's in a village, in Hindi, or in a market the West won't scale to.</p>
    </div>

    <!-- SHRUTAM FEATURED (full-width, blue glow) -->
    <article class="bg-card border border-primary/30 rounded-2xl p-8 md:p-12 mb-6 shadow-[0_0_40px_rgba(14,165,233,0.1)] relative overflow-hidden">
      <div class="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent opacity-80"></div>
      <div class="grid md:grid-cols-[2fr,1fr] gap-10 items-center">
        <div>
          <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/30 text-xs font-bold text-green-400 uppercase tracking-[.12em] mb-4">🟢 Launching May 20, 2026</p>
          <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🌍 Prithvi — Knowledge is Foundation</p>
          <h3 class="text-2xl md:text-3xl font-black mb-2"><span class="hindi text-accent mr-2">श्रुतम्</span><span class="text-gray-100">SHRUTAM</span></h3>
          <p class="hindi text-primary text-lg mb-5">सुनते हैं, सीखते हैं।</p>
          <p class="text-gray-400 leading-relaxed mb-6">AI-powered audio-first learning for CG Board &amp; CBSE students. SAAVI didi teaches Science &amp; Math in Hinglish — for Class 6–10 students in India's villages. Built around how real Bharat learners actually study: audio over long text, Hinglish over English, privacy over paywall-shame.</p>
          <div class="flex flex-wrap gap-2 mb-6">
            <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">5 Languages</span>
            <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Class 6-10</span>
            <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">₹199/mo</span>
            <span class="bg-accent/10 border border-accent/30 text-accent rounded-full px-3 py-1 text-xs">♿ Blind Mode FREE</span>
          </div>
          <div class="flex flex-wrap gap-3">
            <a href="/products/" class="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-6 py-3 rounded-xl transition-all">Learn more →</a>
            <a href="/#waitlist" class="inline-flex items-center gap-2 border border-white/20 hover:border-primary/50 text-gray-300 hover:text-primary font-semibold px-6 py-3 rounded-xl transition-all">Join Waitlist →</a>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2.5 content-center">
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-sm text-gray-500 mb-1">Class</div><div class="font-bold text-gray-100">6 — 10</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-sm text-gray-500 mb-1">Board</div><div class="font-bold text-gray-100">CG + CBSE</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-sm text-gray-500 mb-1">Price</div><div class="font-bold text-gray-100">₹199/mo</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-sm text-gray-500 mb-1">Blind</div><div class="font-bold text-accent">FREE</div></div>
        </div>
      </div>
    </article>

    <!-- SECONDARY ROW: Commerce + Future -->
    <div class="grid md:grid-cols-2 gap-6">
      <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8">
        <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">🔵 In Development — 2026</p>
        <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🌬️ Vayu — Commerce Flows Like Air</p>
        <h3 class="text-xl font-black text-gray-100 mb-2">WhatsApp Commerce AI</h3>
        <p class="text-primary text-sm mb-4">Kirana se enterprise tak</p>
        <p class="text-gray-400 leading-relaxed text-sm mb-5">AI-powered B2B order management for Indian distributors. WhatsApp se order, AI se catalog matching, smart reorder predictions.</p>
        <a href="/products/#commerce" class="inline-flex items-center gap-2 border border-primary/40 text-primary hover:bg-primary/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Express Interest →</a>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-8">
        <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/30 text-xs font-bold text-accent uppercase tracking-[.12em] mb-4">⚡ Coming Next</p>
        <div class="flex items-center gap-3 mb-3 text-2xl">🔥 💧 ✨</div>
        <h3 class="text-xl font-black text-gray-100 mb-2">Tejas · Jal · Akasha</h3>
        <p class="text-gray-400 leading-relaxed text-sm mb-5">Three more AI products. Five elements. One mission — India's AI future, one product at a time.</p>
        <a href="/philosophy/" class="inline-flex items-center gap-2 border border-accent/40 text-accent hover:bg-accent/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Pancha Bhoota →</a>
      </article>
    </div>
  </div>
</section>

<!-- 5. FOUNDER'S NOTE -->
<section class="bg-cosmos py-24 px-4 md:px-8">
  <div class="max-w-3xl mx-auto">
    <div class="bg-card/60 border border-accent/20 rounded-2xl p-8 md:p-12 text-center relative">
      <span class="absolute -top-3 left-1/2 -translate-x-1/2 bg-cosmos border border-accent/30 text-accent px-4 py-1 rounded-full text-xs font-bold tracking-[.20em] uppercase"
            x-text="$store.lang.t('founder_badge')"></span>
      <p class="hindi italic text-2xl md:text-3xl text-accent leading-relaxed mt-4 mb-6">
        एक गाँव से निकले थे।<br>
        22 साल बाद — एक सवाल आया:<br>
        यह सब गाँव तक क्यों नहीं पहुँचा?<br>
        वही सवाल है आरम्भ।
      </p>
      <p class="text-gray-400 text-base md:text-lg leading-relaxed mb-8"
         x-text="$store.lang.t('founder_quote')"></p>
      <a href="/about/" class="inline-flex items-center gap-2 border border-accent/40 text-accent hover:bg-accent/10 font-semibold px-6 py-3 rounded-xl transition-all"
         x-text="$store.lang.t('founder_cta')"></a>
    </div>
  </div>
</section>

<!-- 6. PHILOSOPHY TEASER -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-center">
    <div>
      <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-4">Philosophy</p>
      <h2 class="text-3xl md:text-4xl font-black mb-4 hindi">22/7 — <span class="text-accent">तेज़ नहीं, सही।</span></h2>
      <p class="text-gray-400 leading-relaxed mb-6">Two woodcutters. One works 24 hours nonstop. The other works 22 — and spends 2 hours sharpening the axe. The second one cuts more wood. That's how we build.</p>
      <div class="flex flex-wrap gap-2 mb-6">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-sm">⏸️ Pause</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-sm">🎯 Optimize</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-sm">🔥 Build Right</span>
      </div>
      <a href="/philosophy/" class="inline-flex items-center gap-2 border border-white/20 hover:border-accent/50 text-gray-300 hover:text-accent font-semibold px-6 py-3 rounded-xl transition-all">Read Our Philosophy →</a>
    </div>
    <div class="bg-card border border-white/[.07] rounded-2xl p-10 text-center">
      <div class="text-6xl mb-4">🪓</div>
      <div class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">The Principle</div>
      <div class="text-4xl font-black grad mb-2">22 + 2</div>
      <div class="text-sm text-gray-400">22 hours of work. 2 hours of sharpening.<br>More wood. Every day.</div>
    </div>
  </div>
</section>

<!-- 7. FINAL CTA + WAITLIST -->
<section id="waitlist" class="bg-cosmos py-24 px-4 md:px-8 relative overflow-hidden">
  <div class="absolute inset-0 pointer-events-none" style="background:
    radial-gradient(ellipse at 50% 40%, rgba(14,165,233,0.18), transparent 55%),
    radial-gradient(ellipse at 50% 80%, rgba(245,158,11,0.10), transparent 50%);"></div>
  <div class="relative z-10 max-w-3xl mx-auto text-center">
    <h2 class="text-3xl md:text-5xl font-black leading-tight mb-2">India ki AI ki aarambh mein</h2>
    <h2 class="text-3xl md:text-5xl font-black leading-tight grad mb-6">shamil ho jaao.</h2>
    <p class="hindi text-gray-400 text-lg md:text-xl mb-10">भारत के लिए AI — साथ बनाएँगे।</p>
    <div class="flex flex-col sm:flex-row justify-center gap-3 mb-10">
      <a href="#waitlist-form" class="inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-6 py-3.5 rounded-xl transition-all">🎓 Join Shrutam Waitlist</a>
      <a href="mailto:hello@aarambhax.ai?subject=Partnership" class="inline-flex items-center justify-center gap-2 bg-accent hover:bg-accent-dark text-gray-900 font-bold px-6 py-3.5 rounded-xl transition-all">🤝 Partner With Us</a>
      <a href="mailto:hello@aarambhax.ai" class="inline-flex items-center justify-center gap-2 border border-white/20 hover:border-primary/50 text-gray-300 hover:text-primary font-semibold px-6 py-3.5 rounded-xl transition-all">📬 hello@aarambhax.ai</a>
    </div>
    <form id="waitlist-form" action="mailto:hello@aarambhax.ai" method="get" enctype="text/plain" class="max-w-md mx-auto flex flex-col sm:flex-row gap-2">
      <input type="hidden" name="subject" value="Shrutam Waitlist — Aarambhax">
      <label for="waitlist-email" class="sr-only">Email</label>
      <input id="waitlist-email" type="email" name="body" required placeholder="your@email.com"
             class="flex-1 min-w-0 px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60 focus:bg-white/[.06] transition-all">
      <button type="submit" class="bg-primary hover:bg-primary-dark text-white font-bold px-5 py-3 rounded-xl transition-all">Stay Updated</button>
    </form>
    <p class="text-xs text-gray-600 mt-3">Submitting opens your email client. No spam. Promise.</p>
  </div>
</section>
```

- [ ] **Step 2.3: Paste nav + footer partials from Task 1**

Open `index.html` and replace:
- `<!-- PASTE THE NAV PARTIAL FROM TASK 1 HERE -->` with the full Nav partial block from Task 1.
- `<!-- PASTE THE FOOTER PARTIAL FROM TASK 1 HERE -->` with the full Footer partial block from Task 1.

Save the file.

- [ ] **Step 2.4: Local smoke test — does the page serve?**

```bash
python3 -m http.server 8000 &
SERVER_PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code} /\n" http://127.0.0.1:8000/
kill $SERVER_PID 2>/dev/null || true
wait 2>/dev/null
```

Expected: `200 /`

- [ ] **Step 2.5: Grep-based DOM check — did all 7 sections render?**

```bash
for marker in 'id="starfield"' 'hero_badge' 'hero_tagline' 'India Ka' 'Aarambha Studio' 'Shrutam' 'Pancha Bhoota|Coming Next|Tejas' 'founder_badge' '22/7' 'id="waitlist"' 'waitlist-form'; do
  count=$(grep -cE "$marker" index.html)
  echo "$count $marker"
done
```

Expected: every count ≥ 1.

- [ ] **Step 2.6: Headless Chrome screenshot @ 1440×900**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
python3 -m http.server 8000 > /tmp/s.log 2>&1 &
SERVER_PID=$!
sleep 1
rm -rf /tmp/chrome-profile
"$CHROME" --headless=new --disable-gpu --no-sandbox --disable-extensions \
  --user-data-dir=/tmp/chrome-profile \
  --window-size=1440,900 \
  --virtual-time-budget=6000 \
  --screenshot=/tmp/home-desktop.png \
  --hide-scrollbars \
  http://127.0.0.1:8000/ > /tmp/c.log 2>&1
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null
ls -lh /tmp/home-desktop.png
```

Expected: PNG file > 80KB. Read the file inline to visually inspect the hero, manifesto, problem cards, product cards, founder block, philosophy teaser, and final CTA.

- [ ] **Step 2.7: Headless Chrome screenshot @ 375×2400 (mobile)**

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 &
SERVER_PID=$!
sleep 1
rm -rf /tmp/chrome-profile-mob
"$CHROME" --headless=new --disable-gpu --no-sandbox --disable-extensions \
  --user-data-dir=/tmp/chrome-profile-mob \
  --window-size=375,2400 \
  --virtual-time-budget=6000 \
  --screenshot=/tmp/home-mobile.png \
  --hide-scrollbars \
  http://127.0.0.1:8000/ > /tmp/c.log 2>&1
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null
ls -lh /tmp/home-mobile.png
```

- [ ] **Step 2.8: Commit homepage**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
feat: homepage — 7-section Aarambha Studio landing

Ships /index.html with the full cinematic homepage:

  1. Hero — cosmos bg + 120 animated stars (JS), massive आरम्भ
     Devanagari wordmark in amber, badge pill, tagline, lede, two
     CTAs, glassmorphism stats pill (1.2B+ / 2 / 22+ / 5)
  2. Manifesto — large quote on "60 crore Indians deserve world-class
     AI" with 4 theme pills
  3. India Ka AI Paradox — 3 dramatic stat cards with gradient top-bar
     (1.2B / 68% / 63M)
  4. Products — Shrutam featured (permanent blue glow, 🌍 Prithvi
     element, Class 6-10 CG+CBSE ₹199 Blind FREE); WhatsApp Commerce
     (🌬️ Vayu, dashed blue); Pancha Bhoota preview (🔥💧✨, dashed amber)
  5. Founder's note — anonymous Hinglish + English quote, CTA to /about/
  6. Philosophy teaser — 22/7 woodcutter, 3 pills, CTA to /philosophy/
  7. Final CTA + waitlist — id="waitlist" anchor with mailto form;
     3 CTA buttons (Join Shrutam / Partner / Email)

Nav + footer partials inlined from the shared markup defined in the
foundation commit. No personal identifying info anywhere per spec.

Pre-commit hook runs set_cache_bust.py; translations.js now carries
?v=<time>-<hash> query on the <script src> so CDN cache stays honest.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md
Plan: docs/superpowers/plans/2026-04-17-aarambha-studio-v1.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expect: pre-commit hook runs, stages the ?v= rewrite, one commit lands.

---

## Task 3 — About page (`about/index.html`)

**Goal:** Ship the Our Story page — cinematic header, 8-beat vertical timeline, 2-column why + 4 values cards.

**Files:**
- Create: `about/index.html`

### Steps

- [ ] **Step 3.1: Scaffold the page**

```bash
mkdir -p about
```

Create `about/index.html` with the same head + nav + footer skeleton from Step 2.1, but swap the SEO block and replace `<main>...</main>` with the body below.

Head SEO:
```html
<title>Our Story — Gaon Se US, Ab Gaon Ke Liye | Aarambha</title>
<meta name="description" content="Aarambha ki kahani. Gaon se enterprise AI tak. 22 saal. Ek sawaal ne sab badal diya: yeh gaon tak kyun nahi pahuncha?">
<link rel="canonical" href="https://aarambhax.ai/about/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aarambhax.ai/about/">
<meta property="og:title" content="Our Story — Aarambha">
<meta property="og:description" content="Gaon se US, ab gaon ke liye. A universal story of 22 years, one question, and the AI studio it became.">
<meta property="og:site_name" content="Aarambha">
```

Main body:
```html
<main>

<!-- 1. CINEMATIC HEADER -->
<section class="bg-cosmos min-h-[60vh] flex items-center justify-center px-4 md:px-8 pt-20 pb-16 relative overflow-hidden">
  <div class="absolute inset-0 pointer-events-none" style="background:
    radial-gradient(ellipse at 30% 30%, rgba(245,158,11,0.12), transparent 55%),
    radial-gradient(ellipse at 70% 70%, rgba(14,165,233,0.10), transparent 55%);"></div>
  <div class="relative z-10 max-w-4xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-8">Our Story</p>
    <h1 class="hindi text-5xl md:text-7xl font-black text-accent leading-tight mb-2">गाँव से US.</h1>
    <h1 class="text-4xl md:text-6xl font-black text-primary leading-tight mb-8">US se Gaon ke liye.</h1>
    <p class="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto">22 saal. Do duniya. Ek sawaal. Ek mission.</p>
  </div>
</section>

<!-- 2. THE JOURNEY — vertical timeline -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-3xl mx-auto">
    <div class="text-center mb-14">
      <h2 class="text-3xl md:text-5xl font-black mb-3 grad">The Journey</h2>
      <p class="text-gray-400">Eight beats. No names. Universal by design.</p>
    </div>
    <ol class="relative border-l-2 border-gradient-to-b border-accent/30 pl-7 md:pl-10 space-y-5">
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">🌱 Start</div>
          <p class="text-gray-300 leading-relaxed">Ek gaon. Ek kamra. Ek sapna — engineer banna.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">🎓 College</div>
          <p class="text-gray-300 leading-relaxed">Pehli generation jo shahar gayi. Engineering complete. Aankhon mein duniya.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">💼 First Job</div>
          <p class="text-gray-300 leading-relaxed">Software engineer. Chhota office. Bada seekhna.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">✈️ Departure</div>
          <p class="text-gray-300 leading-relaxed">Ek call aaya. Bahar jaane ka mauka. Haan bol diya.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">🏢 22 Years</div>
          <p class="text-gray-300 leading-relaxed">Fortune 500 companies. Kafka architectures. Search systems. AI pipelines. Unke liye banaya jinke paas sab tha. Jinke paas nahi tha — unke baare mein koi nahi socha.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">📱 The Message</div>
          <p class="text-gray-300 leading-relaxed">Ek WhatsApp aaya. Ghar se. "Yahan teacher nahi hai. Bacche samajh nahi pa rahe. Koi app nahi jo Hindi mein samjhaye." 22 saal enterprise AI. Ek message.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-accent shadow-[0_0_10px_#f59e0b]"></span>
        <div class="bg-card/50 border border-white/[.07] rounded-xl p-5 md:p-6">
          <div class="text-xs text-accent font-bold uppercase tracking-[.18em] mb-2">💡 The Question</div>
          <p class="text-gray-300 leading-relaxed">"Yeh sab gaon tak kyun nahi pahuncha?" Yeh sawaal — raat bhar nahi sone diya.</p>
        </div>
      </li>
      <li class="relative">
        <span class="absolute -left-[34px] md:-left-[44px] top-4 w-3 h-3 rounded-full bg-primary shadow-[0_0_12px_#0ea5e9]"></span>
        <div class="bg-gradient-to-br from-primary/10 to-accent/5 border border-primary/30 rounded-xl p-5 md:p-6">
          <div class="text-xs text-primary font-bold uppercase tracking-[.18em] mb-2">🌅 Aarambha</div>
          <p class="text-gray-200 leading-relaxed font-medium">India mein AI ki aarambha. Unke liye jo peeche reh gaye — nahi kyunki woh kam the, balki kyunki tools unki bhasha nahi bolte the.</p>
        </div>
      </li>
    </ol>
  </div>
</section>

<!-- 3. WHY AARAMBHA (2-col) -->
<section class="bg-cosmos py-24 px-4 md:px-8">
  <div class="max-w-5xl mx-auto grid md:grid-cols-2 gap-10">
    <div>
      <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-4">The Gap</p>
      <h3 class="text-2xl md:text-3xl font-black mb-4 text-gray-100">Ek paradox.</h3>
      <p class="text-gray-400 leading-relaxed">India mein ek paradox hai. 1.4 billion log. 200 million English speakers. Har AI tool unke liye bana. 1.2 billion? Left behind. Intelligence ki kami nahi — tools ki bhasha galat thi.</p>
    </div>
    <div>
      <p class="inline-block px-3 py-1 rounded-full border border-primary/30 bg-primary/5 text-xs font-bold text-primary tracking-[.18em] uppercase mb-4">The Answer</p>
      <h3 class="text-2xl md:text-3xl font-black mb-4 text-gray-100">Reimagination.</h3>
      <p class="text-gray-400 leading-relaxed">SAAVI didi kabhi nahi bolti: "See the diagram." Woh bolti hai: "Ek circle socho..." Yeh fark hai. Translation nahi — reimagination. Aarambha 1.2 billion ke liye banata hai.</p>
    </div>
  </div>
</section>

<!-- 4. VALUES -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-4">Values</p>
      <h2 class="text-3xl md:text-4xl font-black">How we build.</h2>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <article class="bg-card border border-white/[.07] rounded-2xl p-7">
        <div class="text-3xl mb-3">🎯</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Build for Real India</h3>
        <p class="text-gray-400 text-sm leading-relaxed">Tier 2/3/4, not metro conferences. Villages, Hindi medium, unmetro India.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-7">
        <div class="text-3xl mb-3">🗣️</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Native AI</h3>
        <p class="text-gray-400 text-sm leading-relaxed">Hindi mein sochte hain, translate nahi karte. Hinglish is a feature, not a bug.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-7">
        <div class="text-3xl mb-3">♿</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Include Everyone</h3>
        <p class="text-gray-400 text-sm leading-relaxed">Blind mode, weak readers, rural students. 50 lakh blind students — zero other edtech serves them.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-7">
        <div class="text-3xl mb-3">🔬</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Quality &gt; Speed</h3>
        <p class="text-gray-400 text-sm leading-relaxed">22/7 — ship right, not fast. No feature launches until it's actually good.</p>
      </article>
    </div>
  </div>
</section>

</main>
```

- [ ] **Step 3.2: Paste nav + footer partials from Task 1**

Same as Step 2.3 — inline the full Nav and Footer partials.

- [ ] **Step 3.3: Smoke test**

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 & SERVER_PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code} /about/\n" http://127.0.0.1:8000/about/
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null
```

Expected: `200 /about/`.

- [ ] **Step 3.4: Grep DOM check**

```bash
for marker in 'Our Story' 'गाँव से US' 'The Journey' '🌱 Start' '🏢 22 Years' '💡 The Question' '🌅 Aarambha' 'Values' 'Build for Real India'; do
  count=$(grep -c "$marker" about/index.html)
  echo "$count $marker"
done
```

Expected: every count ≥ 1.

- [ ] **Step 3.5: Screenshot 1440×900 + 375×2800**

Same pattern as Steps 2.6–2.7. URL: `http://127.0.0.1:8000/about/`. Save to `/tmp/about-desktop.png` and `/tmp/about-mobile.png`.

- [ ] **Step 3.6: Commit**

```bash
git add about/index.html
git commit -m "$(cat <<'EOF'
feat: about page — our story, 8-beat timeline, values

Ships /about/index.html with:

  1. Cinematic header — 'गाँव से US. · US se Gaon ke liye.' + subline
  2. The Journey — vertical timeline with 8 anonymised beats:
     Start → College → First Job → Departure → 22 Years →
     The Message → The Question → Aarambha
     Final beat highlighted with sky-blue ring + primary glow.
  3. Why Aarambha — 2-column: The Gap / The Answer
  4. Values — 4 cards: Build for Real India / Native AI /
     Include Everyone / Quality > Speed

No founder name, no employer, no specific village or city — per the
spec's content rules. Story is universal by design.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4 — Products page (`products/index.html`)

**Goal:** Shrutam featured (all 13 features visible), WhatsApp Commerce with interest form, Pancha Bhoota vision cards.

**Files:**
- Create: `products/index.html`

### Steps

- [ ] **Step 4.1: Scaffold the page**

```bash
mkdir -p products
```

Create `products/index.html` with the same head + nav + footer skeleton from Step 2.1, with this SEO:

```html
<title>Products — Shrutam & WhatsApp Commerce AI | Aarambha Studio</title>
<meta name="description" content="Aarambha's AI portfolio: Shrutam (audio-first AI education for CG Board + CBSE) and WhatsApp Commerce AI (kirana to enterprise). Pancha Bhoota — 5 products, 5 elements.">
<link rel="canonical" href="https://aarambhax.ai/products/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aarambhax.ai/products/">
<meta property="og:title" content="Products — Aarambha Studio">
<meta property="og:description" content="Shrutam + WhatsApp Commerce AI. Pancha Bhoota — 5 products, 5 elements, one mission for Bharat.">
<meta property="og:site_name" content="Aarambha">
```

Main body:

```html
<main>

<!-- 1. HEADER -->
<section class="bg-cosmos pt-28 pb-16 px-4 md:px-8">
  <div class="max-w-6xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-6">Aarambha Studio</p>
    <h1 class="text-4xl md:text-6xl font-black mb-4"><span class="grad">5 Products</span> · 5 Elements · 1 Mission</h1>
    <p class="text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">We don't build apps. We build AI that reaches India's villages.</p>
  </div>
</section>

<!-- 2. SHRUTAM FEATURED -->
<section id="shrutam" class="bg-dark py-20 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-primary/30 rounded-2xl p-8 md:p-12 shadow-[0_0_60px_rgba(14,165,233,0.12)] relative overflow-hidden">
      <div class="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent opacity-80"></div>
      <div class="grid md:grid-cols-[2fr,1fr] gap-10 mb-10">
        <div>
          <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/30 text-xs font-bold text-green-400 uppercase tracking-[.12em] mb-4">🟢 Launching May 20, 2026</p>
          <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🌍 Prithvi — Knowledge is Foundation</p>
          <h2 class="text-3xl md:text-5xl font-black mb-3">
            <span class="hindi text-accent mr-2">श्रुतम्</span>
            <span class="text-gray-100">SHRUTAM</span>
          </h2>
          <p class="hindi text-primary text-xl mb-6">सुनते हैं, सीखते हैं।</p>
          <p class="text-gray-300 leading-relaxed mb-6">AI-powered audio-first learning for CG Board &amp; CBSE students. SAAVI didi teaches Science &amp; Math in Hinglish — for Class 6-10 students in India's villages. Audio over long text. Hinglish over English. Privacy over paywall-shame.</p>
          <div class="bg-accent/10 border border-accent/30 rounded-xl p-5 mb-6">
            <p class="text-accent font-bold text-lg mb-1">♿ Blind Mode — India's first. FREE forever.</p>
            <p class="text-gray-400 text-sm">50 lakh visually-impaired students in India. Zero edtech serves them. Shrutam does — no paywall, no limit.</p>
          </div>
          <div class="flex flex-wrap gap-3">
            <a href="/#waitlist" class="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-6 py-3 rounded-xl transition-all">Join Waitlist →</a>
            <a href="mailto:hello@aarambhax.ai?subject=Shrutam%20Info" class="inline-flex items-center gap-2 border border-white/20 hover:border-primary/50 text-gray-300 hover:text-primary font-semibold px-6 py-3 rounded-xl transition-all">Learn More →</a>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2.5 content-center">
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-xs text-gray-500 mb-1">Class</div><div class="font-bold text-gray-100">6 — 10</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-xs text-gray-500 mb-1">Board</div><div class="font-bold text-gray-100">CG + CBSE</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-xs text-gray-500 mb-1">Price</div><div class="font-bold text-gray-100">₹199/mo</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-xs text-gray-500 mb-1">Blind</div><div class="font-bold text-accent">FREE</div></div>
          <div class="col-span-2 bg-white/[.03] border border-white/[.07] rounded-xl p-4 text-center"><div class="text-xs text-gray-500 mb-1">Languages</div><div class="font-bold text-gray-100">Hindi · Hinglish · English · Telugu · Marathi</div></div>
        </div>
      </div>

      <!-- 13 FEATURES GRID -->
      <h3 class="text-xl font-bold text-gray-100 mb-4 pt-6 border-t border-white/[.07]">13 Features. Built for Bharat.</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Mother Tongue Learning</div><div class="text-xs text-gray-500">Apni bhasha mein seekho.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Adaptive Learning</div><div class="text-xs text-gray-500">Tumhari speed par.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Informed Learning</div><div class="text-xs text-gray-500">Syllabus aligned.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Revision Mode</div><div class="text-xs text-gray-500">Exam se pehle — tej.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Ask Like 10</div><div class="text-xs text-gray-500">Doubt clear hone tak.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Zero to Hero</div><div class="text-xs text-gray-500">Shuruaat se — basics.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Photo Doubt Solver</div><div class="text-xs text-gray-500">Textbook ka photo → answer.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Mock Exams (4 levels)</div><div class="text-xs text-gray-500">Easy → Medium → Hard → Exam Ready.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Spoken English</div><div class="text-xs text-gray-500">Zero se interview ready.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Exam Notes</div><div class="text-xs text-gray-500">Short, sharp, tested.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Student Tracking</div><div class="text-xs text-gray-500">Kaunsa topic pending.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Parent Portal</div><div class="text-xs text-gray-500">Progress ka saaf vyaura.</div></div>
        <div class="bg-white/[.03] border border-white/[.07] rounded-lg p-4"><div class="text-sm font-bold text-primary mb-1">Reel Mode</div><div class="text-xs text-gray-500">App · Instagram · YouTube.</div></div>
      </div>
    </article>
  </div>
</section>

<!-- 3. WHATSAPP COMMERCE -->
<section id="commerce" class="bg-cosmos py-20 px-4 md:px-8">
  <div class="max-w-5xl mx-auto">
    <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8 md:p-12">
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">🔵 In Development — 2026</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🌬️ Vayu — Commerce Flows Like Air</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">WhatsApp Commerce AI</h2>
      <p class="text-primary text-lg mb-5">Kirana se enterprise tak.</p>

      <div class="grid md:grid-cols-2 gap-6 mb-8">
        <div>
          <h4 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h4>
          <p class="text-gray-400 leading-relaxed text-sm">63 million MSMEs. WhatsApp + Excel. Zero AI in the stack. Orders get lost, catalogs don't match, reorders miss the window — all because nothing speaks the language of the trade.</p>
        </div>
        <div>
          <h4 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h4>
          <p class="text-gray-400 leading-relaxed text-sm">WhatsApp-native. Hindi voice. 4-layer NLP pipeline. Catalog matching AI. Smart reorder prediction. Meets the trade where it already works.</p>
        </div>
      </div>

      <div class="flex flex-wrap gap-2 mb-6">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-xs">Kirana</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-xs">Pharma</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-xs">FMCG</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3.5 py-1.5 text-xs">B2B Distributors</span>
      </div>

      <!-- Interest form -->
      <form action="mailto:hello@aarambhax.ai" method="get" enctype="text/plain" class="grid md:grid-cols-[1fr,1fr,1fr,auto] gap-2">
        <input type="hidden" name="subject" value="WhatsApp Commerce AI — Interest">
        <input type="text" name="name" required placeholder="Your name" class="px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60">
        <input type="text" name="business" required placeholder="Business type" class="px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60">
        <input type="text" name="body" required placeholder="City" class="px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60">
        <button type="submit" class="bg-primary hover:bg-primary-dark text-white font-bold px-5 py-3 rounded-xl transition-all whitespace-nowrap">Express Interest →</button>
      </form>
      <p class="text-xs text-gray-600 mt-2">Submitting opens your email client with your info prefilled.</p>
    </article>
  </div>
</section>

<!-- 4. PANCHA BHOOTA VISION -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-4">What Comes Next</p>
      <h2 class="text-3xl md:text-5xl font-black mb-3">Pancha Bhoota</h2>
      <p class="text-gray-400 text-lg">Five elements. Five AI products. One mission.</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      <article class="bg-card border border-primary/30 rounded-2xl p-6 text-center">
        <div class="text-4xl mb-3">🌍</div>
        <div class="hindi text-accent text-sm font-bold mb-1">पृथ्वी</div>
        <div class="text-gray-300 font-bold mb-1">Prithvi</div>
        <div class="text-gray-500 text-xs mb-3">Shrutam</div>
        <span class="inline-block text-[10px] bg-green-500/15 text-green-400 border border-green-500/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🟢 Live</span>
      </article>
      <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-6 text-center">
        <div class="text-4xl mb-3">🌬️</div>
        <div class="hindi text-accent text-sm font-bold mb-1">वायु</div>
        <div class="text-gray-300 font-bold mb-1">Vayu</div>
        <div class="text-gray-500 text-xs mb-3">WhatsApp Commerce</div>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🔵 Building</span>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 text-center opacity-90">
        <div class="text-4xl mb-3">🔥</div>
        <div class="hindi text-accent text-sm font-bold mb-1">तेजस्</div>
        <div class="text-gray-300 font-bold mb-1">Tejas</div>
        <div class="text-gray-500 text-xs mb-3">Visual AI</div>
        <span class="inline-block text-[10px] bg-accent/15 text-accent border border-accent/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ Vision</span>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 text-center opacity-90">
        <div class="text-4xl mb-3">💧</div>
        <div class="hindi text-accent text-sm font-bold mb-1">जल</div>
        <div class="text-gray-300 font-bold mb-1">Jal</div>
        <div class="text-gray-500 text-xs mb-3">Healthcare AI</div>
        <span class="inline-block text-[10px] bg-accent/15 text-accent border border-accent/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ Vision</span>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 text-center opacity-90">
        <div class="text-4xl mb-3">✨</div>
        <div class="hindi text-accent text-sm font-bold mb-1">आकाश</div>
        <div class="text-gray-300 font-bold mb-1">Akasha</div>
        <div class="text-gray-500 text-xs mb-3">Infrastructure AI</div>
        <span class="inline-block text-[10px] bg-accent/15 text-accent border border-accent/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ Vision</span>
      </article>
    </div>
  </div>
</section>

</main>
```

- [ ] **Step 4.2: Paste nav + footer partials from Task 1**

Same as Step 2.3.

- [ ] **Step 4.3: Smoke test**

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 & SERVER_PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code} /products/\n" http://127.0.0.1:8000/products/
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null
```

Expected: `200 /products/`.

- [ ] **Step 4.4: Grep DOM check**

```bash
for marker in 'Aarambha Studio' 'Shrutam' 'Blind Mode' 'Mother Tongue' 'Photo Doubt Solver' 'WhatsApp Commerce' 'Kirana' 'Pancha Bhoota' 'Prithvi' 'Vayu' 'Tejas' 'Jal' 'Akasha'; do
  count=$(grep -c "$marker" products/index.html)
  echo "$count $marker"
done
```

Expected: every count ≥ 1.

- [ ] **Step 4.5: Screenshots**

Same pattern as Steps 2.6–2.7. URL: `http://127.0.0.1:8000/products/`. Save to `/tmp/products-desktop.png` and `/tmp/products-mobile.png`.

- [ ] **Step 4.6: Commit**

```bash
git add products/index.html
git commit -m "$(cat <<'EOF'
feat: products page — Shrutam featured, Commerce interest, Pancha Bhoota

Ships /products/index.html:

  1. Header — '5 Products · 5 Elements · 1 Mission'
  2. Shrutam #shrutam — full-width card, permanent blue glow, all 13
     features in a responsive grid (Mother Tongue / Adaptive /
     Informed / Revision / Ask Like 10 / Zero to Hero / Photo Doubt /
     Mock Exams / Spoken English / Exam Notes / Student Tracking /
     Parent Portal / Reel Mode) + ♿ Blind Mode callout (FREE forever)
  3. WhatsApp Commerce #commerce — Vayu element, problem/solution
     two-col, target tags (Kirana/Pharma/FMCG/B2B), 3-field interest
     form that submits via mailto
  4. Pancha Bhoota vision — 5 element cards (Prithvi live / Vayu
     building / Tejas, Jal, Akasha vision) with Devanagari names

All CTAs route to /#waitlist or mailto:hello@aarambhax.ai.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5 — Philosophy page (`philosophy/index.html`)

**Goal:** 22/7 woodcutter story + 3 principle cards + Pancha Bhoota deep (5 large cards) + Bharat First section.

**Files:**
- Create: `philosophy/index.html`

### Steps

- [ ] **Step 5.1: Scaffold the page**

```bash
mkdir -p philosophy
```

Create `philosophy/index.html` with the same head + nav + footer skeleton, SEO:

```html
<title>Philosophy — 22/7 & Pancha Bhoota | Aarambha</title>
<meta name="description" content="22/7: smart work over hard work. Pancha Bhoota: five ancient elements, five AI products for India. Aarambha's philosophy.">
<link rel="canonical" href="https://aarambhax.ai/philosophy/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aarambhax.ai/philosophy/">
<meta property="og:title" content="Philosophy — Aarambha">
<meta property="og:description" content="22/7 — Tez nahi, sahi. Pancha Bhoota — 5 elements, 5 products. Bharat First, not India First.">
<meta property="og:site_name" content="Aarambha">
```

Main body:

```html
<main>

<!-- 1. HEADER -->
<section class="bg-cosmos pt-28 pb-16 px-4 md:px-8">
  <div class="max-w-4xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-6">Philosophy</p>
    <h1 class="hindi text-5xl md:text-7xl font-black text-accent mb-3 leading-tight">तेज़ नहीं, सही।</h1>
    <h1 class="text-3xl md:text-5xl font-black text-primary mb-6">Not Fast. Right.</h1>
    <p class="text-gray-400 text-lg max-w-2xl mx-auto">The thinking behind how we build AI for India.</p>
  </div>
</section>

<!-- 2. 22/7 -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-4xl mx-auto">
    <h2 class="text-3xl md:text-5xl font-black mb-10">22/7 — <span class="grad">The Woodcutter Principle</span></h2>

    <blockquote class="border-l-4 border-accent bg-card/50 rounded-r-2xl italic text-gray-300 p-6 md:p-8 text-lg md:text-xl leading-relaxed mb-12">
      Do lakkadhaare the. Competition tha.<br>
      Pehle ne kaha: 24 ghante kaam karunga. Nonstop.<br>
      Doosre ne kaha: Main 22 ghante kaam karunga. 2 ghante kulhaadi tej karunga.<br>
      <br>
      Din bhar kaam kiya.<br>
      <span class="text-accent font-bold not-italic">22 ghante wale ne zyada lakdi kaati.</span><br>
      <br>
      Kyunki tez kulhaadi — thodi mehnat mein zyada karta hai.
    </blockquote>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-14">
      <article class="bg-card border border-white/[.07] rounded-2xl p-6 hover:border-accent/40 transition-all">
        <div class="text-3xl mb-3">⏸️</div>
        <div class="text-xs text-accent font-bold uppercase tracking-[.14em] mb-2">Pause to Sharpen</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Stop. Reflect. Rebuild.</h3>
        <p class="text-gray-400 text-sm leading-relaxed">No feature ships until it's right. We'd rather delay than ship broken.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-6 hover:border-accent/40 transition-all">
        <div class="text-3xl mb-3">🎯</div>
        <div class="text-xs text-accent font-bold uppercase tracking-[.14em] mb-2">Optimize First</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Don't scale broken things.</h3>
        <p class="text-gray-400 text-sm leading-relaxed">Fix the core until it's perfect, then 10x it. Scale amplifies flaws.</p>
      </article>
      <article class="bg-card border border-white/[.07] rounded-2xl p-6 hover:border-accent/40 transition-all">
        <div class="text-3xl mb-3">🔥</div>
        <div class="text-xs text-accent font-bold uppercase tracking-[.14em] mb-2">Build Right</div>
        <h3 class="text-lg font-bold text-gray-100 mb-2">Ship once, correctly.</h3>
        <p class="text-gray-400 text-sm leading-relaxed">Not ten times, broken. Quality compounds — so does technical debt.</p>
      </article>
    </div>

    <div class="bg-card/60 border border-primary/20 rounded-2xl p-6 md:p-8">
      <p class="text-xs text-primary font-bold uppercase tracking-[.14em] mb-3">Applied to Shrutam</p>
      <p class="text-gray-300 leading-relaxed">Shrutam ki ek ek cheez soch ke bani hai. "Mother tongue first" — ek feature nahi, ek decision tha. Blind mode — 50 lakh students ke liye, revenue zero. Kyunki yahi sahi tha.</p>
    </div>
  </div>
</section>

<!-- 3. PANCHA BHOOTA DEEP -->
<section class="bg-cosmos py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-4">Pancha Bhoota</p>
      <h2 class="text-3xl md:text-5xl font-black mb-4">The Five Elements</h2>
      <p class="text-gray-400 text-lg max-w-2xl mx-auto">Ancient Indian wisdom. Modern AI products.</p>
    </div>

    <blockquote class="max-w-3xl mx-auto text-center italic text-gray-300 text-lg md:text-xl leading-relaxed mb-14">
      "Hinduism mein Pancha Bhoota — 5 elements create the universe. Prithvi, Vayu, Tejas, Jal, Akasha. Aarambha ke 5 products usi philosophy pe bane hain."
    </blockquote>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
      <article class="bg-card border border-primary/30 rounded-2xl p-6 md:p-7">
        <div class="text-5xl mb-4">🌍</div>
        <div class="hindi text-accent text-lg font-bold mb-1">पृथ्वी</div>
        <div class="text-gray-100 text-2xl font-black mb-2">Prithvi</div>
        <div class="text-primary font-bold text-sm mb-3">Shrutam</div>
        <p class="text-gray-400 text-xs leading-relaxed mb-4">Knowledge grounds everything.</p>
        <span class="inline-block text-[10px] bg-green-500/15 text-green-400 border border-green-500/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🟢 May 20</span>
      </article>
      <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-6 md:p-7">
        <div class="text-5xl mb-4">🌬️</div>
        <div class="hindi text-accent text-lg font-bold mb-1">वायु</div>
        <div class="text-gray-100 text-2xl font-black mb-2">Vayu</div>
        <div class="text-primary font-bold text-sm mb-3">WhatsApp Commerce</div>
        <p class="text-gray-400 text-xs leading-relaxed mb-4">Commerce flows everywhere like air.</p>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🔵 2026</span>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 md:p-7 opacity-90">
        <div class="text-5xl mb-4">🔥</div>
        <div class="hindi text-accent text-lg font-bold mb-1">तेजस्</div>
        <div class="text-gray-100 text-2xl font-black mb-2">Tejas</div>
        <div class="text-accent font-bold text-sm mb-3">Visual AI</div>
        <p class="text-gray-400 text-xs leading-relaxed mb-4">Creativity ignited.</p>
        <span class="inline-block text-[10px] bg-accent/15 text-accent border border-accent/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ Vision</span>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 md:p-7 opacity-90">
        <div class="text-5xl mb-4">💧</div>
        <div class="hindi text-accent text-lg font-bold mb-1">जल</div>
        <div class="text-gray-100 text-2xl font-black mb-2">Jal</div>
        <div class="text-accent font-bold text-sm mb-3">Healthcare AI</div>
        <p class="text-gray-400 text-xs leading-relaxed mb-4">Life-giving. Health reaches every village.</p>
        <span class="inline-block text-[10px] bg-accent/15 text-accent border border-accent/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ Vision</span>
      </article>
      <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 md:p-7 opacity-90">
        <div class="text-5xl mb-4">✨</div>
        <div class="hindi text-accent text-lg font-bold mb-1">आकाश</div>
        <div class="text-gray-100 text-2xl font-black mb-2">Akasha</div>
        <div class="text-accent font-bold text-sm mb-3">Infrastructure AI</div>
        <p class="text-gray-400 text-xs leading-relaxed mb-4">The space where everything connects.</p>
        <span class="inline-block text-[10px] bg-accent/15 text-accent border border-accent/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ Vision</span>
      </article>
    </div>

    <p class="text-center hindi text-2xl md:text-3xl font-bold text-accent mt-14">आरम्भ — sab ki aarambh।</p>
  </div>
</section>

<!-- 4. BHARAT FIRST -->
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-4xl mx-auto">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.18em] uppercase mb-4">Positioning</p>
    <h2 class="text-3xl md:text-5xl font-black mb-6">Bharat First — <span class="grad">Not India First.</span></h2>
    <p class="text-gray-400 leading-relaxed text-lg mb-10">
      "India" that gets funded: metro cities, English speakers. "Bharat" that needs AI: villages, Hindi speakers, no tutor, tight budget. Aarambha builds for Bharat.
    </p>
    <ul class="space-y-4">
      <li class="flex items-start gap-4 bg-card/50 border border-white/[.07] rounded-xl p-5">
        <span class="text-2xl flex-shrink-0">🏘️</span>
        <div><div class="text-gray-100 font-bold mb-1">600,000+ villages with internet</div><p class="text-gray-400 text-sm leading-relaxed">Infrastructure is there. Native AI isn't. We close that gap.</p></div>
      </li>
      <li class="flex items-start gap-4 bg-card/50 border border-white/[.07] rounded-xl p-5">
        <span class="text-2xl flex-shrink-0">🗣️</span>
        <div><div class="text-gray-100 font-bold mb-1">5 languages — native, not translated</div><p class="text-gray-400 text-sm leading-relaxed">SAAVI thinks in Hindi. The model wasn't trained on English and retrofitted. That's the difference.</p></div>
      </li>
      <li class="flex items-start gap-4 bg-card/50 border border-white/[.07] rounded-xl p-5">
        <span class="text-2xl flex-shrink-0">♿</span>
        <div><div class="text-gray-100 font-bold mb-1">Blind mode — built in, not bolted on</div><p class="text-gray-400 text-sm leading-relaxed">50 lakh visually-impaired students. Zero other edtech serves them. Shrutam does — free, forever.</p></div>
      </li>
    </ul>
  </div>
</section>

</main>
```

- [ ] **Step 5.2: Paste nav + footer partials**

Same as Step 2.3.

- [ ] **Step 5.3: Smoke test**

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 & SERVER_PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code} /philosophy/\n" http://127.0.0.1:8000/philosophy/
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null
```

Expected: `200 /philosophy/`.

- [ ] **Step 5.4: Grep DOM check**

```bash
for marker in 'तेज़ नहीं' '22/7' 'Woodcutter' 'Pause to Sharpen' 'Pancha Bhoota' 'Prithvi' 'Vayu' 'Tejas' 'Jal' 'Akasha' 'Bharat First' '600,000' 'Blind mode'; do
  count=$(grep -c "$marker" philosophy/index.html)
  echo "$count $marker"
done
```

Expected: every count ≥ 1.

- [ ] **Step 5.5: Screenshots**

Same pattern as before. URL: `http://127.0.0.1:8000/philosophy/`. Save `/tmp/philosophy-desktop.png`, `/tmp/philosophy-mobile.png`.

- [ ] **Step 5.6: Commit**

```bash
git add philosophy/index.html
git commit -m "$(cat <<'EOF'
feat: philosophy page — 22/7, Pancha Bhoota, Bharat First

Ships /philosophy/index.html:

  1. Header — तेज़ नहीं, सही / Not Fast. Right.
  2. 22/7 — The Woodcutter Principle as styled blockquote, 3 principle
     cards (Pause / Optimize / Build Right), 'Applied to Shrutam' callout
  3. Pancha Bhoota deep — 5 large element cards with Devanagari names,
     status pills, philosophy lines, closing आरम्भ — sab ki aarambh
  4. Bharat First — not India First positioning, 3 data-backed points
     (600K villages, 5 native languages, blind mode built-in)

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6 — Blog page (`blog/index.html`)

**Goal:** Minimal empty-state with "Coming soon" + email capture.

**Files:**
- Create: `blog/index.html`

### Steps

- [ ] **Step 6.1: Scaffold the page**

```bash
mkdir -p blog
```

Create `blog/index.html` with the same head + nav + footer skeleton, SEO:

```html
<title>Blog — Seekhte Rahenge | Aarambha</title>
<meta name="description" content="Aarambha's blog — launching with Shrutam (May 20, 2026). Guides on AI for Bharat, Hindi-medium learning, and the long road from gaon to production.">
<link rel="canonical" href="https://aarambhax.ai/blog/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://aarambhax.ai/blog/">
<meta property="og:title" content="Blog — Aarambha">
<meta property="og:description" content="Seekhte Rahenge. Launching with Shrutam.">
<meta property="og:site_name" content="Aarambha">
```

Main body:

```html
<main>

<section class="bg-cosmos min-h-[80vh] flex items-center justify-center px-4 md:px-8 py-24">
  <div class="max-w-2xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-6">Blog</p>
    <h1 class="text-4xl md:text-6xl font-black mb-4"><span class="grad">Seekhte Rahenge.</span></h1>
    <p class="hindi text-xl md:text-2xl text-gray-400 mb-10">सीखते रहेंगे — The Aarambha Blog</p>

    <div class="bg-card/60 border border-white/[.07] rounded-2xl p-8 md:p-10 text-left">
      <p class="text-gray-300 text-lg leading-relaxed mb-6">
        Coming soon — first posts drop with <strong class="text-primary">Shrutam launch (May 20, 2026)</strong>. Expect guides on building AI for Bharat, Hindi-medium learning, the long road from gaon to production.
      </p>
      <p class="text-gray-500 text-sm mb-6">Want to know when? Drop your email — zero spam, only Aarambha updates.</p>
      <form action="mailto:hello@aarambhax.ai" method="get" enctype="text/plain" class="flex flex-col sm:flex-row gap-2">
        <input type="hidden" name="subject" value="Aarambha Blog — Notify Me">
        <input type="email" name="body" required placeholder="your@email.com"
               class="flex-1 min-w-0 px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60">
        <button type="submit" class="bg-primary hover:bg-primary-dark text-white font-bold px-5 py-3 rounded-xl transition-all whitespace-nowrap">Notify Me</button>
      </form>
    </div>
  </div>
</section>

</main>
```

- [ ] **Step 6.2: Paste nav + footer partials**

Same as Step 2.3.

- [ ] **Step 6.3: Smoke test + commit**

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 & SERVER_PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code} /blog/\n" http://127.0.0.1:8000/blog/
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null

git add blog/index.html
git commit -m "$(cat <<'EOF'
feat: blog page — minimal empty-state with notify-me capture

Ships /blog/index.html: 'Seekhte Rahenge.' header, Devanagari subhead,
'first posts drop with Shrutam launch May 20, 2026' message, and a
mailto email capture form. Real posts land in a later milestone.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expected: `200 /blog/`; commit lands.

---

## Task 7 — 404, sitemap finalize, push to remote

**Goal:** Ship the branded 404 page, populate sitemap.xml with all five URLs, push the repo.

**Files:**
- Create: `404.html`
- Modify: `sitemap.xml`

### Steps

- [ ] **Step 7.1: Create `404.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Not Found — Aarambha</title>
<meta name="description" content="Yeh page abhi nahi bana. Par aarambha zaroor ho chuki hai.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap" rel="stylesheet">

<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = { theme: { extend: {
    colors: { primary: '#0ea5e9', 'primary-dark': '#0284c7', accent: '#f59e0b', 'accent-dark': '#d97706', cosmos: '#020710', dark: '#060d1a', card: '#0d1525' },
    fontFamily: { sora: ['Sora', 'sans-serif'], hindi: ['Noto Sans Devanagari', 'sans-serif'] }
  } } }
</script>

<style>
  body { font-family: 'Sora', sans-serif; background: #020710; color: #e2e8f0; }
  .hindi { font-family: 'Noto Sans Devanagari', sans-serif; }
  .grad { background: linear-gradient(135deg, #0ea5e9, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
</style>
</head>
<body class="min-h-screen flex items-center justify-center px-4 md:px-8">

<div class="max-w-xl mx-auto text-center">
  <div class="hindi text-[8rem] md:text-[10rem] font-black text-accent leading-none mb-4" style="text-shadow: 0 0 60px rgba(245,158,11,0.3);">404</div>
  <p class="hindi text-xl md:text-2xl text-gray-300 leading-relaxed mb-2">यह page अभी नहीं बना।</p>
  <p class="text-lg text-gray-500 mb-8 italic">Par aarambha zaroor ho chuki hai.</p>
  <a href="/" class="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-6 py-3 rounded-xl transition-all">← Wapas jaao homepage</a>
</div>

</body>
</html>
```

- [ ] **Step 7.2: Populate `sitemap.xml` with all URLs**

Replace the stub with:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://aarambhax.ai/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://aarambhax.ai/products/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://aarambhax.ai/about/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://aarambhax.ai/philosophy/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://aarambhax.ai/blog/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
```

- [ ] **Step 7.3: All-page smoke test**

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 & SERVER_PID=$!
sleep 1
for p in / /about/ /products/ /philosophy/ /blog/ /404.html /sitemap.xml /robots.txt /assets/js/translations.js; do
  echo "$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000$p) $p"
done
kill $SERVER_PID 2>/dev/null; wait 2>/dev/null
```

Expected: every line shows `200 …`. (404.html will return 200 because we're asking for the file directly; a truly-missing path would 404 — that's also fine behaviour for a static server.)

- [ ] **Step 7.4: Commit 404 + sitemap**

```bash
git add 404.html sitemap.xml
git commit -m "$(cat <<'EOF'
feat: branded 404 + final sitemap

  - 404.html — standalone (no nav/footer), big amber 404, Hindi line
    'यह page अभी नहीं बना' + 'Par aarambha zaroor ho chuki hai',
    button back to /. Self-contained so it renders even when Tailwind
    or translations.js fail to load.
  - sitemap.xml — populated with 5 live URLs (/, /products/, /about/,
    /philosophy/, /blog/) at priority 1.0/0.9/0.9/0.9/0.7.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 7.5: Push to remote**

```bash
git push -u origin main
```

Expected: 7 commits pushed to `origin/main`. If this is the first push and the remote has nothing, `git push -u origin main` succeeds. If the remote was pre-populated with a README or anything, the push will be rejected — in that case, inspect with `git fetch origin && git log origin/main` and reconcile before retrying.

- [ ] **Step 7.6: Enable GitHub Pages + bind domain (manual step by user)**

Instructions the user runs in their browser:

1. Go to `https://github.com/hforever-ai/aarambhax` → **Settings → Pages → remove the `aarambhax.ai` custom domain** (releases the domain from the old repo).
2. Go to `https://github.com/hforever-ai/aarambha-studio` → **Settings → Pages**:
   - **Source:** Deploy from a branch
   - **Branch:** `main` · `/` (root)
   - Save.
3. Still on new repo Pages settings → **Custom domain → enter `aarambhax.ai` → save.** GitHub reads the `CNAME` file and waits for DNS.
4. Wait 5–10 minutes; refresh `https://aarambhax.ai/` and the new homepage should load.

After DNS propagates, verify:
```bash
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" https://aarambhax.ai/
curl -s https://aarambhax.ai/assets/js/translations.js | head -3
```
Expected: `200 https://aarambhax.ai/` and the file header `// AARAMBHA — translations.js`.

---

## Self-Review

Running through the checklist:

**1. Spec coverage**
- Spec §Tech stack → Covered by Task 1 (head block with CDNs + font link) and referenced by each page scaffold.
- Spec §Design tokens → Covered by the inline `tailwind.config` block repeated in every page scaffold.
- Spec §File architecture → Matches File Structure section above exactly.
- Spec §Shared runtime (translations.js, nav, footer, waitlist form) → Task 1 Steps 1.5, nav partial, footer partial + Task 2 Step 2.2 section 7 for the form.
- Spec §Page-by-page (5 pages + 404) → Tasks 2–7.
- Spec §Cache-bust → Task 1 Steps 1.6–1.8 (script + hook).
- Spec §Build sequence (8 commits) → Commit 1 is the spec itself (already landed). Tasks 1–7 map to commits 2–8.
- Spec §Deploy + DNS → Task 7 Step 7.6.
- Spec §Content rules (no names/employers/cities) → Applied throughout copy: founder block on homepage, all 8 timeline beats in /about, founder quote string in translations.js, philosophy/Bharat First section. No specific employer, village, or person named anywhere.
- Spec §Risks → Captured in the spec; plan does not need to re-list.

**2. Placeholder scan** — no TBDs, no "implement later", no "similar to Task N". Every code step has complete pasteable content or explicit paste-from-Task-1 instructions for the nav/footer partials (which are fully defined in Task 1 under "Reusable markup").

**3. Type consistency** — CSS class names match across pages (`.hindi`, `.grad`, `.star`, `.card`, `.cosmos`, `.dark`, `.primary`, `.accent`, `.primary-dark`, `.accent-dark`). Alpine store key `aarambha_lang` used consistently in `translations.js` only (plan never references it in HTML — only the store's `.t()`/`.toggle()` methods are called). Translation keys used in HTML (`hero_badge`, `nav_cta`, etc.) all appear in both `en` and `hi` blocks of `translations.js`.

**4. Spec requirements mapped to tasks** — every spec bullet has a task. No gaps.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-17-aarambha-studio-v1.md`.

Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
