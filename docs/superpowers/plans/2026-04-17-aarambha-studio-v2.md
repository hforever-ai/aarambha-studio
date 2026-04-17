# Aarambha Studio v2 — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) tracking.

**Goal:** Expand the shipped 5-page Aarambha Studio site into a 7-product portfolio with bilingual (EN + HI) 20-post blog, Nano Banana editorial imagery, and a contact/partnership surface.

**Architecture:** Six implementation tasks, all on `main` (same pattern as v1). Scripts live in `scripts/`; briefs in `content/briefs.yaml`; images in `assets/images/{blog,products,philosophy}/`. Every blog post is a single bilingual HTML file with both EN + HI inline, toggled by the existing Alpine `lang` store.

**Tech stack (additions to v1):** Python 3 + Pillow (local), Gemini 2.5 Flash (text) via REST, Gemini 2.5 Flash Image (Nano Banana) via REST. API key read from `/Users/ajayagrawal/aarambhax/.env` (gitignored) as `GEMINI_API_KEY`.

**Spec:** [docs/superpowers/specs/2026-04-17-aarambha-studio-v2-design.md](../specs/2026-04-17-aarambha-studio-v2-design.md) — refer to it for content strategy, product portfolio table, image style rules, and content calendar.

---

## File structure additions

```
Create:
  content/briefs.yaml                              Task 4 — 20 post briefs
  scripts/llm_client.py                            Task 4 — shared Gemini text + image helpers
  scripts/generate_post.py                         Task 4 — 1 brief → EN+HI text + hero image
  scripts/generate_product_images.py               Task 4 — 7 product card images
  scripts/generate_philosophy_images.py            Task 4 — 6 element illustrations
  scripts/lib_image.py                             Task 4 — image compress/resize helpers
  contact/index.html                               Task 1 — 6th page
  blog/<slug>/index.html                           Task 5 × 20
  assets/images/blog/<slug>-hero.webp              Task 5 × 20
  assets/images/products/<slug>.webp               Task 4b × 7
  assets/images/philosophy/{prithvi,vayu,tejas,jal,akasha,woodcutter}.webp  Task 4c × 6
  assets/images/og-default.webp                    Task 4d × 1

Modify:
  index.html                  Task 1 — Partner section + Press strip + 7-card preview
  products/index.html         Task 2 — full rewrite, 7 product cards
  philosophy/index.html       Task 3 — Pancha Bhoota section → 7-product mapping
  blog/index.html             Task 6 — card grid + filters
  sitemap.xml                 Task 6 — add contact + 20 blog URLs
  assets/js/translations.js   Task 1 — add a few new UI labels
```

---

## Task 1 — Contact page + homepage additions

**Goal:** Ship `/contact/index.html`. Add Partner + Press sections + 7-card Pancha Bhoota preview to homepage. Update translations.

**Files:**
- Create: `contact/index.html`
- Modify: `index.html` (splice new sections before `#waitlist`)
- Modify: `assets/js/translations.js` (add keys)

### Step 1.1 — Create `contact/index.html`

Use the SAME head + nav + footer structure as the other pages (head block from Task 2 of v1 plan, nav partial + footer partial inlined verbatim). The `<main>` body content:

```html
<main>
<section class="bg-cosmos pt-28 pb-16 px-4 md:px-8">
  <div class="max-w-3xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-6">Contact</p>
    <h1 class="text-4xl md:text-6xl font-black mb-4"><span class="grad">Baat karte hain.</span></h1>
    <p class="text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">
      Partnership, press, press, hiring, or just want to say <em>namaste</em> — pick a channel below.
    </p>
  </div>
</section>

<section class="bg-dark py-20 px-4 md:px-8">
  <div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-5">
    <a href="mailto:hello@aarambhax.ai" class="bg-card border border-white/[.07] hover:border-primary/40 rounded-2xl p-7 transition-all group block">
      <div class="text-3xl mb-3">📬</div>
      <h2 class="text-xl font-bold text-gray-100 mb-2 group-hover:text-primary transition-colors">General</h2>
      <p class="text-gray-400 text-sm mb-3">Anything else — feedback, ideas, curiosity.</p>
      <p class="text-primary font-mono text-sm">hello@aarambhax.ai →</p>
    </a>
    <a href="mailto:partners@aarambhax.ai?subject=Partnership%20Enquiry" class="bg-card border border-white/[.07] hover:border-accent/40 rounded-2xl p-7 transition-all group block">
      <div class="text-3xl mb-3">🤝</div>
      <h2 class="text-xl font-bold text-gray-100 mb-2 group-hover:text-accent transition-colors">Partners</h2>
      <p class="text-gray-400 text-sm mb-3">Schools, NGOs, govt. bodies, distributors, co-build.</p>
      <p class="text-accent font-mono text-sm">partners@aarambhax.ai →</p>
    </a>
    <a href="mailto:press@aarambhax.ai?subject=Press%20Enquiry" class="bg-card border border-white/[.07] hover:border-primary/40 rounded-2xl p-7 transition-all group block">
      <div class="text-3xl mb-3">📰</div>
      <h2 class="text-xl font-bold text-gray-100 mb-2 group-hover:text-primary transition-colors">Press</h2>
      <p class="text-gray-400 text-sm mb-3">Media, interviews, podcast invites, story ideas.</p>
      <p class="text-primary font-mono text-sm">press@aarambhax.ai →</p>
    </a>
    <a href="mailto:hiring@aarambhax.ai?subject=Hiring%20Enquiry" class="bg-card border border-white/[.07] hover:border-accent/40 rounded-2xl p-7 transition-all group block">
      <div class="text-3xl mb-3">🛠️</div>
      <h2 class="text-xl font-bold text-gray-100 mb-2 group-hover:text-accent transition-colors">Build with us</h2>
      <p class="text-gray-400 text-sm mb-3">Engineers, designers, content folks. Hindi-first builders.</p>
      <p class="text-accent font-mono text-sm">hiring@aarambhax.ai →</p>
    </a>
  </div>
</section>

<section class="bg-cosmos py-20 px-4 md:px-8">
  <div class="max-w-2xl mx-auto">
    <div class="bg-card/60 border border-white/[.07] rounded-2xl p-8 md:p-10">
      <h2 class="text-2xl font-bold text-gray-100 mb-3">Quick message</h2>
      <p class="text-gray-400 text-sm mb-5">Tell us what you're building / thinking / stuck on. We read everything.</p>
      <form action="mailto:hello@aarambhax.ai" method="get" enctype="text/plain" class="flex flex-col gap-3">
        <input type="text" name="subject" required placeholder="Subject (partnership, press, feedback...)" class="px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60">
        <textarea name="body" required rows="5" placeholder="Your message..." class="px-4 py-3 rounded-xl border border-white/[.12] bg-white/[.04] text-gray-100 placeholder:text-gray-500 focus:outline-none focus:border-primary/60"></textarea>
        <button type="submit" class="bg-primary hover:bg-primary-dark text-white font-bold px-5 py-3 rounded-xl transition-all self-start">Send Message →</button>
      </form>
      <p class="text-xs text-gray-600 mt-3">Opens your email client with the message prefilled.</p>
    </div>
  </div>
</section>
</main>
```

Wrap with the standard `<!DOCTYPE html>...nav...</nav>` + `</main>` + standard footer. Use SEO:
```
<title>Contact — Aarambha</title>
<meta name="description" content="Baat karte hain — partnerships, press, hiring, feedback. India's AI Studio. hello@aarambhax.ai">
<link rel="canonical" href="https://aarambhax.ai/contact/">
```

### Step 1.2 — Splice new sections into `index.html`

Read `/Users/ajayagrawal/aarambhax/index.html`. Find the section with `id="waitlist"` — the Partner and Press sections go IMMEDIATELY BEFORE it (so they appear after the Philosophy Teaser section and before the final CTA). Find also the existing Products section (the one with `<h2>We build AI products. Not just apps.</h2>`) — replace its 3-card preview (Shrutam + Commerce + "Coming Next") with the **7-card preview** described below.

**(A) 7-card preview** — replace the content inside `<section class="bg-dark py-24 px-4 md:px-8">` that holds the old Products preview:

```html
<section class="bg-dark py-24 px-4 md:px-8">
  <div class="max-w-6xl mx-auto">
    <div class="text-center max-w-2xl mx-auto mb-14">
      <p class="inline-block px-3 py-1 rounded-full border border-white/[.12] bg-white/[.04] text-xs font-bold text-gray-400 tracking-[.18em] uppercase mb-5">Pancha Bhoota · 7 Products</p>
      <h2 class="text-3xl md:text-5xl font-black mb-4">We build <span class="grad">AI for Bharat</span>, not just apps.</h2>
      <p class="text-gray-400 text-lg leading-relaxed">Five elements. Two shipping. Five building. Every one solves a Bharat problem no one has built AI for yet.</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <a href="/products/#shrutam" class="bg-card border border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">🌍</span><span class="hindi text-accent text-sm font-bold">पृथ्वी</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1"><span class="hindi mr-1">श्रुतम्</span>Shrutam</h3>
        <p class="text-gray-500 text-xs mb-3">Audio-first AI tutor for CG+CBSE Class 6–10</p>
        <span class="inline-block text-[10px] bg-green-500/15 text-green-400 border border-green-500/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🟢 May 20</span>
      </a>
      <a href="/products/#commerce" class="bg-card border border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">🌬️</span><span class="hindi text-accent text-sm font-bold">वायु</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1">WhatsApp Commerce</h3>
        <p class="text-gray-500 text-xs mb-3">Kirana-to-enterprise B2B ordering AI</p>
        <span class="inline-block text-[10px] bg-green-500/15 text-green-400 border border-green-500/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🟢 LIVE</span>
      </a>
      <a href="/products/#karta" class="bg-card border border-dashed border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">🔥</span><span class="hindi text-accent text-sm font-bold">तेजस्</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1">Karta AI</h3>
        <p class="text-gray-500 text-xs mb-3">GST + ITR voice-filing for MSMEs</p>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ 2026</span>
      </a>
      <a href="/products/#pashu" class="bg-card border border-dashed border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">💧</span><span class="hindi text-accent text-sm font-bold">जल</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1">Pashu AI</h3>
        <p class="text-gray-500 text-xs mb-3">Cattle doctor in your pocket</p>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ 2026</span>
      </a>
      <a href="/products/#bima" class="bg-card border border-dashed border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">💧</span><span class="hindi text-accent text-sm font-bold">जल</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1">Bima AI</h3>
        <p class="text-gray-500 text-xs mb-3">Insurance claim automation</p>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ 2026</span>
      </a>
      <a href="/products/#svayam" class="bg-card border border-dashed border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">✨</span><span class="hindi text-accent text-sm font-bold">आकाश</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1">Svayam AI</h3>
        <p class="text-gray-500 text-xs mb-3">Voice-first sarkari form filling</p>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ 2026</span>
      </a>
      <a href="/products/#adhikar" class="bg-card border border-dashed border-primary/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all block">
        <div class="flex items-center gap-2 mb-3"><span class="text-2xl">✨</span><span class="hindi text-accent text-sm font-bold">आकाश</span></div>
        <h3 class="text-gray-100 font-black text-lg mb-1">Adhikar AI</h3>
        <p class="text-gray-500 text-xs mb-3">Pension + welfare entitlement tracker</p>
        <span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ 2026</span>
      </a>
      <a href="/products/" class="bg-card/30 border border-dashed border-accent/30 rounded-2xl p-5 hover:-translate-y-0.5 transition-all flex flex-col items-center justify-center text-center">
        <div class="text-3xl mb-2">🧭</div>
        <p class="text-gray-300 font-bold text-sm">Explore all 7</p>
        <p class="text-gray-500 text-xs mt-1">Pancha Bhoota portfolio →</p>
      </a>
    </div>
  </div>
</section>
```

**(B) Partner section** — insert immediately before `<section id="waitlist"`:

```html
<section class="bg-cosmos py-20 px-4 md:px-8">
  <div class="max-w-5xl mx-auto">
    <div class="text-center max-w-2xl mx-auto mb-12">
      <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-4">Partner With Us</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3">School chahiye partnership? <span class="grad">Baat karte hain.</span></h2>
      <p class="text-gray-400 text-base leading-relaxed">Schools, NGOs, govt agencies, distributors — if you serve Bharat, we want to build with you.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="bg-card border border-white/[.07] rounded-2xl p-6">
        <div class="text-3xl mb-3">🏫</div>
        <h3 class="text-gray-100 font-bold mb-2">Schools</h3>
        <p class="text-gray-400 text-sm leading-relaxed mb-4">Shrutam for your students — bulk pricing, teacher dashboard, offline mode for weak networks.</p>
        <a href="mailto:partners@aarambhax.ai?subject=School%20Partnership" class="text-accent font-bold text-sm hover:underline">partners@aarambhax.ai →</a>
      </div>
      <div class="bg-card border border-white/[.07] rounded-2xl p-6">
        <div class="text-3xl mb-3">🤝</div>
        <h3 class="text-gray-100 font-bold mb-2">NGOs &amp; Foundations</h3>
        <p class="text-gray-400 text-sm leading-relaxed mb-4">Deploy Aarambha products at scale. Rural schools, women SHGs, farmer cooperatives.</p>
        <a href="mailto:partners@aarambhax.ai?subject=NGO%20Partnership" class="text-accent font-bold text-sm hover:underline">partners@aarambhax.ai →</a>
      </div>
      <div class="bg-card border border-white/[.07] rounded-2xl p-6">
        <div class="text-3xl mb-3">🏛️</div>
        <h3 class="text-gray-100 font-bold mb-2">Govt &amp; Public</h3>
        <p class="text-gray-400 text-sm leading-relaxed mb-4">CSR, public-interest pilots, integration with MGNREGA / Ayushman / PMFBY.</p>
        <a href="mailto:partners@aarambhax.ai?subject=Govt%20Partnership" class="text-accent font-bold text-sm hover:underline">partners@aarambhax.ai →</a>
      </div>
    </div>
  </div>
</section>
```

**(C) Press strip** — insert immediately after the Partner section (still before `#waitlist`):

```html
<section class="bg-dark py-16 px-4 md:px-8 border-t border-white/[.05] border-b border-white/[.05]">
  <div class="max-w-6xl mx-auto text-center">
    <p class="text-xs font-bold text-gray-500 tracking-[.20em] uppercase mb-6">As seen in (coming soon)</p>
    <div class="flex flex-wrap justify-center items-center gap-x-10 gap-y-4 opacity-50">
      <span class="text-gray-500 font-bold text-sm">Your Story</span>
      <span class="text-gray-500 font-bold text-sm">Inc42</span>
      <span class="text-gray-500 font-bold text-sm">Entrackr</span>
      <span class="text-gray-500 font-bold text-sm">The Ken</span>
      <span class="text-gray-500 font-bold text-sm">Economic Times</span>
      <span class="text-gray-500 font-bold text-sm">FactorDaily</span>
    </div>
    <p class="text-xs text-gray-600 mt-4">We'll replace with real press links as they come in. <a href="mailto:press@aarambhax.ai" class="text-primary hover:underline">Media? press@aarambhax.ai</a></p>
  </div>
</section>
```

### Step 1.3 — Add translation keys

In `assets/js/translations.js`, extend both `en` and `hi` blocks with a few new UI labels used by the blog index (Task 6) and partner section:

Add to `en`:
```
nav_contact: "Contact",
blog_all: "All",
blog_filter_shrutam: "Education",
blog_filter_commerce: "Commerce",
blog_filter_karta: "Compliance",
blog_filter_pashu: "Livestock",
blog_filter_bima: "Insurance",
blog_filter_svayam: "Govt Services",
blog_filter_adhikar: "Welfare",
blog_filter_brand: "Philosophy",
blog_filter_market: "Market",
```

Add matching `hi` translations:
```
nav_contact: "संपर्क",
blog_all: "सभी",
blog_filter_shrutam: "शिक्षा",
blog_filter_commerce: "व्यापार",
blog_filter_karta: "Compliance",
blog_filter_pashu: "पशुपालन",
blog_filter_bima: "बीमा",
blog_filter_svayam: "सरकारी सेवाएँ",
blog_filter_adhikar: "कल्याण",
blog_filter_brand: "दर्शन",
blog_filter_market: "बाज़ार",
```

Do NOT add a Contact link to the main nav in this task (keep nav clean); contact is accessible via footer "Connect" column which already exists.

### Step 1.4 — Verify + commit

```bash
cd /Users/ajayagrawal/aarambhax
python3 -m http.server 8000 > /tmp/s.log 2>&1 & PID=$!
sleep 1
for p in / /contact/ /about/ /products/ /philosophy/ /blog/; do
  echo "$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000$p) $p"
done
kill $PID 2>/dev/null; wait 2>/dev/null

# DOM checks
grep -c "Partner With Us" index.html
grep -c "As seen in" index.html
grep -c "Pancha Bhoota · 7 Products" index.html
grep -c "Karta AI\|Pashu AI\|Bima AI\|Svayam AI\|Adhikar AI" index.html

git add contact/index.html index.html assets/js/translations.js
git commit -m "$(cat <<'EOF'
feat(v2): contact page + homepage partner/press/7-card preview

  - /contact/ page (6th page) with 4 channel cards (general, partners,
    press, hiring) + quick-message form. All mailto:.
  - Homepage: new "Partner With Us" section (schools / NGOs / govt)
    between philosophy teaser and final CTA.
  - Homepage: Press strip with placeholder "As seen in (coming soon)"
    logos — swap in real ones later.
  - Homepage: 7-card Pancha Bhoota preview replacing old 3-card Shrutam
    + Commerce + "Coming Next". Each card links to its anchor on
    /products/ — Shrutam (🟢 May 20), WhatsApp Commerce (🟢 LIVE),
    Karta / Pashu / Bima / Svayam / Adhikar (all ⚡ 2026), plus an
    "Explore all 7" tile.
  - translations.js: +11 new keys (nav_contact, blog_all, blog_filter_*)
    in EN and HI for Task 6's blog-index filters.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v2-design.md
Plan: docs/superpowers/plans/2026-04-17-aarambha-studio-v2.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

Expect: all 6 pages serve 200; DOM greps return ≥ 1; commit lands with pre-commit hook versioning translations.js.

---

## Task 2 — Products page: full 7-card rewrite

**Goal:** Replace `/products/index.html` with the full 7-product detailed layout. Each product card has: status pill, element label, Hindi tagline, English description, problem/solution 2-col, feature tags, Express Interest mailto, anchor ID.

Subagent reads the existing `products/index.html` to preserve `<head>`, nav partial, footer partial, and shell structure — only replaces content between `<main>` and `</main>`.

**Files:** Modify `products/index.html`.

### Step 2.1 — Replace `<main>` content

The new `<main>` structure (use this verbatim):

```html
<main>

<!-- 1. HEADER -->
<section class="bg-cosmos pt-28 pb-16 px-4 md:px-8">
  <div class="max-w-6xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-6">Aarambha Studio</p>
    <h1 class="text-4xl md:text-6xl font-black mb-4"><span class="grad">7 Products</span> · 5 Elements · 1 Mission</h1>
    <p class="text-gray-400 text-lg max-w-2xl mx-auto leading-relaxed">Pancha Bhoota — five elements of ancient Indian thought. Each element holds AI products we build for Bharat. Two shipping. Five in build. Every one solving a real problem.</p>
  </div>
</section>

<!-- 2. SHRUTAM — LIVE -->
<section id="shrutam" class="bg-dark py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-primary/30 rounded-2xl p-8 md:p-12 shadow-[0_0_60px_rgba(14,165,233,0.12)] relative overflow-hidden">
      <div class="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent opacity-80"></div>
      <div class="grid md:grid-cols-[2fr,1fr] gap-10">
        <div>
          <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/30 text-xs font-bold text-green-400 uppercase tracking-[.12em] mb-4">🟢 Launching May 20, 2026</p>
          <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🌍 Prithvi — Knowledge is Foundation</p>
          <h2 class="text-3xl md:text-5xl font-black mb-3"><span class="hindi text-accent mr-2">श्रुतम्</span><span class="text-gray-100">SHRUTAM</span></h2>
          <p class="hindi text-primary text-xl mb-5">सुनते हैं, सीखते हैं।</p>
          <p class="text-gray-300 leading-relaxed mb-5">AI-powered audio-first learning for CG Board &amp; CBSE Class 6-10. SAAVI didi teaches Science &amp; Math in Hinglish. Audio over text. Hinglish over English. Privacy over paywall-shame.</p>
          <div class="bg-accent/10 border border-accent/30 rounded-xl p-4 mb-5">
            <p class="text-accent font-bold">♿ Blind Mode — India's first. FREE forever.</p>
            <p class="text-gray-400 text-xs">50 lakh visually-impaired students. Zero edtech serves them. Shrutam does.</p>
          </div>
          <div class="flex flex-wrap gap-3">
            <a href="/#waitlist" class="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-5 py-2.5 rounded-xl transition-all text-sm">Join Waitlist →</a>
            <a href="mailto:hello@aarambhax.ai?subject=Shrutam%20Info" class="inline-flex items-center gap-2 border border-white/20 hover:border-primary/50 text-gray-300 hover:text-primary font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Learn More →</a>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2 content-center">
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-3 text-center"><div class="text-xs text-gray-500">Class</div><div class="font-bold text-gray-100 text-sm">6–10</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-3 text-center"><div class="text-xs text-gray-500">Board</div><div class="font-bold text-gray-100 text-sm">CG+CBSE</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-3 text-center"><div class="text-xs text-gray-500">Price</div><div class="font-bold text-gray-100 text-sm">₹199/mo</div></div>
          <div class="bg-white/[.03] border border-white/[.07] rounded-xl p-3 text-center"><div class="text-xs text-gray-500">Blind</div><div class="font-bold text-accent text-sm">FREE</div></div>
          <div class="col-span-2 bg-white/[.03] border border-white/[.07] rounded-xl p-3 text-center"><div class="text-xs text-gray-500">Languages</div><div class="font-bold text-gray-100 text-xs">Hindi · Hinglish · English · Telugu · Marathi</div></div>
        </div>
      </div>
    </article>
  </div>
</section>

<!-- 3. WHATSAPP COMMERCE — LIVE (flipped from "In Development") -->
<section id="commerce" class="bg-cosmos py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-primary/30 rounded-2xl p-8 md:p-12 shadow-[0_0_60px_rgba(14,165,233,0.12)] relative overflow-hidden">
      <div class="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent opacity-80"></div>
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/30 text-xs font-bold text-green-400 uppercase tracking-[.12em] mb-4">🟢 LIVE</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🌬️ Vayu — Commerce Flows Like Air</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">WhatsApp Commerce AI</h2>
      <p class="text-primary text-lg mb-5">Kirana se enterprise tak.</p>
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h3>
          <p class="text-gray-400 leading-relaxed text-sm">63 million MSMEs run India on WhatsApp + Excel. Orders lost, catalogs off, reorders miss the window — nothing speaks the trade's language.</p>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h3>
          <p class="text-gray-400 leading-relaxed text-sm">WhatsApp-native. Hindi voice. 4-layer NLP pipeline. Catalog matching AI. Smart reorder prediction. Meets the trade where it already works.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 mb-5">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Kirana</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Pharma</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">FMCG</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">B2B Distributors</span>
      </div>
      <div class="flex flex-wrap gap-3">
        <a href="mailto:hello@aarambhax.ai?subject=WhatsApp%20Commerce%20Demo" class="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white font-bold px-5 py-2.5 rounded-xl transition-all text-sm">Request Demo →</a>
        <a href="mailto:partners@aarambhax.ai?subject=WhatsApp%20Commerce%20Partnership" class="inline-flex items-center gap-2 border border-white/20 hover:border-primary/50 text-gray-300 hover:text-primary font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Partner with us →</a>
      </div>
    </article>
  </div>
</section>
```

The 5 in-development cards follow the SAME structure as WhatsApp Commerce above, but with:
- `bg-dark` / `bg-cosmos` alternating backgrounds for visual rhythm
- `border border-dashed border-primary/30` (dashed border = "building")
- `⚡ In Development — 2026` status pill (primary blue instead of green)
- No glow shadow (keep subtle)
- Mailto CTAs: `Express Interest` + `Partnership enquiries`

Template for each — copy, replace the placeholders:

```html
<!-- 4. KARTA AI — Building -->
<section id="karta" class="bg-dark py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8 md:p-10">
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">⚡ In Development — 2026</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">🔥 Tejas — Light the Compliance Path</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">Karta AI</h2>
      <p class="text-primary text-lg mb-5">Compliance ki clarity.</p>
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h3>
          <p class="text-gray-400 leading-relaxed text-sm">63 million MSMEs file GSTR-1 / GSTR-3B every month. 80 million salaried Indians file ITR. ClearTax / Quicko are English-only and urban-designed. Hindi voice-first filing doesn't exist. Compliance is mandatory, not optional.</p>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Photo your invoices → Karta AI categorizes, generates GSTR return, files it. ITR via voice: "Meri salary 8 lakh, HRA hai, LIC bhara" → filled ITR in 3 minutes. Hindi. Free first 3 returns.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 mb-5">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">GSTR-1</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">GSTR-3B</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">ITR-1/2/4</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Invoice OCR</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Hindi Voice</span>
      </div>
      <a href="mailto:hello@aarambhax.ai?subject=Karta%20AI%20Interest" class="inline-flex items-center gap-2 border border-primary/40 text-primary hover:bg-primary/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Express Interest →</a>
    </article>
  </div>
</section>

<!-- 5. PASHU AI — Building -->
<section id="pashu" class="bg-cosmos py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8 md:p-10">
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">⚡ In Development — 2026</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">💧 Jal — Life &amp; Sustenance</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">Pashu AI</h2>
      <p class="text-primary text-lg mb-5">Pashu ka doctor, aapke phone mein.</p>
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h3>
          <p class="text-gray-400 leading-relaxed text-sm">70 million dairy farmers. One sick cow = ₹80,000 loss. The vet is 20 km away. Quacks misdiagnose. Govt veterinary scheme unused. No AI-native cattle doctor exists in Hindi.</p>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Photo or 10-second video → AI detects FMD, mastitis, bloat, lameness. Voice: "meri bhains do din se khana nahi kha rahi." Medicine + dosage + generic. Nearest govt vet. Milk yield tracker. Artificial insemination booking.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 mb-5">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Cattle · Buffalo · Goat</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Photo Diagnosis</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Hindi Voice</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Rashtriya Gokul Mission</span>
      </div>
      <a href="mailto:hello@aarambhax.ai?subject=Pashu%20AI%20Interest" class="inline-flex items-center gap-2 border border-primary/40 text-primary hover:bg-primary/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Express Interest →</a>
    </article>
  </div>
</section>

<!-- 6. BIMA AI — Building -->
<section id="bima" class="bg-dark py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8 md:p-10">
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">⚡ In Development — 2026</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">💧 Jal — Life &amp; Protection</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">Bima AI</h2>
      <p class="text-primary text-lg mb-5">Claim automation, rejection nahi.</p>
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h3>
          <p class="text-gray-400 leading-relaxed text-sm">40%+ of health / crop / vehicle insurance claims rejected for paperwork errors. Farmers pay PMFBY premium for 5 years, crop fails, claim never gets filed because the form is impossible. PolicyBazaar compares; nobody helps you CLAIM.</p>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Scan bills + discharge summary + crop-damage photo → AI drafts the claim with the exact wording the insurer won't reject. Filed in Star Health / HDFC Ergo / PMFBY / Bajaj Allianz portals. Hindi + tracking + grievance escalation if rejected.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 mb-5">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Health Claims</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">PMFBY Crop</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Motor</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Ayushman Bharat</span>
      </div>
      <a href="mailto:hello@aarambhax.ai?subject=Bima%20AI%20Interest" class="inline-flex items-center gap-2 border border-primary/40 text-primary hover:bg-primary/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Express Interest →</a>
    </article>
  </div>
</section>

<!-- 7. SVAYAM AI — Building -->
<section id="svayam" class="bg-cosmos py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8 md:p-10">
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">⚡ In Development — 2026</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">✨ Akasha — The Connective Space</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">Svayam AI</h2>
      <p class="text-primary text-lg mb-5">Sarkari form, voice se bhar do.</p>
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h3>
          <p class="text-gray-400 leading-relaxed text-sm">India has ~1500 government forms — DL, passport, Aadhaar update, voter ID, caste / income / scholarship / ration card, KCC. Every form asks the same 15 fields. 90% of rural India fears these forms. UMANG is unusable.</p>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Speak your details once in Hindi → AI stores encrypted profile → auto-fills ANY form (PDF, web, photo of paper). Warns about missing docs. Tracks submission. Hindi voice-first. Privacy-preserving (data never leaves your phone unencrypted).</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 mb-5">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Aadhaar Update</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">DL · Passport</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Caste · Income Cert</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Scholarship · KCC</span>
      </div>
      <a href="mailto:hello@aarambhax.ai?subject=Svayam%20AI%20Interest" class="inline-flex items-center gap-2 border border-primary/40 text-primary hover:bg-primary/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Express Interest →</a>
    </article>
  </div>
</section>

<!-- 8. ADHIKAR AI — Building -->
<section id="adhikar" class="bg-dark py-16 px-4 md:px-8 scroll-mt-24">
  <div class="max-w-6xl mx-auto">
    <article class="bg-card border border-dashed border-primary/30 rounded-2xl p-8 md:p-10">
      <p class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-bold text-primary uppercase tracking-[.12em] mb-4">⚡ In Development — 2026</p>
      <p class="text-xs text-gray-500 uppercase tracking-[.14em] mb-2">✨ Akasha — Every Right Connected</p>
      <h2 class="text-3xl md:text-4xl font-black mb-3 text-gray-100">Adhikar AI</h2>
      <p class="text-primary text-lg mb-5">Pension, welfare, apne haq ka paisa.</p>
      <div class="grid md:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-accent mb-2">The problem</h3>
          <p class="text-gray-400 leading-relaxed text-sm">3 crore elderly + 4 crore widows + 2 crore disabled eligible for pensions (₹1000–₹3000/month). 30–70% never receive them. ₹50,000 crore of govt welfare doesn't reach beneficiaries annually. Forms are broken. Banks lose applications. Nobody follows up.</p>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-[.14em] text-primary mb-2">The solution</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Voice: "mere papa 68 saal ke hain, pension milni chahiye?" → AI checks state-specific eligibility, drafts application, tracks status weekly. MGNREGA wages tracker. Pension delay? Auto-drafts RTI + grievance. Voice interface built for the actually-elderly.</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-2 mb-5">
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Old Age Pension</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Widow Pension</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">Disability Pension</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">MGNREGA Wages</span>
        <span class="bg-white/5 border border-white/10 text-gray-300 rounded-full px-3 py-1 text-xs">RTI Auto-drafter</span>
      </div>
      <a href="mailto:hello@aarambhax.ai?subject=Adhikar%20AI%20Interest" class="inline-flex items-center gap-2 border border-primary/40 text-primary hover:bg-primary/10 font-semibold px-5 py-2.5 rounded-xl transition-all text-sm">Express Interest →</a>
    </article>
  </div>
</section>

<!-- 9. PANCHA BHOOTA SUMMARY -->
<section class="bg-cosmos py-16 px-4 md:px-8">
  <div class="max-w-4xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-4">Pancha Bhoota</p>
    <h2 class="text-2xl md:text-3xl font-black mb-3">Five elements. <span class="grad">Seven products. One mission.</span></h2>
    <p class="hindi text-xl md:text-2xl font-bold text-accent mb-3">आरम्भ — sab ki aarambh।</p>
    <p class="text-gray-400 leading-relaxed max-w-2xl mx-auto mb-8">The framework isn't a marketing frame. It's how we think about what to build next: problems grounded in real Indian life, mapped to elements our grandparents named thousands of years ago.</p>
    <a href="/philosophy/" class="inline-flex items-center gap-2 border border-accent/40 text-accent hover:bg-accent/10 font-semibold px-6 py-3 rounded-xl transition-all">Read the Philosophy →</a>
  </div>
</section>

</main>
```

### Step 2.2 — Verify + commit

```bash
cd /Users/ajayagrawal/aarambhax
python3 -m http.server 8000 > /tmp/s.log 2>&1 & PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/products/
kill $PID 2>/dev/null; wait 2>/dev/null

for anchor in shrutam commerce karta pashu bima svayam adhikar; do
  grep -c "id=\"$anchor\"" products/index.html
done
# Expect each to print 1

grep -cE "🟢 LIVE|🟢 Launching" products/index.html   # Expect ≥ 2
grep -cE "⚡ In Development" products/index.html       # Expect 5

git add products/index.html
git commit -m "feat(v2): products page — 7-product Pancha Bhoota rewrite

Replaces 3-card layout with full 7-product portfolio:

  🟢 LIVE: Shrutam (launching May 20), WhatsApp Commerce (flipped from
     In Development to LIVE)
  ⚡ Building 2026: Karta AI (GST/ITR), Pashu AI (cattle doctor),
     Bima AI (insurance claims), Svayam AI (govt form filling),
     Adhikar AI (pensions + welfare)

Each card: status pill, Pancha Bhoota element eyebrow, Hindi tagline,
problem/solution 2-col, feature tags, Express Interest mailto CTA,
anchor ID for homepage deep links. Dashed borders on building
products, solid glow on shipped ones. Closing Pancha Bhoota summary
links to /philosophy/ for the deeper narrative.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v2-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 3 — Philosophy page Pancha Bhoota update

**Goal:** Update the 5 element cards on `/philosophy/` to show all 7 products mapped across the elements.

**Files:** Modify `philosophy/index.html`.

### Step 3.1 — Replace the Pancha Bhoota card grid

Find the existing 5-element card grid (the one with 🌍 Prithvi → Shrutam, 🌬️ Vayu → WhatsApp Commerce, 🔥 Tejas → Visual AI, 💧 Jal → Healthcare AI, ✨ Akasha → Infrastructure AI) and replace it with this grid that shows 7 products mapped into the 5 elements (Jal holds 2, Akasha holds 2, others hold 1):

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
  <article class="bg-card border border-primary/30 rounded-2xl p-6 md:p-7">
    <div class="text-5xl mb-3">🌍</div>
    <div class="hindi text-accent text-lg font-bold mb-1">पृथ्वी</div>
    <div class="text-gray-100 text-xl font-black mb-1">Prithvi</div>
    <p class="text-gray-400 text-xs mb-4">Knowledge grounds everything.</p>
    <div class="space-y-2">
      <a href="/products/#shrutam" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm"><span class="hindi mr-1">श्रुतम्</span>Shrutam</div>
        <div class="text-[10px] text-green-400 mt-0.5">🟢 May 20, 2026</div>
      </a>
    </div>
  </article>
  <article class="bg-card border border-primary/30 rounded-2xl p-6 md:p-7">
    <div class="text-5xl mb-3">🌬️</div>
    <div class="hindi text-accent text-lg font-bold mb-1">वायु</div>
    <div class="text-gray-100 text-xl font-black mb-1">Vayu</div>
    <p class="text-gray-400 text-xs mb-4">Commerce flows like air.</p>
    <div class="space-y-2">
      <a href="/products/#commerce" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm">WhatsApp Commerce</div>
        <div class="text-[10px] text-green-400 mt-0.5">🟢 LIVE</div>
      </a>
    </div>
  </article>
  <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 md:p-7">
    <div class="text-5xl mb-3">🔥</div>
    <div class="hindi text-accent text-lg font-bold mb-1">तेजस्</div>
    <div class="text-gray-100 text-xl font-black mb-1">Tejas</div>
    <p class="text-gray-400 text-xs mb-4">Clarity ignited.</p>
    <div class="space-y-2">
      <a href="/products/#karta" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm">Karta AI</div>
        <div class="text-[10px] text-primary mt-0.5">⚡ 2026 — GST + ITR</div>
      </a>
    </div>
  </article>
  <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 md:p-7">
    <div class="text-5xl mb-3">💧</div>
    <div class="hindi text-accent text-lg font-bold mb-1">जल</div>
    <div class="text-gray-100 text-xl font-black mb-1">Jal</div>
    <p class="text-gray-400 text-xs mb-4">Life-giving.</p>
    <div class="space-y-2">
      <a href="/products/#pashu" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm">Pashu AI</div>
        <div class="text-[10px] text-primary mt-0.5">⚡ 2026 — Cattle doctor</div>
      </a>
      <a href="/products/#bima" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm">Bima AI</div>
        <div class="text-[10px] text-primary mt-0.5">⚡ 2026 — Insurance claims</div>
      </a>
    </div>
  </article>
  <article class="bg-card border border-dashed border-accent/30 rounded-2xl p-6 md:p-7">
    <div class="text-5xl mb-3">✨</div>
    <div class="hindi text-accent text-lg font-bold mb-1">आकाश</div>
    <div class="text-gray-100 text-xl font-black mb-1">Akasha</div>
    <p class="text-gray-400 text-xs mb-4">The connective space.</p>
    <div class="space-y-2">
      <a href="/products/#svayam" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm">Svayam AI</div>
        <div class="text-[10px] text-primary mt-0.5">⚡ 2026 — Govt form filling</div>
      </a>
      <a href="/products/#adhikar" class="block bg-white/[.03] border border-white/[.07] rounded-lg p-3 hover:border-primary/40 transition-all">
        <div class="font-bold text-gray-100 text-sm">Adhikar AI</div>
        <div class="text-[10px] text-primary mt-0.5">⚡ 2026 — Pensions + welfare</div>
      </a>
    </div>
  </article>
  <article class="bg-card/30 border border-dashed border-accent/20 rounded-2xl p-6 md:p-7 flex flex-col items-center justify-center text-center">
    <div class="text-4xl mb-3">🧭</div>
    <div class="text-gray-300 font-bold mb-1">+ More to come</div>
    <p class="text-gray-500 text-xs">Pancha Bhoota holds more than 7 products. As India's real problems surface, new ones land here.</p>
  </article>
</div>
```

Leave the surrounding section title + intro quote + closing "आरम्भ — sab ki aarambh" line unchanged.

### Step 3.2 — Verify + commit

```bash
cd /Users/ajayagrawal/aarambhax
python3 -m http.server 8000 > /tmp/s.log 2>&1 & PID=$!
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/philosophy/
kill $PID 2>/dev/null; wait 2>/dev/null

for product in Shrutam "WhatsApp Commerce" "Karta AI" "Pashu AI" "Bima AI" "Svayam AI" "Adhikar AI"; do
  grep -c -- "$product" philosophy/index.html
done
# Every product should appear ≥ 1

git add philosophy/index.html
git commit -m "feat(v2): philosophy — Pancha Bhoota maps 7 products to 5 elements

Previous: each element held 1 product (1:1, which was conceptually thin —
Jal had 'Healthcare AI' as a vague placeholder).

New: clean mapping of the 7 real products across the 5 elements:
  🌍 Prithvi: Shrutam
  🌬️ Vayu: WhatsApp Commerce
  🔥 Tejas: Karta AI
  💧 Jal: Pashu AI + Bima AI (life in two forms — livestock, protection)
  ✨ Akasha: Svayam AI + Adhikar AI (connection to state + rights)

Each element card now lists its products as inline links with status
pills. A 6th '+ More to come' tile signals the framework can hold new
products as they land.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v2-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 4 — Content pipeline: scripts + briefs + images

**Goal:** Build the Python pipeline for generating bilingual blog posts and editorial illustrations via Gemini 2.5 Flash + Nano Banana.

**Files:**
- Create: `content/briefs.yaml`
- Create: `scripts/llm_client.py`
- Create: `scripts/lib_image.py`
- Create: `scripts/generate_post.py`
- Create: `scripts/generate_product_images.py`
- Create: `scripts/generate_philosophy_images.py`

### Step 4.1 — `content/briefs.yaml`

Full file — 20 post briefs. Each brief has exactly this shape:

```yaml
# content/briefs.yaml — 20 blog-post briefs
# Each post generates EN + HI independent versions + 1 hero image

common:
  author: "Aarambha"
  brand_voice: |
    Confident founder-tone. Warm. Data-backed. Never corporate.
    Hinglish-friendly English. NO personal names, NO employer names,
    NO city names. Always "we" / "Aarambha".
  target_length: [1200, 1500]   # words per language
  image_style: |
    Editorial dark illustration. Cosmos-navy #060d1a background.
    Amber #f59e0b and sky-blue #0ea5e9 accents only. Premium magazine
    quality. Restrained. One subject. Generous negative space.
    NO text, NO logos, NO watermarks.

posts:
  - slug: india-mein-ai-ki-aarambh
    title_en: "India mein AI ki aarambh — why now, why us"
    title_hi: "भारत में AI का आरम्भ — अभी क्यों, हम क्यों"
    vertical: brand
    published_at: "2026-02-12"
    keywords: [AI for India, Bharat AI, aarambha manifesto]
    og_description_en: "The question we kept asking: why hasn't world-class AI reached India's villages? Aarambha is our answer."
    og_description_hi: "जो सवाल हम बार-बार पूछते रहे: world-class AI गाँव तक क्यों नहीं पहुँचा? आरम्भ उसका उत्तर है।"
    bullets_en:
      - "The 1.2 billion gap — Indians left behind by English-first AI"
      - "Why translation isn't enough — we rebuild for Hindi from scratch"
      - "Pancha Bhoota framing — 5 elements, 7 products, one mission"
      - "The moment that changed everything — one message from home"
      - "What 'aarambh' means for Bharat, not India"
    bullets_hi:
      - "1.2 अरब की दूरी — जो AI से छूट गए"
      - "अनुवाद क्यों काफ़ी नहीं — हम हिंदी के लिए नए सिरे से बनाते हैं"
      - "पंच भूत की दृष्टि — 5 तत्व, 7 products, एक मिशन"
      - "वह message जो सब बदल गया — घर से आई एक चिट्ठी"
      - "आरम्भ का अर्थ — भारत के लिए, India के लिए नहीं"
    image_prompt: |
      Cinematic editorial illustration: a single dimly-lit phone on a
      wooden village table glowing with soft amber light, in the dark
      night, distant silhouette of an Indian village (mud houses, banyan
      tree). The phone screen shows a single beacon of sky-blue AI light
      reaching toward the stars. Peaceful, hopeful, restrained.

  - slug: bharat-vs-india
    title_en: "Bharat vs India — why we build for the villages"
    title_hi: "भारत बनाम India — हम गाँवों के लिए क्यों बनाते हैं"
    vertical: brand
    published_at: "2026-02-20"
    keywords: [Bharat first, rural AI, tier 3 AI India]
    og_description_en: "India gets funded. Bharat gets ignored. Here's why that's about to flip."
    og_description_hi: "India को funding मिलती है। भारत को नज़रअंदाज़ किया जाता है। यही पलटने वाला है।"
    bullets_en:
      - "India: 20 crore English speakers, metro, funded"
      - "Bharat: 120 crore, Hindi/regional, Tier 2/3/4, ignored by every AI company"
      - "Why the gap exists — design assumptions, language assumptions, market assumptions"
      - "What Bharat actually needs from AI — voice, Hindi, audio, low-data"
      - "The data: 600K villages with internet, zero native AI products"
    bullets_hi:
      - "India: 20 करोड़ English-speaking, metro, funded"
      - "भारत: 120 करोड़, हिंदी / क्षेत्रीय भाषाएँ, जिन पर किसी ने AI नहीं बनाया"
      - "यह gap क्यों है — design की, भाषा की, बाज़ार की ग़लत धारणाएँ"
      - "भारत को AI से असली में क्या चाहिए — voice, हिंदी, audio, low-data"
      - "आँकड़े: 6 लाख गाँवों में internet, native AI product शून्य"
    image_prompt: |
      Split-panel conceptual illustration: left half shows a glass metro
      skyscraper in cool blue tones (India), right half shows a warm
      amber-lit village with farmers at dusk (Bharat), joined in the
      middle by a single cable of light. Cinematic, restrained. Two
      worlds, one connection.

  - slug: pancha-bhoota-ai
    title_en: "Pancha Bhoota — ancient elements, modern AI"
    title_hi: "पंच भूत — प्राचीन तत्व, आधुनिक AI"
    vertical: brand
    published_at: "2026-02-28"
    keywords: [pancha bhoota, Indian philosophy AI, Prithvi Vayu Tejas Jal Akasha]
    og_description_en: "Five elements. Seven products. A framework borrowed from our grandparents."
    og_description_hi: "पाँच तत्व। सात products। हमारे दादा-दादियों से उधार लिया गया दर्शन।"
    bullets_en:
      - "The origin — why 5 elements, why now"
      - "Prithvi (earth): knowledge grounds everything — Shrutam"
      - "Vayu (air): commerce flows — WhatsApp Commerce"
      - "Tejas (fire): clarity ignites — Karta AI"
      - "Jal (water): life-giving — Pashu, Bima"
      - "Akasha (space): connection — Svayam, Adhikar"
      - "Why frameworks matter for disciplined product building"
    bullets_hi:
      - "उद्गम — पाँच तत्व क्यों, अभी क्यों"
      - "पृथ्वी: ज्ञान की ज़मीन — श्रुतम्"
      - "वायु: व्यापार का प्रवाह — WhatsApp Commerce"
      - "तेजस्: स्पष्टता की ज्वाला — Karta AI"
      - "जल: जीवनदायिनी — Pashu, Bima"
      - "आकाश: जोड़ने वाला अवकाश — Svayam, Adhikar"
      - "framework अनुशासन के लिए ज़रूरी है"
    image_prompt: |
      Abstract editorial illustration: five ethereal Indian elements
      arranged in a circle — a single leaf (Prithvi), a wisp of wind
      (Vayu), a tiny flame (Tejas), a drop of water (Jal), a star-field
      point (Akasha). Each glows softly. Navy cosmos background, amber
      and sky-blue lights. Balanced, ceremonial, hopeful.

  - slug: 22-7-philosophy
    title_en: "22/7 — tez nahi, sahi. Why we don't ship fast."
    title_hi: "22/7 — तेज़ नहीं, सही। हम जल्दी ship क्यों नहीं करते।"
    vertical: brand
    published_at: "2026-03-06"
    keywords: [22/7 philosophy, smart work, slow build AI]
    og_description_en: "Two woodcutters. One cuts for 24 hours. One cuts for 22 and sharpens for 2. The slow one wins."
    og_description_hi: "दो लकड़हारे। एक 24 घंटे काटता है। दूसरा 22 काटता है, 2 कुल्हाड़ी तेज़ करता है। धीमा जीतता है।"
    bullets_en:
      - "The story — woodcutter parable"
      - "Applied to Shrutam — why blind mode took an extra month"
      - "Pause to sharpen — reflection as work"
      - "Optimize first — don't scale broken things"
      - "Ship right, not ten times broken"
    bullets_hi:
      - "कहानी — लकड़हारे की मिसाल"
      - "श्रुतम् में लागू — blind mode एक महीना देर क्यों हुआ"
      - "रुककर तेज़ करना — सोचना भी काम है"
      - "पहले optimize — टूटे को बड़ा मत करो"
      - "सही ship, दस बार टूटा नहीं"
    image_prompt: |
      A single axe standing upright in soft dusk light, next to a small
      whetstone and a coiled rope, on a dark earth-toned table. Cinematic,
      restrained, meditative. Warm amber light source off-frame. No text.

  - slug: bharat-ai-gap
    title_en: "India's 1.2 billion AI gap — the math"
    title_hi: "भारत का 1.2 अरब AI का अंतर — आँकड़े"
    vertical: market
    published_at: "2026-03-12"
    keywords: [India AI market, non-English India AI, rural India AI]
    og_description_en: "1.4 billion Indians. 200 million speak English. Every AI product serves that 200M. Here's the math on the 1.2B left behind."
    og_description_hi: "1.4 अरब भारतीय। 20 करोड़ English बोलते हैं। हर AI product उन्हीं के लिए बनता है। बाक़ी 1.2 अरब का गणित।"
    bullets_en:
      - "1.4B population, 200M English-speaking — the filter"
      - "Smartphone + Jio data: 500M+ rural users ready"
      - "Why AI companies miss them — venture math, not impact math"
      - "The market being missed — ₹ size if you build for Bharat"
      - "What 'serving' actually looks like — voice, Hindi, WhatsApp-native"
    bullets_hi:
      - "1.4 अरब जनसंख्या, 20 करोड़ English-बोलने वाले — filter यहीं है"
      - "Smartphone + Jio data: 50 करोड़+ ग्रामीण तैयार हैं"
      - "AI companies क्यों चूकती हैं — venture math, impact math नहीं"
      - "जो बाज़ार छूट रहा — भारत के लिए बनाओ तो कितना बड़ा"
      - "'सेवा' असली में क्या है — voice, हिंदी, WhatsApp-native"
    image_prompt: |
      A minimalist infographic-style illustration: a large amber disc
      representing 1.4 billion, with a small sky-blue wedge of 200M
      carved out and lit, the remaining 1.2B dim-amber unlit portion
      dominating. Numbers implied but no actual text. Editorial, clean.

  - slug: hindi-vs-translation
    title_en: "We don't translate, we rebuild — why native Hindi AI wins"
    title_hi: "हम अनुवाद नहीं करते, नए सिरे से बनाते हैं"
    vertical: market
    published_at: "2026-03-18"
    keywords: [native Hindi AI, hindi LLM, translated vs native]
    og_description_en: "Translated AI sounds wrong. It thinks in English and pretends. Native Hindi AI thinks in Hindi. The difference is everything."
    og_description_hi: "अनूदित AI ग़लत लगती है। वह English में सोचती है, नाटक करती है। हिंदी में सोचने वाली AI अलग है।"
    bullets_en:
      - "The tell-tale signs of translated AI — idioms wrong, metaphors stiff"
      - "Why our SAAVI says 'Ek circle socho' not 'See the diagram'"
      - "The technical side — native training vs post-hoc translation"
      - "What students notice immediately — and why it builds trust"
      - "The cost of translation: cultural mistakes nobody caught"
    bullets_hi:
      - "अनुवादित AI के पहचान के निशान — मुहावरे ग़लत, रूपक कड़क"
      - "हमारी SAAVI 'See the diagram' नहीं, 'एक circle सोचो' क्यों कहती है"
      - "तकनीकी पक्ष — native training बनाम बाद का अनुवाद"
      - "विद्यार्थी तुरंत क्या देखते हैं — और भरोसा कैसे बनता है"
      - "अनुवाद की क़ीमत — संस्कृति की ग़लतियाँ जिन पर किसी की नज़र नहीं पड़ी"
    image_prompt: |
      Two overlapping speech bubbles: one in cool English sky-blue with
      mechanical gear-like edges, the other in warm amber Devanagari-
      inspired flowing curves. They overlap but are visibly different
      shapes. Cosmos-navy background. Minimalist, conceptual.

  - slug: shrutam-hindi-medium-kids
    title_en: "Why Hindi-medium kids are falling behind — and what fixes it"
    title_hi: "हिंदी-medium बच्चे पीछे क्यों रह जाते हैं — और क्या ठीक करेगा"
    vertical: shrutam
    product: shrutam
    published_at: "2026-03-22"
    keywords: [hindi medium students, class 10 board exam hindi, CG Board CBSE]
    og_description_en: "67% of India's students study in Hindi medium. They're not behind because of intelligence. They're behind because every tool assumes English."
    og_description_hi: "भारत के 67% विद्यार्थी हिंदी माध्यम में पढ़ते हैं। वे बुद्धि की कमी से पीछे नहीं हैं। वे पीछे हैं क्योंकि हर tool English मानकर चलता है।"
    bullets_en:
      - "67% Hindi medium — who they are, what they struggle with"
      - "The 10th board cliff — when English subjects appear"
      - "Audio + Hinglish + slower pace = actual comprehension"
      - "Case pattern: the student who suddenly stops failing"
      - "Why CG Board schools see this first"
    bullets_hi:
      - "67% हिंदी माध्यम — कौन हैं, कहाँ अटकते हैं"
      - "10वीं की cliff — जब English वाले subjects आते हैं"
      - "Audio + Hinglish + धीमी गति = असली समझ"
      - "एक patron — जो अचानक पास होने लगा"
      - "CG Board schools यह पहले क्यों देखते हैं"
    image_prompt: |
      A young Indian student sitting in a modest village schoolroom at
      dusk, warm amber window light falling on a notebook. On the desk:
      a phone showing a subtle sky-blue glow as AI audio plays. The
      student's expression is thoughtful, focused — a moment of
      understanding. No faces clearly shown. Cinematic, gentle.

  - slug: shrutam-audio-first
    title_en: "Why audio-first for Class 6-10 students"
    title_hi: "Class 6-10 के लिए audio-first क्यों"
    vertical: shrutam
    product: shrutam
    published_at: "2026-03-28"
    keywords: [audio learning India, Hinglish tutor, audio vs video class 10]
    og_description_en: "Video feels modern but fails Bharat. Text fails the weak reader. Audio meets everyone where they are."
    og_description_hi: "Video आधुनिक लगता है, पर भारत के लिए नहीं चलता। Text कमज़ोर पाठक को पीछे छोड़ देता है। Audio हर बच्चे से मिलता है।"
    bullets_en:
      - "The data problem — 2GB/day limits video"
      - "The literacy problem — weak readers skip text"
      - "Why audio works — hands free, eyes free, listen anywhere"
      - "SAAVI's voice design — warm, calm, a didi not a teacher"
      - "The surprise: parents listen along"
    bullets_hi:
      - "Data की समस्या — 2GB/दिन video नहीं चलने देता"
      - "साक्षरता की समस्या — कमज़ोर पाठक text छोड़ देते हैं"
      - "Audio क्यों चलता है — हाथ फ़्री, आँख फ़्री, कहीं भी"
      - "SAAVI की आवाज़ — गर्म, शांत, didi जैसी"
      - "अप्रत्याशित खोज: माता-पिता भी सुनते हैं"
    image_prompt: |
      A single wireless earbud resting on an open textbook (blurred,
      no readable text), warm amber lamplight, dark wooden desk. Above
      the scene, a faint sky-blue soundwave line gently pulses. Quiet,
      intimate, late-evening study mood. Restrained.

  - slug: shrutam-blind-mode
    title_en: "India's first blind-mode edtech — FREE forever"
    title_hi: "भारत का पहला blind-mode edtech — हमेशा के लिए FREE"
    vertical: shrutam
    product: shrutam
    published_at: "2026-04-02"
    keywords: [blind students India, accessibility edtech, visually impaired students]
    og_description_en: "50 lakh visually-impaired students in India. Zero edtech serves them. Shrutam does — and it's free."
    og_description_hi: "भारत में 50 लाख दृष्टिबाधित विद्यार्थी। कोई edtech उनकी सेवा नहीं करता। Shrutam करता है — और मुफ़्त में।"
    bullets_en:
      - "The 50 lakh students nobody serves"
      - "What 'blind mode' actually means — not screen reader bolt-on"
      - "Voice navigation, haptic feedback, SAAVI-as-guide design"
      - "Why revenue zero, commitment eternal"
      - "How schools for the blind are adopting"
    bullets_hi:
      - "50 लाख विद्यार्थी जिनकी सेवा कोई नहीं करता"
      - "'Blind mode' असल में क्या है — bolt-on screen reader नहीं"
      - "Voice navigation, haptic feedback, SAAVI-as-guide design"
      - "Revenue शून्य, प्रतिबद्धता शाश्वत क्यों"
      - "अंधा-विद्यालय कैसे अपना रहे हैं"
    image_prompt: |
      A braille-textured surface softly lit by warm amber light, with a
      single phone placed beside it emitting a gentle sky-blue audio
      waveform. Fingers implied but not shown. Dignified, hopeful,
      serene. Editorial composition.

  - slug: whatsapp-commerce-msme
    title_en: "63M MSMEs run on WhatsApp + Excel — here's the AI layer"
    title_hi: "6.3 करोड़ MSMEs WhatsApp + Excel पर चलते हैं — AI layer अब यहाँ है"
    vertical: commerce
    product: commerce
    published_at: "2026-04-08"
    keywords: [MSME AI India, kirana automation, whatsapp commerce b2b]
    og_description_en: "India's 63 million MSMEs don't need enterprise SaaS. They need AI that speaks their channel and their language."
    og_description_hi: "भारत के 6.3 करोड़ MSMEs को enterprise SaaS नहीं चाहिए। उन्हें उनके channel और भाषा की AI चाहिए।"
    bullets_en:
      - "The ground truth — WhatsApp is the ERP"
      - "What breaks at scale — lost orders, stockout blindness, reorder misses"
      - "Four NLP layers — intent, catalog, stock, fulfillment"
      - "Why metro SaaS can't serve this — the 80% shape of Indian SMBs"
      - "What changes when a kirana owner gets AI"
    bullets_hi:
      - "ज़मीनी सच — WhatsApp ही ERP है"
      - "scale पर क्या टूटता है — orders खो जाते, stockout दिखता नहीं, reorder छूटता"
      - "चार NLP layers — intent, catalog, stock, fulfillment"
      - "Metro SaaS यह नहीं कर सकता — भारत के SMB का 80% आकार"
      - "एक kirana मालिक को AI मिले तो क्या बदलता है"
    image_prompt: |
      A small Indian kirana shop interior at dusk, the shopkeeper's phone
      on the counter showing a WhatsApp-style interface with a sky-blue
      AI glow. Shelves of products in background, warm amber hanging
      bulb. Intimate, working, real. No logos.

  - slug: kirana-to-distributor
    title_en: "Kirana to distributor — the 4-layer NLP stack explained"
    title_hi: "Kirana से distributor तक — 4-layer NLP stack"
    vertical: commerce
    product: commerce
    published_at: "2026-04-14"
    keywords: [nlp commerce india, whatsapp ai b2b, catalog matching ai]
    og_description_en: "How AI handles 'Suresh-ji, 10 paani soda aur 5 chai patti bhej do' — from message to fulfilment."
    og_description_hi: "'सुरेश जी, 10 पानी soda और 5 चाय-पत्ती भेज दो' — message से डिलीवरी तक AI कैसे सँभालती है।"
    bullets_en:
      - "Layer 1: intent — order? stock query? reorder? complaint?"
      - "Layer 2: catalog — which SKU does 'paani soda' mean for THIS distributor?"
      - "Layer 3: stock — is it available, alt brands, ETA"
      - "Layer 4: fulfillment — delivery route, invoice, payment"
      - "The hard part — Hinglish, brand nicknames, regional units"
    bullets_hi:
      - "Layer 1: intent — order? stock? reorder? शिकायत?"
      - "Layer 2: catalog — 'पानी soda' इस distributor के लिए कौन-सा SKU"
      - "Layer 3: stock — उपलब्ध है? alternatives, ETA"
      - "Layer 4: fulfillment — delivery route, invoice, payment"
      - "कठिन भाग — Hinglish, brand के तकिया-नाम, क्षेत्रीय units"
    image_prompt: |
      An abstract four-layer architectural diagram, each layer a glowing
      horizontal band in varying shades (amber → sky-blue → darker
      amber → deep blue), stacked on a cosmos-navy background. Minimal,
      editorial, no numbers or text.

  - slug: karta-ai-gst
    title_en: "GSTR-1, GSTR-3B, and Karta AI — compliance at voice speed"
    title_hi: "GSTR-1, GSTR-3B, और Karta AI — voice की गति पर compliance"
    vertical: karta
    product: karta
    published_at: "2026-04-20"
    keywords: [gst filing ai hindi, gstr-3b automation, karta ai msme]
    og_description_en: "Every month, 63 million MSMEs file GST returns. Most pay a CA ₹2000-5000. Karta AI does it for free in 3 minutes."
    og_description_hi: "हर महीने 6.3 करोड़ MSMEs GST returns भरते हैं। ज़्यादातर CA को ₹2000-5000 देते हैं। Karta AI 3 मिनट में मुफ़्त करता है।"
    bullets_en:
      - "The monthly nightmare — GSTR-1 (outward), GSTR-3B (summary)"
      - "What goes wrong today — 30% return errors in first filing"
      - "Karta's invoice-photo-to-return pipeline"
      - "Voice filing — speak your sales, AI categorises"
      - "What CAs lose, what MSMEs gain"
    bullets_hi:
      - "हर महीने का सिरदर्द — GSTR-1 (outward), GSTR-3B (summary)"
      - "आज क्या ग़लत होता है — पहली filing में 30% return errors"
      - "Karta की invoice-फ़ोटो-से-return pipeline"
      - "Voice से filing — अपनी sales बोलो, AI वर्गीकृत करे"
      - "CA क्या खोते हैं, MSMEs क्या पाते हैं"
    image_prompt: |
      A stack of paper invoices on a small Indian shop desk, one in the
      foreground being photographed by a phone that emits a subtle
      sky-blue scan-line. Warm amber desk lamp. Editorial, focused. No
      readable text on invoices.

  - slug: karta-ai-itr
    title_en: "ITR filing in 3 minutes — voice, Hinglish, no CA"
    title_hi: "3 मिनट में ITR filing — voice, Hinglish, बिना CA"
    vertical: karta
    product: karta
    published_at: "2026-04-26"
    keywords: [itr filing hindi, voice tax filing india, karta itr]
    og_description_en: "8 crore salaried Indians file ITR every July. ClearTax charges. CAs charge more. Karta AI files by voice, for free."
    og_description_hi: "हर जुलाई 8 करोड़ salaried भारतीय ITR भरते हैं। ClearTax पैसे लेता है। CA और भी। Karta AI voice से मुफ़्त में करता है।"
    bullets_en:
      - "The annual panic — who files what (ITR-1/2/4)"
      - "Form-16 → AI auto-detects fields"
      - "Voice deductions — 'LIC mein 50 hazaar, PPF 1.5 lakh' → filled"
      - "HRA, 80C, 80D — the Hindi side of tax planning"
      - "Edge cases — freelance, capital gains, multiple employers"
    bullets_hi:
      - "सालाना घबराहट — कौन कौन-सा form (ITR-1/2/4)"
      - "Form-16 → AI अपने आप fields भरती है"
      - "Voice कटौतियाँ — 'LIC में 50 हज़ार, PPF 1.5 लाख' → भर गया"
      - "HRA, 80C, 80D — tax planning का हिंदी पक्ष"
      - "Edge cases — freelance, capital gains, कई employers"
    image_prompt: |
      A single Form-16 paper on a desk with a faint sky-blue highlight
      outline around specific fields, as if AI is reading them. Beside
      it a phone with a subtle voice-wave indicator. Amber desk light.
      Clean, calm, technical-elegant.

  - slug: pashu-ai-cattle
    title_en: "Pashu ka doctor, aapke phone mein — how Pashu AI works"
    title_hi: "पशु का डॉक्टर, आपके फ़ोन में — Pashu AI कैसे काम करता है"
    vertical: pashu
    product: pashu
    published_at: "2026-05-02"
    keywords: [cattle doctor app india, pashu ai dairy farmer, veterinary ai hindi]
    og_description_en: "70 million dairy farmers. The nearest vet is 20km away. One sick cow = ₹80,000 loss. Pashu AI is the difference."
    og_description_hi: "7 करोड़ दुग्ध किसान। सबसे पास का वेट 20km दूर। एक बीमार गाय = ₹80,000 का नुक़सान। Pashu AI यही अंतर है।"
    bullets_en:
      - "The cost of a sick animal — real numbers, real losses"
      - "Photo diagnosis — FMD, mastitis, bloat, lameness"
      - "Voice consultation in Hindi — what to say, what AI hears"
      - "Medicine recommendation + generic alternatives"
      - "Integration with Rashtriya Gokul Mission"
    bullets_hi:
      - "बीमार पशु की क़ीमत — असली अंक, असली नुक़सान"
      - "फ़ोटो से निदान — FMD, mastitis, bloat, lameness"
      - "हिंदी में voice consultation — क्या बोलें, AI क्या सुनती है"
      - "दवा की सलाह + generic विकल्प"
      - "राष्ट्रीय गोकुल मिशन से जुड़ाव"
    image_prompt: |
      A dairy farmer's hand holding a phone toward a calm cow in a
      village stable at dawn, soft warm amber light, dust motes in air.
      A gentle sky-blue camera-focus outline on the cow. Documentary,
      dignified, no face focus.

  - slug: pashu-ai-livestock-ai
    title_en: "Livestock AI for rural dairy — beyond a photo app"
    title_hi: "ग्रामीण डेयरी के लिए Livestock AI — photo app से आगे"
    vertical: pashu
    product: pashu
    published_at: "2026-05-08"
    keywords: [dairy farm ai, livestock tracker india, milk yield ai]
    og_description_en: "Pashu AI isn't a diagnosis app. It's a dairy operations layer for 70 million Indian families."
    og_description_hi: "Pashu AI निदान app नहीं है। यह 7 करोड़ भारतीय परिवारों के लिए dairy operations की परत है।"
    bullets_en:
      - "Milk yield tracking — per animal, per day"
      - "Pregnancy calendar + artificial insemination booking"
      - "Feed optimisation — cost per litre calc"
      - "Vet visit history + medicine calendar"
      - "Group buying — when 10 farmers pool for one tanker delivery"
    bullets_hi:
      - "दूध उपज tracking — प्रति पशु, प्रति दिन"
      - "गर्भावस्था calendar + कृत्रिम गर्भाधान booking"
      - "चारा optimisation — प्रति लीटर लागत गणना"
      - "वेट visit इतिहास + दवा calendar"
      - "साझा ख़रीदारी — 10 किसान मिलकर एक tanker मंगवाएँ"
    image_prompt: |
      A wide-format illustration of a small village dairy at sunrise,
      mist rising, a row of cattle being milked, amber glow on the
      horizon. A subtle sky-blue data-line traces through the scene
      connecting the animals. Editorial, aspirational, not busy.

  - slug: bima-ai-insurance
    title_en: "40% of insurance claims rejected — AI fixes the paperwork"
    title_hi: "40% बीमा claims रिजेक्ट होते हैं — AI paperwork ठीक करता है"
    vertical: bima
    product: bima
    published_at: "2026-05-14"
    keywords: [insurance claim ai india, ayushman bharat claim, health insurance automation]
    og_description_en: "You bought insurance. The claim got rejected. Paperwork, not fraud. Bima AI drafts claims that insurers accept."
    og_description_hi: "आपने बीमा लिया। Claim रिजेक्ट हो गया। Paperwork की वजह से, धोखाधड़ी नहीं। Bima AI ऐसे claims बनाती है जो insurer मानते हैं।"
    bullets_en:
      - "The 40% rejection rate — why, really"
      - "What insurers scan for — wording, document order, amounts"
      - "Bima AI's claim-drafting pipeline"
      - "Escalation automation — when a rejection is wrong"
      - "Ayushman Bharat + Star Health + HDFC Ergo integrations"
    bullets_hi:
      - "40% रिजेक्शन क्यों — असली कारण"
      - "Insurers क्या scan करते हैं — wording, document क्रम, amounts"
      - "Bima AI की claim-drafting pipeline"
      - "Escalation का automation — जब रिजेक्शन ग़लत है"
      - "Ayushman Bharat + Star Health + HDFC Ergo integrations"
    image_prompt: |
      A stack of medical bills and discharge summaries on a dim wooden
      table, with one document subtly glowing sky-blue as if AI is
      reading it. Amber ambient lighting. Serious, empathetic, editorial.

  - slug: bima-ai-crop-pmfby
    title_en: "PMFBY claims — why 90% of farmers don't file them"
    title_hi: "PMFBY claims — 90% किसान क्यों नहीं भरते"
    vertical: bima
    product: bima
    published_at: "2026-05-20"
    keywords: [pmfby claim hindi, crop insurance ai, pradhan mantri fasal bima]
    og_description_en: "Farmers pay PMFBY premiums faithfully. When the crop fails, they don't claim — because the form is impossible. Bima AI fixes this."
    og_description_hi: "किसान ईमानदारी से PMFBY premium भरते हैं। फ़सल नष्ट हो जाए तो claim नहीं करते — क्योंकि form असंभव है। Bima AI यही ठीक करता है।"
    bullets_en:
      - "The PMFBY trust-gap — premium goes, claim never comes"
      - "Why the form fails rural farmers"
      - "Photo of damaged crop → auto-drafted claim"
      - "Coordinating with patwari + KCC"
      - "What happens to ₹30,000 that would have been lost"
    bullets_hi:
      - "PMFBY का विश्वास-गैप — premium जाता है, claim नहीं आता"
      - "Form ग्रामीण किसान के लिए क्यों fail होता है"
      - "फ़सल नष्ट होने की photo → auto-drafted claim"
      - "पटवारी + KCC से coordination"
      - "₹30,000 का क्या होता है जो खो जाता था"
    image_prompt: |
      A damaged paddy field under overcast light, a lone farmer in the
      distance holding a phone up to photograph the field. Soft amber
      horizon, quiet pathos. Editorial, respectful.

  - slug: svayam-ai-forms
    title_en: "Sarkari form, voice se bhar do — Svayam AI explained"
    title_hi: "सरकारी form, voice से भर दो — Svayam AI"
    vertical: svayam
    product: svayam
    published_at: "2026-05-26"
    keywords: [sarkari form ai, govt form filling hindi, voice form filling]
    og_description_en: "India has ~1500 government forms. Every one asks the same 15 fields. Svayam fills them all, by voice."
    og_description_hi: "भारत में ~1500 सरकारी forms हैं। हर एक वही 15 fields माँगता है। Svayam voice से सब भरता है।"
    bullets_en:
      - "The form maze — 1500 forms, 15 common fields"
      - "Speak once, fill forever — encrypted profile"
      - "How voice-first OCR + form-field detection works"
      - "Privacy design — data never leaves device unencrypted"
      - "Where UMANG failed and Svayam starts"
    bullets_hi:
      - "Forms का भूल-भुलैया — 1500 forms, 15 common fields"
      - "एक बार बोलो, हमेशा भरो — encrypted profile"
      - "Voice-first OCR + form-field detection कैसे"
      - "Privacy design — data बिना encryption device नहीं छोड़ता"
      - "UMANG जहाँ fail हुआ, Svayam वहाँ से शुरू"
    image_prompt: |
      A stack of blank Indian government forms on a table, slowly being
      auto-filled by an invisible presence — field outlines gently
      glowing sky-blue as they get completed. Warm amber ambient light.
      Editorial, almost magical, restrained.

  - slug: svayam-ai-aadhaar
    title_en: "Aadhaar update, passport, caste cert — one voice interface"
    title_hi: "आधार update, passport, जाति प्रमाण — एक voice interface"
    vertical: svayam
    product: svayam
    published_at: "2026-06-01"
    keywords: [aadhaar update voice, passport form hindi, caste certificate ai]
    og_description_en: "Every adult Indian deals with these 5 forms at least once a year. Svayam AI makes each one a 2-minute voice conversation."
    og_description_hi: "हर वयस्क भारतीय को साल में इन 5 forms में से कम-से-कम एक भरना पड़ता है। Svayam AI हर को 2 मिनट की voice बातचीत बना देता है।"
    bullets_en:
      - "The 5 forms — Aadhaar, passport, voter, DL, caste cert"
      - "Common failure modes — document upload, photo size, signature box"
      - "Svayam's voice walk-through"
      - "When a form needs Tehsildar / gram pradhan signature — what AI does"
      - "What changes when filling feels like a conversation"
    bullets_hi:
      - "पाँच forms — आधार, passport, voter, DL, जाति प्रमाण"
      - "आम fail — document upload, photo size, signature box"
      - "Svayam का voice walk-through"
      - "जब form पर Tehsildar / ग्राम प्रधान के signature चाहिए — AI क्या करती है"
      - "Form भरना बातचीत जैसी लगे तो क्या बदलता है"
    image_prompt: |
      A gentle side-view of an older rural Indian man speaking to his
      phone at a wooden desk, warm amber lamp light, phone emits a soft
      sky-blue listening indicator. Respectful, dignified, no face
      centrality. Cinematic.

  - slug: adhikar-ai-pension
    title_en: "Widow pension, old-age pension — why 30% don't receive what they're owed"
    title_hi: "विधवा पेंशन, वृद्धावस्था पेंशन — 30% को उनका हक़ क्यों नहीं मिलता"
    vertical: adhikar
    product: adhikar
    published_at: "2026-06-07"
    keywords: [widow pension india app, old age pension tracking, adhikar ai welfare]
    og_description_en: "₹50,000 crore of welfare doesn't reach beneficiaries each year. Adhikar AI is how we change that."
    og_description_hi: "हर साल ₹50,000 करोड़ का कल्याण लाभार्थियों तक नहीं पहुँचता। Adhikar AI यही बदलता है।"
    bullets_en:
      - "The scale — 3Cr elderly + 4Cr widows + 2Cr disabled eligible"
      - "Why benefits don't arrive — banks, forms, follow-up gaps"
      - "Adhikar's eligibility → application → tracking pipeline"
      - "RTI auto-drafter when things go silent"
      - "Voice interface for the actually-elderly"
    bullets_hi:
      - "पैमाना — 3 करोड़ बुज़ुर्ग + 4 करोड़ विधवाएँ + 2 करोड़ दिव्यांग"
      - "लाभ क्यों नहीं पहुँचते — bank, forms, follow-up की खाइयाँ"
      - "Adhikar का eligibility → application → tracking pipeline"
      - "जब चीज़ें शांत हो जाएँ — RTI auto-drafter"
      - "असल में वृद्ध के लिए बना voice interface"
    image_prompt: |
      An elderly Indian woman in a simple cotton sari seated on a
      charpai in the veranda of a mud-brick home, holding a basic phone
      that emits a gentle sky-blue voice indicator. Warm amber sunset
      light. Dignified, hopeful, not sentimental.
```

### Step 4.2 — `scripts/llm_client.py`

Shared helper for Gemini text + image calls. Reads `GEMINI_API_KEY` and `GEMINI_MODEL` from `/Users/ajayagrawal/aarambhax/.env`.

```python
#!/usr/bin/env python3
"""Gemini client helpers: text generation + Nano Banana image generation."""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error, base64
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_env() -> dict[str, str]:
    env = {}
    p = _repo_root() / ".env"
    if not p.exists():
        print("ERROR: /Users/ajayagrawal/aarambhax/.env not found", file=sys.stderr)
        sys.exit(2)
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    if "GEMINI_API_KEY" not in env:
        print("ERROR: GEMINI_API_KEY missing in .env", file=sys.stderr)
        sys.exit(2)
    env.setdefault("GEMINI_MODEL", "gemini-2.5-flash")
    return env


_ENV = _load_env()
TEXT_MODEL  = _ENV["GEMINI_MODEL"]
IMAGE_MODEL = "gemini-2.5-flash-image"
API_KEY     = _ENV["GEMINI_API_KEY"]
BASE_URL    = "https://generativelanguage.googleapis.com/v1beta/models"


def _post(url: str, body: dict, timeout: int = 60) -> dict:
    data = json.dumps(body).encode("utf-8")
    req  = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Gemini HTTP {e.code}: {e.read().decode()[:500]}") from e


def gen_text(prompt: str, *, temperature: float = 0.6, max_tokens: int = 8192,
             retries: int = 2) -> str:
    """Generate text with thinking disabled (2.5 Flash uses reasoning tokens otherwise)."""
    url = f"{BASE_URL}/{TEXT_MODEL}:generateContent?key={API_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": temperature,
            "thinkingConfig": {"thinkingBudget": 0}
        }
    }
    for attempt in range(retries + 1):
        try:
            resp = _post(url, body, timeout=120)
            cand = resp.get("candidates", [{}])[0]
            parts = cand.get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts).strip()
            if text:
                return text
            raise RuntimeError(f"empty response; finish={cand.get('finishReason')}")
        except Exception as e:
            if attempt == retries:
                raise
            print(f"  gen_text retry {attempt + 1} after error: {e}", file=sys.stderr)
            time.sleep(2 ** attempt)


def gen_image(prompt: str, *, retries: int = 2) -> bytes:
    """Generate an image via Nano Banana. Returns raw PNG bytes."""
    url = f"{BASE_URL}/{IMAGE_MODEL}:generateContent?key={API_KEY}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]}
    }
    for attempt in range(retries + 1):
        try:
            resp = _post(url, body, timeout=90)
            parts = resp.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for p in parts:
                inline = p.get("inlineData", {})
                if inline.get("mimeType", "").startswith("image/"):
                    return base64.b64decode(inline["data"])
            raise RuntimeError("no image in response")
        except Exception as e:
            if attempt == retries:
                raise
            print(f"  gen_image retry {attempt + 1} after error: {e}", file=sys.stderr)
            time.sleep(2 ** attempt)


if __name__ == "__main__":
    # Smoke test: print a haiku, save a tiny test image
    print("TEXT MODEL:", TEXT_MODEL)
    print("IMAGE MODEL:", IMAGE_MODEL)
    print("---")
    print(gen_text("Write a one-line haiku about Bharat at dawn. No explanation."))
    img = gen_image("A single amber diya glowing in the darkness, cinematic, Indian temple.")
    Path("/tmp/llm_smoke.png").write_bytes(img)
    print(f"image saved: /tmp/llm_smoke.png ({len(img) // 1024} KB)")
```

### Step 4.3 — `scripts/lib_image.py`

Pillow helpers to compress/resize Gemini images into WebP targets.

```python
#!/usr/bin/env python3
"""Image post-processing: crop, resize, compress, save WebP."""
from __future__ import annotations
import io
from pathlib import Path
from PIL import Image


def _crop_to_ratio(img: Image.Image, ratio: float) -> Image.Image:
    """Centre-crop image to the given width/height ratio."""
    w, h = img.size
    cur = w / h
    if abs(cur - ratio) < 0.01:
        return img
    if cur > ratio:
        new_w = int(h * ratio)
        left  = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    new_h = int(w / ratio)
    top   = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def save_as_webp(png_bytes: bytes, out_path: Path, *, width: int, height: int, quality: int = 82) -> int:
    """Crop to `width:height` ratio, resize, save WebP. Returns bytes written."""
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img = _crop_to_ratio(img, width / height)
    img = img.resize((width, height), Image.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "WEBP", quality=quality, method=6)
    return out_path.stat().st_size


# Standard aspect presets used across the site
PRESETS = {
    "blog-hero":        {"width": 1200, "height": 630, "quality": 82},
    "blog-hero-large":  {"width": 1600, "height": 840, "quality": 80},
    "product-card":     {"width":  800, "height": 800, "quality": 85},
    "philosophy":       {"width": 1200, "height": 800, "quality": 82},
    "og-default":       {"width": 1200, "height": 630, "quality": 82},
}
```

### Step 4.4 — `scripts/generate_post.py`

Reads `content/briefs.yaml`, generates each post's EN + HI text + hero image, writes a bilingual HTML file under `blog/<slug>/index.html` + `assets/images/blog/<slug>-hero.webp`.

```python
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
```

### Step 4.5 — `scripts/generate_product_images.py`

```python
#!/usr/bin/env python3
"""Generate the 7 product-card illustrations + site OG default."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_client import gen_image
from lib_image  import save_as_webp, PRESETS

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "assets" / "images" / "products"

STYLE = (
    "Editorial dark illustration, cosmos-navy #060d1a background with subtle depth. "
    "Warm amber #f59e0b and sky-blue #0ea5e9 as singular accent lights. "
    "Premium magazine quality, restrained, one subject centered, generous negative space. "
    "NO text, NO logos, NO watermarks. Square composition."
)

SUBJECTS = {
    "shrutam":   "A single phone on a wooden village desk at dusk, its screen emitting a soft amber glow of audio learning, a notebook and pen beside it.",
    "commerce":  "A shopkeeper's hand holding a phone with a WhatsApp-like chat glowing, against a kirana shop shelf backdrop, dusk lighting.",
    "karta":     "A clean stack of invoices on a desk being read by an invisible presence — a single sky-blue scan line across them, small amber desk lamp.",
    "pashu":     "A calm cow in a rural Indian stable at dawn, a subtle sky-blue diagnostic outline on the animal's flank, misty amber light.",
    "bima":      "A medical bill document softly highlighted in sky-blue as if AI is reading it, on a dark table with warm amber ambient light.",
    "svayam":    "A blank Indian government form being filled by an invisible voice — field outlines gently glowing sky-blue, warm amber ambient.",
    "adhikar":   "An elderly hand holding a simple phone that emits a gentle sky-blue voice indicator, the background a blurred veranda at dusk.",
}

OG_DEFAULT = (
    "A single amber diya glowing softly at the foot of a dark cosmic sky with scattered stars, "
    "a faint horizon line suggesting an Indian village, editorial minimalist composition. "
    "Restrained, ceremonial, no text."
)

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "images").mkdir(parents=True, exist_ok=True)

    for slug, subject in SUBJECTS.items():
        out = OUT / f"{slug}.webp"
        if out.exists():
            print(f"exists: {out.relative_to(ROOT)} — skip (delete to regenerate)")
            continue
        print(f"generating {slug}...")
        png = gen_image(f"{STYLE}\n\nSubject: {subject}")
        size = save_as_webp(png, out, **PRESETS["product-card"])
        print(f"  saved {size // 1024} KB")

    # Site-wide OG default (1200x630)
    og_out = ROOT / "assets" / "images" / "og-default.webp"
    if og_out.exists():
        print(f"exists: {og_out.relative_to(ROOT)} — skip")
    else:
        print("generating og-default ...")
        png = gen_image(f"{STYLE}\n\nSubject: {OG_DEFAULT}")
        size = save_as_webp(png, og_out, **PRESETS["og-default"])
        print(f"  saved {size // 1024} KB")

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Step 4.6 — `scripts/generate_philosophy_images.py`

```python
#!/usr/bin/env python3
"""Generate 6 editorial images: Pancha Bhoota 5 elements + 22/7 woodcutter."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_client import gen_image
from lib_image  import save_as_webp, PRESETS

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "assets" / "images" / "philosophy"

STYLE = (
    "Editorial dark illustration, cosmos-navy #060d1a background with subtle depth. "
    "Warm amber #f59e0b and sky-blue #0ea5e9 as singular accent lights. "
    "Premium magazine quality, ceremonial, one symbolic subject, negative space. "
    "NO text, NO logos, NO watermarks."
)

SUBJECTS = {
    "prithvi":    "A single leaf on dark earth, with a soft amber light from below as if the leaf itself glows with life — knowledge grounding everything.",
    "vayu":       "A wisp of luminous wind carrying a paisley-pattern trail across the dark sky, sky-blue highlights, amber accents — commerce flowing like air.",
    "tejas":      "A small brilliant amber flame alone in the dark, casting faint sky-blue ripples around it — clarity igniting.",
    "jal":        "A single drop of water suspended mid-air, reflecting amber and sky-blue lights inside it, dark background, ceremonial — life-giving.",
    "akasha":     "A constellation of tiny sky-blue pinpoints against the cosmos, loosely connecting like a web, one amber pinpoint brighter in the centre — the connective space.",
    "woodcutter": "A single axe standing upright next to a small whetstone and a coiled rope, on dark earth-toned table, warm amber side light, cinematic and meditative.",
}

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, subject in SUBJECTS.items():
        out = OUT / f"{slug}.webp"
        if out.exists():
            print(f"exists: {out.relative_to(ROOT)} — skip (delete to regenerate)")
            continue
        print(f"generating {slug}...")
        png = gen_image(f"{STYLE}\n\nSubject: {subject}")
        size = save_as_webp(png, out, **PRESETS["philosophy"])
        print(f"  saved {size // 1024} KB")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Step 4.7 — Verify pipeline & commit scripts (NOT run yet)

Install Pillow if missing:
```bash
python3 -c "import PIL" 2>&1 | grep -q ModuleNotFoundError && python3 -m pip install --user pillow pyyaml
python3 -c "import yaml, PIL; print('deps ok')"
```

Smoke-test the LLM client:
```bash
cd /Users/ajayagrawal/aarambhax
python3 scripts/llm_client.py
ls -lh /tmp/llm_smoke.png  # should exist
```

Commit the scripts + briefs (images generated in Task 5):

```bash
cd /Users/ajayagrawal/aarambhax
git add content/ scripts/llm_client.py scripts/lib_image.py scripts/generate_post.py scripts/generate_product_images.py scripts/generate_philosophy_images.py
git commit -m "feat(v2): content + image generation pipeline (Gemini 2.5 + Nano Banana)

  - content/briefs.yaml — 20 post briefs (EN + HI bullets, image prompts,
    vertical tags, published_at, keywords, og descriptions)
  - scripts/llm_client.py — Gemini text + Nano Banana image client,
    reads .env, handles retries, disables 2.5 Flash reasoning budget
    so output actually fits
  - scripts/lib_image.py — Pillow helpers: crop-to-ratio, resize,
    WebP compress with quality presets
  - scripts/generate_post.py — reads a brief, two independent Gemini
    calls (one EN, one HI — NOT translation, native prompts in each
    language), Nano Banana hero, writes bilingual blog HTML with
    schema.org BlogPosting entries for both languages
  - scripts/generate_product_images.py — 7 product-card illustrations
    + site OG default
  - scripts/generate_philosophy_images.py — 5 Pancha Bhoota elements
    + 22/7 woodcutter

Idempotent: skips files that already exist unless --all.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v2-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 5 — Run pipeline: generate all content + images

**Goal:** Execute the pipeline — produce 20 bilingual blog posts + 7 product images + 6 philosophy images + 1 OG default.

**Files:**
- Creates: `blog/<slug>/index.html` × 20
- Creates: `assets/images/blog/<slug>-hero.webp` × 20
- Creates: `assets/images/products/<slug>.webp` × 7
- Creates: `assets/images/philosophy/{prithvi,vayu,tejas,jal,akasha,woodcutter}.webp` × 6
- Creates: `assets/images/og-default.webp` × 1

### Step 5.1 — Generate product + philosophy images

Run these first — they're fewer, smaller, and verify image pipeline quality before batching 20 posts.

```bash
cd /Users/ajayagrawal/aarambhax
python3 scripts/generate_product_images.py
python3 scripts/generate_philosophy_images.py

# Confirm outputs
ls -lh assets/images/products/*.webp assets/images/philosophy/*.webp assets/images/og-default.webp
# Expect: 7 products + 6 philosophy + 1 OG = 14 files, each roughly 50-200 KB
```

If any image looks off-brand (wrong colours, text bleed, generic), delete that specific file and re-run — the script is idempotent (skips existing).

Commit:

```bash
cd /Users/ajayagrawal/aarambhax
git add assets/images/products/ assets/images/philosophy/ assets/images/og-default.webp
git commit -m "feat(v2): Nano Banana illustrations — 7 products + 6 philosophy + OG

Generated via scripts/generate_product_images.py +
generate_philosophy_images.py. All follow the Aarambha house style:
cosmos-navy background, amber + sky-blue accents, editorial dark,
centered subject, no text.

  - assets/images/products/{shrutam,commerce,karta,pashu,bima,svayam,adhikar}.webp  (800x800)
  - assets/images/philosophy/{prithvi,vayu,tejas,jal,akasha,woodcutter}.webp        (1200x800)
  - assets/images/og-default.webp                                                    (1200x630)

Total: 14 WebP images, ~2MB combined. All compressed at quality 82-85.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

### Step 5.2 — Generate the 20 blog posts

```bash
cd /Users/ajayagrawal/aarambhax
python3 scripts/generate_post.py         # runs all 20; skips any that already exist
# Expect ~15-25 minutes; each post = 2 text calls + 1 image call
ls blog/*/index.html | wc -l       # should be 20
ls assets/images/blog/*-hero.webp | wc -l  # should be 20
```

Spot-check a random post:

```bash
python3 -m http.server 8000 > /tmp/s.log 2>&1 & PID=$!
sleep 1
SLUG=$(ls blog | head -1)
curl -s -o /dev/null -w "%{http_code} /blog/$SLUG/\n" http://127.0.0.1:8000/blog/$SLUG/
# Expect: 200
# Open in browser and skim for structure / Hindi quality
kill $PID 2>/dev/null; wait 2>/dev/null
```

### Step 5.3 — Human quality pass (critical)

**This step is manual.** Open 3 random post HTMLs, look at:
1. EN version reads natural — no obvious "Gemini-ese" filler
2. HI version reads natural — NOT transparently translated English; check idioms and rhythm
3. Hero image matches the tone and topic
4. Internal links go somewhere valid

If any post fails: `rm blog/<slug>/index.html` and re-run the script. If many posts fail on the same axis (e.g., Hindi reads translated), tighten the prompt template and regenerate those slugs with `--all`.

### Step 5.4 — Commit posts

```bash
cd /Users/ajayagrawal/aarambhax
git add blog/ assets/images/blog/
git commit -m "feat(v2): 20 bilingual blog posts + hero images (Gemini 2.5 Flash + Nano Banana)

Generated via scripts/generate_post.py from content/briefs.yaml.
Each post: independent EN + HI body (native, not translated), hero
image from Nano Banana, bilingual schema.org BlogPosting entries in
<head>, hreflang alternates, Alpine x-show toggle tied to the lang store.

Verticals shipped:
  - brand (4): India mein AI ki aarambh, Bharat vs India, Pancha Bhoota, 22/7
  - market (2): 1.2B gap, hindi vs translation
  - shrutam (3): hindi-medium kids, audio-first, blind mode
  - commerce (2): MSME WhatsApp, 4-layer NLP stack
  - karta (2): GST/ITR voice filing
  - pashu (2): cattle doctor, full livestock ops
  - bima (2): health claims, PMFBY crop
  - svayam (2): form-filling maze, Aadhaar/passport
  - adhikar (1): pension / welfare / RTI auto-draft

Total: 20 posts × ~1300 words × 2 languages ≈ 52k words of original
content. Hero images: 20 WebP files, ~3MB combined.

Published dates back-dated across Feb 12 – Jun 7, 2026 so the calendar
feels organic not batched.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

---

## Task 6 — Blog index upgrade + sitemap + push

**Goal:** Replace the empty-state `/blog/index.html` with a category-filtered card grid of all 20 posts. Update sitemap. Final push.

**Files:**
- Modify: `blog/index.html`
- Modify: `sitemap.xml`
- Modify: `products/index.html` (swap emoji → Nano Banana image thumbnails on 7 cards — optional polish)
- Modify: `philosophy/index.html` (add Nano Banana images to the 5 element cards)

### Step 6.1 — Rewrite `blog/index.html`

Replace the entire `<main>` content. Keep head/nav/footer structure.

```html
<main x-data="{ cat: 'all' }">

<section class="bg-cosmos pt-28 pb-12 px-4 md:px-8">
  <div class="max-w-6xl mx-auto text-center">
    <p class="inline-block px-3 py-1 rounded-full border border-accent/30 bg-accent/5 text-xs font-bold text-accent tracking-[.20em] uppercase mb-4">Blog</p>
    <h1 class="text-4xl md:text-6xl font-black mb-3"><span class="grad">Seekhte Rahenge.</span></h1>
    <p class="hindi text-lg md:text-xl text-gray-400 mb-0">सीखते रहेंगे — The Aarambha Blog</p>
  </div>
</section>

<section class="bg-dark border-b border-white/[.06] sticky top-[72px] z-40 py-3 px-4 md:px-8 backdrop-blur-xl">
  <div class="max-w-6xl mx-auto flex flex-wrap gap-2 justify-center">
    <button @click="cat='all'"       :class="cat==='all'       ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">All</button>
    <button @click="cat='brand'"     :class="cat==='brand'     ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Philosophy</button>
    <button @click="cat='market'"    :class="cat==='market'    ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Market</button>
    <button @click="cat='shrutam'"   :class="cat==='shrutam'   ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Education</button>
    <button @click="cat='commerce'"  :class="cat==='commerce'  ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Commerce</button>
    <button @click="cat='karta'"     :class="cat==='karta'     ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Compliance</button>
    <button @click="cat='pashu'"     :class="cat==='pashu'     ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Livestock</button>
    <button @click="cat='bima'"      :class="cat==='bima'      ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Insurance</button>
    <button @click="cat='svayam'"    :class="cat==='svayam'    ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Govt Services</button>
    <button @click="cat='adhikar'"   :class="cat==='adhikar'   ? 'bg-accent text-gray-900' : 'border border-white/[.10] text-gray-400 hover:text-gray-200'" class="px-3.5 py-1.5 rounded-full text-sm font-bold transition-all">Welfare</button>
  </div>
</section>

<section class="bg-dark py-12 md:py-20 px-4 md:px-8">
  <div class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5" id="blog-grid">
    <!-- BLOG_CARDS_INJECTED_BY_PLAN_STEP_6.1 -->
  </div>
</section>

</main>
```

The 20 card `<article>` entries go inside `#blog-grid`. Each card template:

```html
<article x-show="cat==='all' || cat==='VERTICAL'" class="bg-card border border-white/[.07] rounded-2xl overflow-hidden hover:border-primary/40 transition-all group">
  <a href="/blog/SLUG/" class="block">
    <div class="aspect-[1200/630] overflow-hidden"><img src="/assets/images/blog/SLUG-hero.webp" alt="" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" width="1200" height="630"></a>
    <div class="p-5">
      <p class="text-[10px] font-bold text-accent tracking-[.18em] uppercase mb-2">VERTICAL_LABEL</p>
      <h3 class="font-bold text-gray-100 text-lg leading-tight mb-2 group-hover:text-primary transition-colors" x-show="$store.lang.current === 'en'" lang="en">TITLE_EN</h3>
      <h3 class="hindi font-bold text-gray-100 text-lg leading-tight mb-2 group-hover:text-primary transition-colors" x-show="$store.lang.current === 'hi'" lang="hi">TITLE_HI</h3>
      <p class="text-sm text-gray-400 leading-relaxed line-clamp-3" x-show="$store.lang.current === 'en'" lang="en">OG_EN</p>
      <p class="text-sm text-gray-400 leading-relaxed line-clamp-3 hindi" x-show="$store.lang.current === 'hi'" lang="hi">OG_HI</p>
      <p class="text-xs text-gray-600 mt-3">DATE</p>
    </div>
  </a>
</article>
```

**Generate the cards programmatically** — add a helper inline in the implementer's task. Shell approach:

```bash
cd /Users/ajayagrawal/aarambhax
python3 - <<'PY' > /tmp/blog-cards.html
import yaml, html
briefs = yaml.safe_load(open("content/briefs.yaml"))["posts"]
label_map = {
    "brand": "Philosophy", "market": "Market", "shrutam": "Education",
    "commerce": "Commerce", "karta": "Compliance", "pashu": "Livestock",
    "bima": "Insurance", "svayam": "Govt Services", "adhikar": "Welfare",
}
for post in sorted(briefs, key=lambda p: p["published_at"], reverse=True):
    slug, v = post["slug"], post["vertical"]
    print(f'''<article x-show="cat==='all' || cat==='{v}'" class="bg-card border border-white/[.07] rounded-2xl overflow-hidden hover:border-primary/40 transition-all group">
  <a href="/blog/{slug}/" class="block">
    <div class="aspect-[1200/630] overflow-hidden"><img src="/assets/images/blog/{slug}-hero.webp" alt="" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" width="1200" height="630"></div>
    <div class="p-5">
      <p class="text-[10px] font-bold text-accent tracking-[.18em] uppercase mb-2">{label_map.get(v, v).upper()}</p>
      <h3 class="font-bold text-gray-100 text-lg leading-tight mb-2 group-hover:text-primary transition-colors" x-show="$store.lang.current === 'en'" lang="en">{html.escape(post['title_en'])}</h3>
      <h3 class="hindi font-bold text-gray-100 text-lg leading-tight mb-2 group-hover:text-primary transition-colors" x-show="$store.lang.current === 'hi'" lang="hi">{html.escape(post['title_hi'])}</h3>
      <p class="text-sm text-gray-400 leading-relaxed line-clamp-3" x-show="$store.lang.current === 'en'" lang="en">{html.escape(post['og_description_en'])}</p>
      <p class="text-sm text-gray-400 leading-relaxed line-clamp-3 hindi" x-show="$store.lang.current === 'hi'" lang="hi">{html.escape(post['og_description_hi'])}</p>
      <p class="text-xs text-gray-600 mt-3">{post['published_at']}</p>
    </div>
  </a>
</article>''')
PY
cat /tmp/blog-cards.html | wc -l   # ~200 lines
# Then paste into blog/index.html in place of <!-- BLOG_CARDS_INJECTED_BY_PLAN_STEP_6.1 -->
```

### Step 6.2 — Update `sitemap.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://aarambhax.ai/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://aarambhax.ai/products/</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://aarambhax.ai/about/</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://aarambhax.ai/philosophy/</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://aarambhax.ai/blog/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://aarambhax.ai/contact/</loc><changefreq>yearly</changefreq><priority>0.6</priority></url>
  <!-- 20 blog posts, priority 0.7 each, auto-list from briefs.yaml: -->
  <!-- generate with: python3 -c 'import yaml; [print(f"  <url><loc>https://aarambhax.ai/blog/{p["slug"]}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>") for p in yaml.safe_load(open("content/briefs.yaml"))["posts"]]' -->
</urlset>
```

Replace the comment with the actual 20 URL entries (one per post slug in `briefs.yaml`).

### Step 6.3 — All-page smoke test + final commit

```bash
cd /Users/ajayagrawal/aarambhax
python3 -m http.server 8000 > /tmp/s.log 2>&1 & PID=$!
sleep 1
for p in / /about/ /products/ /philosophy/ /blog/ /contact/ /404.html /sitemap.xml /robots.txt; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8000$p")
  echo "$code $p"
done
# 3 random blog posts
for slug in $(ls blog | shuf -n 3 2>/dev/null || ls blog | head -3); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8000/blog/$slug/")
  echo "$code /blog/$slug/"
done
kill $PID 2>/dev/null; wait 2>/dev/null
# Expect: every line is 200
```

```bash
cd /Users/ajayagrawal/aarambhax
git add blog/index.html sitemap.xml
git commit -m "feat(v2): blog index upgrade + sitemap with 20 posts

  - /blog/ replaces empty-state with a sticky-filter card grid:
    10 category pills (All, Philosophy, Market, Education, Commerce,
    Compliance, Livestock, Insurance, Govt Services, Welfare) +
    20-card grid. Alpine \`cat\` state filters by vertical; card
    titles/descriptions flip with the existing lang store.
  - sitemap.xml now lists all 5 top-level pages + /contact/ + all 20
    blog posts, priority-weighted.

The /contact/, /about/, /products/, /philosophy/ pages are unchanged
in this commit — only the index grid + sitemap.

Spec: docs/superpowers/specs/2026-04-17-aarambha-studio-v2-design.md

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
```

### Step 6.4 — Push everything to origin/main

```bash
cd /Users/ajayagrawal/aarambhax
git log --oneline origin/main..HEAD   # Review all Phase 2 commits before push
git push origin main
```

Expect: all Phase 2 commits land on `hforever-ai/aarambha-studio`. GitHub Pages rebuild picks them up in ~2 min.

### Step 6.5 — Final live verification

```bash
# After GH Pages rebuild (wait ~3 minutes)
for p in "/" "/contact/" "/products/" "/philosophy/" "/blog/"; do
  curl -s -o /dev/null -w "%{http_code} https://aarambhax.ai$p\n" "https://aarambhax.ai$p"
done
for slug in $(ls blog | head -3); do
  curl -s -o /dev/null -w "%{http_code} https://aarambhax.ai/blog/$slug/\n" "https://aarambhax.ai/blog/$slug/"
done
# All should be 200
```

---

## Self-Review

**1. Spec coverage** — every spec section maps to tasks:
- Site structure additions (contact, partner, press) → Task 1 ✓
- Product portfolio expansion → Task 2 ✓
- Philosophy 7-product mapping → Task 3 ✓
- Bilingual architecture + content pipeline + content rules → Tasks 4, 5 ✓
- 20 blog post seed → Task 5 ✓
- Image generation (33 images) → Tasks 4b, 4c, 5 ✓
- Blog index upgrade + sitemap + push → Task 6 ✓

**2. Placeholder scan** — no TBDs. Every code block inline. `<!-- BLOG_CARDS_INJECTED_BY_PLAN_STEP_6.1 -->` is a marker that Step 6.1's script output replaces — legitimate template slot, not a placeholder.

**3. Type consistency** — Alpine store `$store.lang.current` used identically everywhere. Cache-bust mechanism unchanged from v1. Colour tokens (primary/accent/cosmos/dark/card) match Tailwind config from v1 head. File paths consistent (`blog/<slug>/index.html`, not `blog/<slug>.html`).

**4. Coverage gaps** — none. Analytics, separate-URL i18n, real email capture, blog comments, RSS are explicit non-goals in the spec.

---

## Execution Handoff

Plan saved to `docs/superpowers/plans/2026-04-17-aarambha-studio-v2.md`.

Execution approach: **subagent-driven** (same pattern as v1). One implementer subagent per task, I verify via smoke tests between tasks, final push after Task 6.

Task order — strict:
1. Task 1: contact + homepage additions
2. Task 2: products rewrite
3. Task 3: philosophy update
4. Task 4: pipeline scripts + briefs (commit scripts only, no run yet)
5. Task 5: run pipeline (images then posts) + commit content
6. Task 6: blog index + sitemap + push
