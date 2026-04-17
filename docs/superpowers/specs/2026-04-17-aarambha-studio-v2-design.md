# Aarambha Studio v2 — content expansion design spec

**Date:** 2026-04-17
**Repo:** [github.com/hforever-ai/aarambha-studio](https://github.com/hforever-ai/aarambha-studio)
**Author:** Claude + ajayagrawal
**Status:** Approved — execution pending
**Predecessor:** [v1 design](2026-04-17-aarambha-studio-v1-design.md) — shipped as commits 78e88f3..264600b

## Goal

Transform the site from a 5-page skeleton to a full AI-studio brand presence: 7-product portfolio (2 live + 5 in development), a 20-post bilingual blog seed, Nano Banana–generated editorial imagery, and a contact/partnership surface.

## Scope

**In scope**
- **Site structure additions:**
  - New `/contact/` page (6th page)
  - Homepage: new "Partner with us" section + "Press / Community" placeholder strip
  - Homepage: 7-product Pancha Bhoota preview row (replace 3-card preview)
- **Product portfolio expansion:**
  - `/products/index.html` rewritten with 7 detailed product cards
  - WhatsApp Commerce flips from `🔵 In Development` to `🟢 LIVE`
  - 5 new named products: Karta AI, Pashu AI, Bima AI, Svayam AI, Adhikar AI
  - `/philosophy/index.html` Pancha Bhoota section updated to show 7-product mapping
- **Bilingual content architecture:**
  - Each blog post has inline EN + HI versions, toggled via existing Alpine `lang` store
  - `<link rel="alternate" hreflang="en|hi">` + `lang` attributes on the two content blocks
  - Content generated NATIVELY in each language (two Gemini calls per post, NOT mechanical translation)
- **Content pipeline:**
  - `scripts/generate-post.py` — reads a brief, calls Gemini 2.5 Flash for EN + HI text + Nano Banana for hero image, writes blog post HTML
  - `scripts/generate-images.py` — standalone image runner for product cards + philosophy art
  - `content/briefs.yaml` — 20 post briefs with topic, vertical, keywords, image prompt
  - Prompt templates for voice consistency
- **Image generation (Nano Banana):**
  - 20 blog hero images (1200×630 WebP)
  - 7 product card images (800×800 WebP) — replaces emoji icons on `/products/` cards
  - 6 philosophy/brand images (Pancha Bhoota 5 elements + 22/7 woodcutter)
  - 1 default OG image
- **Blog seed — 20 posts:**
  - Shrutam (3), WhatsApp Commerce (2), Karta (2), Pashu (2), Bima (2), Svayam (2), Adhikar (2), philosophy/brand (3), Bharat-AI market analysis (2)
  - Each post: 1200–1500 words per language, proper H1/H2/H3, schema.org BlogPosting, OG tags, 2–3 internal links
- `/blog/index.html` upgrade — replace empty-state with card grid + category filter pills

**Out of scope (v2)**
- Real email capture (Mailchimp/Resend/Formspree) — keep mailto for now
- Newsletter system / RSS feed
- Blog comments / disqus
- Multi-language for product pages themselves (only blog goes EN + HI; product pages stay EN-primary with inline Hindi accents, as they are today)
- Separate-URL bilingual (`/hi/blog/<slug>/`) — deferred; single-URL toggle is simpler and good enough for launch
- Real press logos — placeholder cards only
- Real partner logos — placeholder cards only
- Analytics (GA4 / Plausible) — add in a future pass

## Content rules (unchanged from v1, re-asserted)

- Voice: "We" / "हम" / "Aarambha". Never first-person singular with names.
- No founder name, no employer name, no city/village name. Anywhere.
- Hinglish is valid; English + Hindi body copy are independent native writings, not translated pairs.
- Data-backed: reuse the canonical stats (1.2B Indians, 68% rote-learn, 63M MSMEs, 600K villages, 50 lakh blind students, 97/100K MMR). No fresh stats invented by the LLM.

## Product portfolio — the final 7

| # | Name | Element | Status | Tagline | Audience |
|---|---|---|---|---|---|
| 1 | **Shrutam** | 🌍 Prithvi | 🟢 LIVE May 20 | सुनते हैं, सीखते हैं | CG Board + CBSE Class 6-10 students |
| 2 | **WhatsApp Commerce** | 🌬️ Vayu | 🟢 LIVE | Kirana se enterprise tak | B2B distributors, kirana, pharma, FMCG |
| 3 | **Karta AI** | 🔥 Tejas | ⚡ 2026 | Compliance ki clarity | 63M MSMEs + 80M salaried taxpayers |
| 4 | **Pashu AI** | 💧 Jal | ⚡ 2026 | Pashu ka doctor, aapke phone mein | 70M dairy farmers |
| 5 | **Bima AI** | 💧 Jal | ⚡ 2026 | Claim automation, rejection nahi | Every insured Indian |
| 6 | **Svayam AI** | ✨ Akasha | ⚡ 2026 | Sarkari form, voice se bhar do | Anyone dealing with govt paperwork |
| 7 | **Adhikar AI** | ✨ Akasha | ⚡ 2026 | Pension, welfare, apne haq ka paisa | 3Cr elderly + 4Cr widows + 2Cr disabled |

Each card on `/products/` gets: status pill, element label, Nano Banana illustration, Hindi tagline, English description, problem/solution 2-col, 3–4 feature pills, "Express Interest" mailto CTA.

## Bilingual architecture

### On the page
```html
<article class="blog-post">
  <header>
    <img src="/assets/images/blog/<slug>-hero.webp" ...>
    <h1 x-show="$store.lang.current === 'en'" lang="en">English Title</h1>
    <h1 x-show="$store.lang.current === 'hi'" lang="hi" class="hindi">हिंदी शीर्षक</h1>
    <p class="meta">
      <span x-show="$store.lang.current === 'en'">Published April 17, 2026 · 7 min read</span>
      <span x-show="$store.lang.current === 'hi'" class="hindi">17 अप्रैल 2026 · 7 मिनट</span>
    </p>
  </header>
  <div class="prose" x-show="$store.lang.current === 'en'" lang="en"><!-- English body --></div>
  <div class="prose hindi" x-show="$store.lang.current === 'hi'" lang="hi"><!-- Hindi body --></div>
</article>
```

### In the head
```html
<link rel="alternate" hreflang="en-IN" href="https://aarambhax.ai/blog/<slug>/">
<link rel="alternate" hreflang="hi-IN" href="https://aarambhax.ai/blog/<slug>/">
<link rel="alternate" hreflang="x-default" href="https://aarambhax.ai/blog/<slug>/">
```

(Single URL with both languages inline. Google will index and rank for both. Separate-URL setup is a future migration.)

### Schema.org — two `BlogPosting` entries
Each post emits two `<script type="application/ld+json">` blocks — one for the EN version, one for the HI — with matching `inLanguage`, `headline`, `description`. Lets Google understand both variants.

## Content pipeline

### `scripts/generate-post.py`
Pseudo-flow:
```
for brief in briefs.yaml:
  if blog/<slug>/index.html exists: skip  (idempotent)
  en_text  = gemini_text(prompt_en(brief))   # native English
  hi_text  = gemini_text(prompt_hi(brief))   # native Hindi
  hero_img = gemini_image(brief.image_prompt)
  write blog/<slug>/index.html  (template with both versions inline)
  write assets/images/blog/<slug>-hero.webp  (resized, compressed)
  update content/briefs.yaml with `generated_at`
```

### Prompt template — English
```
You are Aarambha's content writer. Audience: Indian readers thinking about {vertical}.
Voice: confident founder-tone, warm, data-backed, NEVER corporate. Hinglish-friendly.
NO personal names, NO employer names, NO city names. Use "we" / "Aarambha".

Topic: {title}
Vertical: {vertical}
Key points to cover: {bullets}
Target length: 1200-1500 words

Output: valid HTML article body only (no <!DOCTYPE>, no <html>, no <head>, no <body>).
Use:
- One <h2> per major section (3-5 sections)
- <h3> for subsections
- One <blockquote> pullquote
- 2-3 internal links: <a href="/products/">, <a href="/philosophy/">, <a href="/about/">
- Paragraphs wrapped in <p>. Lists in <ul>/<ol>.

Start directly with the first <h2>. No preamble.
```

### Prompt template — Hindi
```
आप Aarambha के content writer हैं। पाठक: {vertical} के बारे में सोचने वाले भारतीय।
आवाज़: आत्मविश्वासी founder-tone, गर्मजोशी, data-backed, कभी corporate नहीं। Hinglish ठीक है।
किसी का नाम, company, शहर न लिखें। "हम" या "Aarambha" कहें।

विषय: {title_hindi_native}
क्षेत्र: {vertical}
मुख्य बिंदु: {bullets_hindi}
लंबाई: 1200-1500 शब्द

Output: सिर्फ़ HTML article body। कोई <!DOCTYPE>, <html>, <head>, <body> नहीं।
प्रयोग करें:
- हर मुख्य section के लिए एक <h2> (3-5 sections)
- Subsections के लिए <h3>
- एक <blockquote> pullquote
- 2-3 internal links: /products/, /philosophy/, /about/
- Paragraphs <p> में, lists <ul>/<ol> में।

सीधे पहले <h2> से शुरू करें।

महत्वपूर्ण: यह English का अनुवाद नहीं है। यह अपनी आवाज़ में लिखना है — भारतीय पाठक के लिए जो हिंदी में सोचता है।
```

**Key nuance:** the Hindi prompt says "this is NOT a translation of English — write it in its own voice for a reader who thinks in Hindi". The brief's bullets are the only shared context; the voice and examples are native to each language.

### Nano Banana image prompt template
```
Editorial illustration, dark cinematic style. Dark cosmos-navy background (#060d1a).
Warm amber (#f59e0b) and sky-blue (#0ea5e9) as singular accent lights.
Premium magazine quality, restrained, generous negative space.
Subject: {image_subject}
Indian visual cues: {cultural_context}
NO text in the image. NO logos. NO watermarks.
Composition: centered subject, shallow depth of field feel, muted palette.
```

## File structure additions

```
content/
  briefs.yaml                      NEW — 20 post briefs
scripts/
  generate-post.py                 NEW — text+image for one post
  generate-images.py               NEW — standalone image runner
assets/
  images/
    blog/                          NEW — 20 hero images (*.webp)
    products/                      NEW — 7 product card images
    philosophy/                    NEW — 6 element + woodcutter images
    og-default.webp                NEW — site-wide OG fallback
blog/
  <slug>/
    index.html                     NEW × 20 — bilingual post pages
contact/
  index.html                       NEW — 6th page
```

Existing files MODIFIED:
- `index.html` — add Partner section + Press strip + 7-product preview row
- `products/index.html` — full rewrite with 7 cards
- `philosophy/index.html` — Pancha Bhoota deep updated to 7-product mapping
- `blog/index.html` — replace empty-state with grid + category filters
- `sitemap.xml` — add /contact/ + 20 blog post URLs
- `assets/js/translations.js` — add keys for new UI labels (filter pills, section headers)

## Image strategy — Nano Banana prompts

All images: Gemini `gemini-2.5-flash-image` model. Output: 1024×1024 PNG from API, we compress to WebP + resize to target dimensions.

### Post-processing (Python + Pillow)
- **Blog hero:** crop to 16:9 → resize to 1200×630 → WebP quality 82 → target ~100KB
- **Product cards:** square crop → 800×800 → WebP quality 85 → target ~120KB
- **Philosophy/brand:** 1200×800 → WebP quality 82 → target ~140KB
- **OG default:** 1200×630 → WebP + PNG fallback → ~100KB each

### Consistency system prompt (prepended to every image call)
```
Aarambha house style: editorial dark illustration, cosmos-navy #060d1a background with
subtle stars or gradient depth, one warm amber #f59e0b accent light, one cool sky-blue
#0ea5e9 accent light. Premium magazine quality. Restrained. One subject. Negative space.
No text, no logos, no watermarks.
```

## Content calendar — 20 posts

| # | Slug | Topic | Vertical | Primary keyword |
|---|---|---|---|---|
| 1 | india-mein-ai-ki-aarambh | India mein AI ki aarambh — manifesto | brand | "AI for India" |
| 2 | bharat-vs-india | Bharat vs India — why we build for villages | brand | "bharat first AI" |
| 3 | pancha-bhoota-ai | Pancha Bhoota — ancient elements, modern AI | brand | "pancha bhoota ai" |
| 4 | 22-7-philosophy | 22/7 — tez nahi, sahi | brand | "smart work vs hard work" |
| 5 | bharat-ai-gap | India's 1.2 billion AI gap — the math | market | "india ai gap hindi" |
| 6 | hindi-vs-translation | We don't translate, we rebuild | market | "native hindi ai" |
| 7 | shrutam-hindi-medium-kids | Hindi-medium kids are falling behind | shrutam | "hindi medium study app" |
| 8 | shrutam-audio-first | Why audio-first for Class 6-10 | shrutam | "audio learning class 10" |
| 9 | shrutam-blind-mode | India's first blind-mode edtech | shrutam | "blind students app india" |
| 10 | whatsapp-commerce-msme | 63M MSMEs run on WhatsApp + Excel | commerce | "whatsapp commerce india" |
| 11 | kirana-to-distributor | Kirana to distributor — 4-layer NLP | commerce | "kirana ai tool" |
| 12 | karta-ai-gst | GSTR-1, GSTR-3B, and Karta AI | karta | "gst filing ai hindi" |
| 13 | karta-ai-itr | ITR ki zaroorat, 3 minute mein | karta | "itr filing hindi" |
| 14 | pashu-ai-cattle | Pashu ka doctor, aapke phone mein | pashu | "cattle doctor app india" |
| 15 | pashu-ai-livestock-ai | Livestock AI for rural dairy farmers | pashu | "dairy farm ai" |
| 16 | bima-ai-insurance | 40% insurance claims rejected — AI fixes | bima | "insurance claim ai" |
| 17 | bima-ai-crop-pmfby | PMFBY claims: why farmers don't file | bima | "pmfby claim hindi" |
| 18 | svayam-ai-forms | Sarkari form, voice se bhar do | svayam | "sarkari form ai" |
| 19 | svayam-ai-aadhaar | Aadhaar update, passport, caste cert — one voice | svayam | "aadhaar update hindi" |
| 20 | adhikar-ai-pension | Widow pension, old-age pension — 30% left behind | adhikar | "widow pension app india" |

Each brief in `content/briefs.yaml` has: `slug`, `title_en`, `title_hi`, `vertical`, `product` (if any), `bullets_en[]`, `bullets_hi[]`, `image_prompt`, `og_description`, `keywords`, `published_at`.

## Deploy

- Builds incrementally commit-by-commit on `main`
- Push at end of the last task (same pattern as v1)
- GitHub Pages already bound (assuming v1 cutover has happened; if not, user handles it before this phase ships)

## Risks

1. **Gemini Hindi quality** — first drafts might be "translated English" despite prompt instructions. **Mitigation:** human review after generation; re-run with stronger "do not translate" prompt if any post reads translated.
2. **Nano Banana inconsistency** — 33 images from a generative model will vary in style. **Mitigation:** shared system prompt + strict colour constraints; reject + regenerate any off-brand.
3. **Page weight creep** — 20 blog posts × inline EN+HI both rendered = bigger HTML. **Mitigation:** `x-show` hides one at parse time; Alpine strips non-visible content from render tree; images are WebP + lazy-loaded.
4. **SEO ambiguity from single-URL bilingual** — Google might pick one language to rank. **Mitigation:** `hreflang` alternates + schema.org `inLanguage` on both; revisit as separate URLs in v3 if needed.
5. **Content calendar staleness** — 20 posts shipped in one day looks suspicious. **Mitigation:** back-date published_at values across the past 60 days so the calendar feels natural.

## Success criteria

- `/contact/` serves 200 with working partner form
- Homepage has visible Partner section + Press strip
- `/products/` shows 7 detailed cards (2 🟢 LIVE + 5 ⚡ Building), each with a Nano Banana illustration
- `/philosophy/` Pancha Bhoota section shows 7 products mapped to 5 elements
- `/blog/` shows grid of 20 posts with category filters
- All 20 posts accessible at `/blog/<slug>/`, each with working EN↔HI toggle via nav lang button
- Every post has a unique hero image; no two posts share art
- All text post-generated (no hand-written HTML copy except structural shells)
- Site still passes: HTTP 200 on every page, no broken internal links, sitemap.xml lists every new URL
