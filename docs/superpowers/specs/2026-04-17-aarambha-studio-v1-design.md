# Aarambha Studio — v1 website design spec

**Date:** 2026-04-17
**Repo:** [github.com/hforever-ai/aarambha-studio](https://github.com/hforever-ai/aarambha-studio) · deploys to `aarambhax.ai` via GitHub Pages
**Author:** Claude + ajayagrawal
**Status:** Approved — execution pending

## Goal

Ship a five-page Aarambha Studio website that positions Aarambha as India's AI Studio (parent brand) — not a single product marketing page. Premium, mission-driven, dark cinematic aesthetic with Indian warmth. Launches with Shrutam as the active product and WhatsApp Commerce AI as the in-development sibling, under a Pancha Bhoota (five-elements) narrative frame.

## Scope

**In scope**
- 5 pages: `/`, `/about/`, `/products/`, `/philosophy/`, `/blog/`
- `404.html` (branded)
- Shared Alpine.js `lang` store + EN/हिंदी toggle on every page
- Cache-bust pipeline for `/assets/js/translations.js`
- Favicons, `CNAME`, `sitemap.xml`, `robots.txt`
- Fresh GitHub repo (`aarambha-studio`) on `hforever-ai`

**Out of scope (v1)**
- CMS or build tooling (vanilla HTML, CDN Tailwind, CDN Alpine)
- Backend / real form submission (waitlist form uses `mailto:` fallback)
- Legacy SEO preservation (old `/saavi/`, `/shrutam/`, `/faq/`, `/contact/`, `/schools/`, `/waitlist/`, `/terms/`, `/privacy/`, `/404.html`, 3 blog posts from the previous `aarambhax` repo — they disappear when the custom domain switches. User explicitly chose "fresh start" deploy path.)
- Deep Hindi translation of every paragraph — only the brand-voice strings (nav, hero, manifesto, founder lead, footer) get EN/HI twins. Long-form Hinglish copy stays mixed (reads the same in both modes).
- Real Shrutam app links — `shrutam.ai` is not running yet, so all "Join Shrutam" CTAs point at an in-page `#waitlist` anchor on the homepage.

**Success criteria**
- Every page loads under 80KB of HTML + one 200-line JS file, zero local CSS.
- Language toggle persists in `localStorage` and updates the ~20 tracked strings site-wide without a page reload.
- Every page shares identical nav + footer markup (copy-paste, no templating).
- `aarambhax.ai/` serves the new homepage after the DNS binding moves from the old repo to the new one.
- No personally-identifying content anywhere: no founder name, no previous employer names, no specific village or city.

## Tech stack

Exactly as specified by the user brief:

| Layer | Choice | Why |
|---|---|---|
| CSS | Tailwind v3 CDN (`cdn.tailwindcss.com`) | Zero build step; matches the spec; config object inline extends with `primary` / `accent` / `cosmos` / `dark` / `card` colors + `sora` / `hindi` font families |
| Reactivity | Alpine.js 3.x (`cdn.jsdelivr.net`) | Lightweight; only used for lang store + mobile menu toggle + hamburger |
| Fonts | Google Fonts — Sora (weights 300/400/600/700/800) + Noto Sans Devanagari (400/600/700/800) | Preconnect + `display=swap` in every `<head>` |
| Hosting | GitHub Pages from `main` branch, root folder | No Actions needed; Pages serves static HTML directly |
| i18n | `/assets/js/translations.js` with Alpine store | ~20 keys; `localStorage.aarambha_lang` persistence |

**Consequence:** Tailwind's CDN runtime compiles utility classes in the browser. It's slower than a prebuilt CSS bundle but acceptable for a 5-page marketing site. If performance becomes a concern, we can precompile later — not now.

## Brand + design tokens

### Color palette
```
primary:      #0ea5e9   (sky blue — CTAs, glows, highlights)
primary-dark: #0284c7   (hover state)
accent:       #f59e0b   (amber — Devanagari moments, editorial accents)
accent-dark:  #d97706
cosmos:       #020710   (deepest bg — hero, footer)
dark:         #060d1a   (default dark bg — body)
card:         #0d1525   (elevated surfaces — product cards, stats)
```

### Type
```
Display + body: Sora (weights 300/400/600/700/800)
Devanagari:     Noto Sans Devanagari (weights 400/600/700/800)
```
Hero `आरम्भ` renders at `clamp(6rem, 10vw, 10rem)` with `text-shadow: 0 0 80px rgba(245,158,11,0.3)`. No other text is that large.

### Layout primitives
- Page content: `max-w-6xl mx-auto px-4 md:px-8` (≈1152px max, 16→32px gutters)
- Hero: `min-h-screen` with radial-gradient cosmos backdrop + generated starfield
- Section rhythm: `py-24` desktop, `py-16` mobile (Tailwind responsive)
- Rounded: cards `rounded-2xl`, buttons `rounded-xl`, pills `rounded-full`

## File architecture

```
aarambha-studio/                 ← repo root, GitHub Pages root
├── CNAME                        ← "aarambhax.ai" (plain text, LF only, no trailing content)
├── index.html                   ← homepage, 7 sections + #waitlist anchor form
├── about/index.html             ← Our Story — cinematic header + 8-beat timeline + values
├── products/index.html          ← Shrutam featured + WhatsApp Commerce (#commerce) + Pancha Bhoota preview
├── philosophy/index.html        ← 22/7 woodcutter + Pancha Bhoota deep + Bharat First
├── blog/index.html              ← minimal empty-state
├── 404.html                     ← branded, small, centered
├── sitemap.xml
├── robots.txt
├── favicon.svg                  ← copied from aarambhax-backup (circle-mark SVG)
├── favicon.ico                  ← copied from aarambhax-backup
├── assets/js/
│   └── translations.js          ← Alpine store + EN/HI strings (~20 keys)
├── docs/superpowers/specs/
│   └── 2026-04-17-aarambha-studio-v1-design.md     ← this spec
└── scripts/
    ├── set_cache_bust.py        ← versions /assets/js/translations.js in every HTML <script src>
    └── pre-commit.sh            ← hook wrapper that runs the bust script
```

**Explicitly NOT present:**
- `/assets/css/` — Tailwind comes from CDN; any extra styles live in per-page `<style>` blocks inside `<head>`.
- `/assets/images/` — the spec says "no images if possible — use CSS/emoji." Favicons are the exception and live at root.
- `/blog/<post-slug>/` — blog is empty-state only in v1. Posts come later.

## Shared runtime

### `/assets/js/translations.js`
```
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

const translations = { en: { /* ~20 keys */ }, hi: { /* same keys */ } };
```

Keys covered: `nav_products`, `nav_about`, `nav_philosophy`, `nav_blog`, `nav_cta`, `lang_toggle`, `hero_badge`, `hero_tagline`, `hero_sub`, `hero_cta1`, `hero_cta2`, `manifesto`, `founder_badge`, `founder_quote`, `founder_cta`, `footer_tagline`, `footer_copy`, `footer_india`.

Body sentences outside this key set stay in their original Hinglish/English and don't toggle. This is intentional — prevents the "half-translated card" mess.

### Nav (identical across every page)
Sticky header, `bg-dark/90 backdrop-blur-xl`, logo left, center links, right cluster with EN/हिंदी toggle + "Join Shrutam →" CTA (scrolls to `/#waitlist`). Hamburger below `md:` breakpoint opens a fullscreen Alpine-driven overlay.

### Footer (identical across every page)
4-column grid: Brand + tagline / Products / Company / Connect. Email `hello@aarambhax.ai`. Domain-row at the bottom reads `aarambhax.ai · shrutam.ai` as display text.

### Waitlist form
Lives on `index.html` Section 7 (`id="waitlist"`). Email input + button. Submission is `mailto:hello@aarambhax.ai?subject=Shrutam%20Waitlist&body=<email>`. CTA convention: **always use absolute `/#waitlist`** — works from every page (jumps home + scrolls to anchor) and avoids the homepage-vs-subpage branching that `#waitlist` alone would need. `html { scroll-behavior: smooth }` makes the in-page jump glide.

## Page-by-page content

### 1. `/index.html` — Homepage

Seven sections, in order:

1. **Hero** — `bg-cosmos min-h-screen`. Center-aligned frame with: badge pill (`🇮🇳 India's AI Studio`), massive `आरम्भ` Devanagari in amber, tagline, body lede, 2 CTAs (See Products / Join Shrutam), glassmorphism stats pill (1.2B+ / 2 / 22+ / 5). JS generates 120 twinkling stars on load.

2. **Manifesto** — `bg-dark`, text-center, large 4-line quote (`60 crore Indians deserve world-class AI...`). Key words `60 crore` in amber, `world-class AI` in primary. 4 theme pills below: India First / Bhasha First / Bharat First / Accessible First.

3. **Problem** — `bg-cosmos`. Eyebrow "The Opportunity" + h2 "India Ka AI Paradox". 3 cards with gradient top-bar: `1.2B+` Indians without native AI · `68%` students rote-learn · `63M` MSMEs without AI commerce. Amber line: "Hum yahan hain — yeh gap mitane ke liye."

4. **Products** — `bg-dark`. Eyebrow "Aarambha Studio" + h2 "We Build AI. Not Just Apps."
   - **Shrutam** (full-width, permanent sky-blue glow): `🟢 Launching May 20, 2026`, `🌍 PRITHVI — Knowledge is Foundation`, Hindi `श्रुतम्` + English `SHRUTAM`, tagline `सुनते हैं, सीखते हैं।`, description, 4 pills, 2 CTAs (shrutam.ai display-text + `/#waitlist`)
   - **WhatsApp Commerce** (half-width, dashed blue): `🔵 In Development — 2026`, `🌬️ VAYU — Commerce Flows Like Air`, tagline `Kirana se enterprise tak`, brief description, "Express Interest" CTA
   - **Future** (half-width, dashed amber): `🔥 TEJAS 💧 JAL ✨ AKASHA` — "Three more AI products. Five elements. One mission."

5. **Founder's note** — `bg-card`, centered, amber-bordered. Badge "Our Story". Hindi italic quote first (from spec), English version below, CTA "Read Full Story →" → `/about/`. No name, no employer, no city.

6. **Philosophy teaser** — `bg-cosmos`, 2-col (md:). Left: "22/7 — Tez Nahi, Sahi" + 3-line story + 3 pills (⏸️ Pause / 🎯 Optimize / 🔥 Build Right). Right: simple 22/7 woodcutter visual (emoji + CSS). CTA → `/philosophy/`.

7. **Final CTA + waitlist** — `bg-dark`, centered. h2 "India ki AI ki aarambh mein shamil ho." Hindi sub. 3 buttons: Join Shrutam (#waitlist scroll) / Partner With Us (mailto) / hello@aarambhax.ai (mailto). Email capture form at `id="waitlist"` — simple input + "Stay Updated" button, submits via `mailto:`.

### 2. `/about/index.html` — Our Story

1. **Cinematic header** — `min-h-[60vh]`. Hindi large `गाँव से US.` (amber), English `US se Gaon ke liye.` (primary), sub "22 saal. Do duniya. Ek sawaal. Ek mission."

2. **The Journey** — `bg-dark`, vertical timeline with left `bg-gradient-to-b from-primary to-accent` rail. 8 beats, each `bg-card/50 rounded-xl p-6 border border-white/[.07]` with a left amber dot:
   - 🌱 Start · Ek gaon. Ek kamra. Ek sapna — engineer banna.
   - 🎓 College · Pehli generation jo shahar gayi.
   - 💼 First Job · Software engineer. Chota office. Bada seekhna.
   - ✈️ Departure · Ek call aaya. Bahar jaane ka mauka.
   - 🏢 22 Years · Fortune 500 companies. Kafka. Search. AI pipelines.
   - 📱 The Message · Ek WhatsApp aaya. Ghar se.
   - 💡 The Question · 'Yeh sab gaon tak kyun nahi pahuncha?'
   - 🌅 Aarambha · India mein AI ki aarambha.

3. **Why Aarambha** — `bg-cosmos`, 2-col. Left "The Gap" (1.2B left behind), Right "The Answer" (reimagination not translation).

4. **Values** — 4 cards: 🎯 Build for Real India / 🗣️ Native AI / ♿ Include Everyone / 🔬 Quality > Speed.

### 3. `/products/index.html` — Products

1. **Header** — h1 "Aarambha Studio", badge "5 Products · 5 Elements · 1 Mission", body lede.

2. **Shrutam featured** — full-width card, permanent sky-blue glow. All 13 features listed in a 2-col grid:
   Mother Tongue Learning · Adaptive Learning · Informed Learning · Revision Mode · Ask Like 10 · Zero to Hero · Photo Doubt Solver · Mock Exams (4 levels) · Spoken English · Exam Notes · Student Tracking · Parent Portal · Reel Mode.
   Blind Mode callout: "♿ Blind Mode — India's first · FREE forever."
   CTAs: `shrutam.ai ↗` (display text) + "Join Waitlist →" (#waitlist on homepage).

3. **WhatsApp Commerce** — `id="commerce"`. Status, Vayu element, problem/solution/target paragraphs, 3-field interest form (Name, Business Type, City, `mailto:` submit).

4. **Pancha Bhoota vision** — 5 element cards:
   🌍 PRITHVI → Shrutam 🟢 · 🌬️ VAYU → WhatsApp Commerce 🔵 · 🔥 TEJAS → Visual AI ⚡ · 💧 JAL → Healthcare AI ⚡ · ✨ AKASHA → Infrastructure AI ⚡.

### 4. `/philosophy/index.html` — Philosophy

1. **Header** — h1 Hindi `तेज़ नहीं, सही`, English "Not Fast. Right." Body lede.

2. **22/7** — h2 "22/7 — The Woodcutter Principle". Story in `border-l-4 border-accent italic` blockquote. 3 principle cards (⏸️ Pause to Sharpen / 🎯 Optimize First / 🔥 Build Right). "Applied to Shrutam" paragraph.

3. **Pancha Bhoota deep** — h2 + intro quote. 5 large element cards (desktop: pentagon layout, mobile: stack). Each card: emoji (huge), Hindi name, English name, product name, philosophy line, status pill. Centered line `आरम्भ — sab ki aarambh` below.

4. **Bharat First** — h2 "Bharat First — Not India First". Distinction text + 3 stat-backed points (600K villages, 5 native languages, blind mode).

### 5. `/blog/index.html` — Minimal

Header "Seekhte Rahenge · The Aarambha Blog". Empty state: "Coming soon — first posts drop with Shrutam launch (May 20, 2026)." Small email capture → same `mailto:` as homepage.

### `/404.html`

Centered small page. Huge `404` in amber. Line: "Yeh page abhi nahi bana. Par aarambha zaroor ho chuki hai." Button: "← Wapas jaao homepage" → `/`.

## Cache-bust pipeline

### `scripts/set_cache_bust.py`
- Hashes `assets/js/translations.js` → `v = <time_ns[-10:]>-<sha256[:8]>` in dev mode (default) or `<sha256[:12]>` under `AARAMBHA_BUST_MODE=content`.
- Pattern: rewrites every `src="/assets/js/translations.js(?:\?v=[^"]*)?"` in every `*.html` at repo root.
- Single-purpose: no CSS imports to bust, no @import chains, no per-page JS files.

### `scripts/pre-commit.sh`
- Invokes `set_cache_bust.py` before each commit.
- Stages any HTML changes the bust script makes.
- Installed manually after repo init: `ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit`.

## Build sequence (atomic commits)

1. **Commit 1** — This design spec only (`docs/superpowers/specs/2026-04-17-aarambha-studio-v1-design.md`) + `.gitignore`.
2. **Commit 2** — Foundation: `CNAME`, `favicon.svg`, `favicon.ico`, `robots.txt`, `sitemap.xml` (stub), `assets/js/translations.js`, `scripts/set_cache_bust.py`, `scripts/pre-commit.sh`.
3. **Commit 3** — `index.html` (homepage, 7 sections, #waitlist form).
4. **Commit 4** — `about/index.html`.
5. **Commit 5** — `products/index.html`.
6. **Commit 6** — `philosophy/index.html`.
7. **Commit 7** — `blog/index.html`.
8. **Commit 8** — `404.html` + final `sitemap.xml` with all URLs + polish.
9. **Push to origin/main.**

## Deploy + DNS cutover

After commit 8 is pushed:

1. **Old repo** (`hforever-ai/aarambhax`) — Settings → Pages → **remove the `aarambhax.ai` custom domain**. Optionally rename repo to `aarambhax-legacy-2026` for clarity. Backup of the old site is already preserved locally at `/Users/ajayagrawal/aarambhax-backup-2026-04-17/`.
2. **New repo** (`hforever-ai/aarambha-studio`) — Settings → Pages → source `main` / `/` (root) → add custom domain `aarambhax.ai`. GitHub reads the `CNAME` file and provisions the cert.
3. **DNS** — unchanged. Existing A-record / CNAME to `hforever-ai.github.io` continues to resolve; GitHub uses the repo-side domain binding to route.
4. **Expected propagation** — ~5 min for GitHub to swap; up to a few hours for any downstream CDN worldwide.

## Risks & mitigations

1. **SEO loss** — old site's indexed pages (saavi, shrutam, faq, contact, blog posts) disappear; backlinks will 404. **Mitigation:** accepted by user ("fresh start" choice). Can revisit with 301-redirect shim later if needed.
2. **Tailwind CDN runtime perf** — in-browser compile is slower than a prebuilt bundle. **Mitigation:** marketing site with small HTML; acceptable in v1. If LCP suffers, swap to a prebuilt `tailwind.min.css` via a later commit.
3. **Alpine.js single point of failure** — whole lang toggle + hamburger depends on one external CDN. **Mitigation:** jsdelivr is a reliable CDN; fallback is "site still reads fine in English without Alpine" — nav still works, just no toggle.
4. **Shrutam.ai downstream references** — we're hard-coding "shrutam.ai" as display text in multiple places. If the domain eventually launches with a different path structure, a search-replace across 5 pages will fix it.
5. **No analytics** — v1 ships without GA/Plausible. **Mitigation:** add in a follow-up commit once copy is settled; doesn't block launch.

## Content rules (positive)

Every piece of copy across the five pages must obey:
- **Voice:** first-person plural — "We" / "हम" / "Aarambha". Never "I" or "my" attached to a person.
- **No names:** no founder name, no company legal name (Kishyam AI Pvt Ltd stays off the site entirely).
- **No employer names:** "Fortune 500 companies" is allowed as a category descriptor; specific corporate names are not.
- **No place identifiers:** the founder story mentions "ek gaon" / "village" / "US" as archetypes — never a specific village, state, or city.
- **Mixed register:** Hinglish is valid. Long copy stays in the original mixed voice even when the English/Hindi toggle is off — the toggle only swaps the ~20 keyed brand-voice strings.
- **Data-backed numbers:** 1.2B (Indians without native AI), 68% (rote-learn), 63M (MSMEs), 600K (villages), 50 lakh (blind students). Don't invent new stats; reuse these.

## Non-goals (explicit)

- No build tooling, no npm, no Node dependency, no Docker.
- No backend, no real API, no form POST targets.
- No CMS; content edits are direct HTML changes.
- No multi-language translation beyond the ~20 keyed strings.
- No A/B testing harness.
- No legacy-URL redirects from the old `aarambhax` repo.
- No blog posts in v1.
- No product detail pages beyond the single `/products/` page.
- No explicit `/saavi/`, `/shrutam/`, `/faq/`, `/contact/`, `/schools/`, `/waitlist/`, `/terms/`, `/privacy/` pages. If needed later, add as follow-up work.
