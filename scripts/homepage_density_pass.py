#!/usr/bin/env python3
"""
Homepage density pass — option A + D.

A. Tighten vertical rhythm: py-24 → py-20 on content sections (keeps hero +
   waitlist CTA generous).

D. Upgrade the 7-product grid to image-rich cards using /assets/images/products/
   webp files. Removes the redundant "Explore all 7" tile (all 7 are visible).

Idempotent: re-running detects already-patched state via a marker comment and
does not double-apply.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

# ------------------------------------------------------------
# Part A: padding trim. Only on non-hero, non-waitlist sections
# that still use py-24. We keep py-24 on the #waitlist section.
# ------------------------------------------------------------

def trim_padding(text: str) -> tuple[str, int]:
    # Match opening <section ...py-24...> — replace py-24 with py-20,
    # UNLESS the same opening tag contains id="waitlist" or is the hero
    # (the hero has no py-24; it uses min-h-screen).
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        tag = m.group(0)
        if 'id="waitlist"' in tag:
            return tag
        new_tag = tag.replace("py-24", "py-20", 1)
        if new_tag != tag:
            count += 1
        return new_tag

    pattern = re.compile(r'<section\b[^>]*?\bpy-24\b[^>]*?>')
    new_text = pattern.sub(repl, text)
    return new_text, count


# ------------------------------------------------------------
# Part D: product grid rebuild
# ------------------------------------------------------------

PRODUCTS = [
    # slug,        element_hi, element_emoji, name_en,      name_hi,         tag_en,                                              tag_hi,                                     status
    ("shrutam",    "पृथ्वी",   "🌍",          "Shrutam",    "श्रुतम्",        "Audio-first AI tutor for CG+CBSE Class 6–10",       "कक्षा 6-10 CG+CBSE के लिए ऑडियो-फर्स्ट AI ट्यूटर",      ("LIVE",  "🟢 20 मई")),
    ("commerce",   "वायु",     "🌬️",          "WhatsApp Commerce", "WhatsApp कॉमर्स",   "Kirana-to-enterprise B2B ordering AI",              "किराना से एंटरप्राइज तक B2B ऑर्डरिंग AI",               ("LIVE",  "🟢 लाइव")),
    ("karta",      "तेजस्",    "🔥",          "Karta AI",   "कर्ता AI",       "GST + ITR voice-filing for MSMEs",                   "MSMEs के लिए GST + ITR वॉइस-फाइलिंग",                   ("2026", "⚡ 2026")),
    ("pashu",     "जल",       "💧",          "Pashu AI",   "पशु AI",        "Cattle doctor in your pocket",                      "आपकी जेब में पशु डॉक्टर",                                ("2026", "⚡ 2026")),
    ("bima",      "जल",       "💧",          "Bima AI",    "बीमा AI",       "Insurance claim automation for PMFBY + PMJJBY",      "PMFBY + PMJJBY के लिए बीमा क्लेम ऑटोमेशन",              ("2026", "⚡ 2026")),
    ("svayam",    "आकाश",     "✨",          "Svayam AI",  "स्वयं AI",       "Voice-first sarkari form filling",                  "वॉइस-फर्स्ट सरकारी फॉर्म भरना",                          ("2026", "⚡ 2026")),
    ("adhikar",   "आकाश",     "✨",          "Adhikar AI", "अधिकार AI",      "Pension + welfare entitlement tracker",             "पेंशन + कल्याण पात्रता ट्रैकर",                         ("2026", "⚡ 2026")),
]


def _card_en(slug: str, element_hi: str, emoji: str, name_en: str, name_hi: str, tag_en: str, status_en: str) -> str:
    if status_en == "LIVE":
        badge = '<span class="inline-block text-[10px] bg-green-500/15 text-green-400 border border-green-500/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">🟢 LIVE</span>'
    else:
        badge = '<span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold">⚡ 2026</span>'
    return f'''<a href="/products/#{slug}" class="group bg-card border border-white/[.07] rounded-2xl overflow-hidden hover:border-primary/40 hover:-translate-y-0.5 transition-all block">
  <div class="aspect-[4/3] overflow-hidden bg-gradient-to-br from-primary/5 to-accent/5">
    <img src="/assets/images/products/{slug}.webp" alt="{name_en} product illustration" class="w-full h-full object-cover group-hover:scale-[1.03] transition-transform duration-500" loading="lazy" width="600" height="450">
  </div>
  <div class="p-5">
    <div class="flex items-center justify-between mb-2">
      <span class="text-xs font-bold text-accent tracking-[.14em] uppercase"><span class="mr-1">{emoji}</span><span class="hindi">{element_hi}</span></span>
      {badge}
    </div>
    <h3 class="text-gray-100 font-black text-lg mb-1.5"><span class="hindi mr-1.5 text-accent">{name_hi}</span>{name_en}</h3>
    <p class="text-gray-400 text-sm leading-snug">{tag_en}</p>
  </div>
</a>'''


def _card_hi(slug: str, element_hi: str, emoji: str, name_en: str, name_hi: str, tag_hi: str, status_hi: str) -> str:
    if "लाइव" in status_hi or "मई" in status_hi:
        badge = f'<span class="inline-block text-[10px] bg-green-500/15 text-green-400 border border-green-500/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold hindi">{status_hi}</span>'
    else:
        badge = f'<span class="inline-block text-[10px] bg-primary/15 text-primary border border-primary/30 rounded-full px-2 py-0.5 uppercase tracking-[.12em] font-bold hindi">{status_hi}</span>'
    return f'''<a href="/products/#{slug}" class="group bg-card border border-white/[.07] rounded-2xl overflow-hidden hover:border-primary/40 hover:-translate-y-0.5 transition-all block">
  <div class="aspect-[4/3] overflow-hidden bg-gradient-to-br from-primary/5 to-accent/5">
    <img src="/assets/images/products/{slug}.webp" alt="{name_hi} उत्पाद चित्रण" class="w-full h-full object-cover group-hover:scale-[1.03] transition-transform duration-500" loading="lazy" width="600" height="450">
  </div>
  <div class="p-5">
    <div class="flex items-center justify-between mb-2">
      <span class="text-xs font-bold text-accent tracking-[.14em] uppercase hindi"><span class="mr-1">{emoji}</span>{element_hi}</span>
      {badge}
    </div>
    <h3 class="text-gray-100 font-black text-lg mb-1.5"><span class="hindi mr-1.5 text-accent">{name_hi}</span><span class="hindi">{name_en}</span></h3>
    <p class="text-gray-400 text-sm leading-snug hindi">{tag_hi}</p>
  </div>
</a>'''


MARKER_BEGIN_EN = "<!-- PRODUCT_GRID_EN_BEGIN -->"
MARKER_END_EN   = "<!-- PRODUCT_GRID_EN_END -->"
MARKER_BEGIN_HI = "<!-- PRODUCT_GRID_HI_BEGIN -->"
MARKER_END_HI   = "<!-- PRODUCT_GRID_HI_END -->"


def _build_grid_en() -> str:
    cards = []
    for slug, elem_hi, emoji, name_en, name_hi, tag_en, tag_hi, status in PRODUCTS:
        cards.append(_card_en(slug, elem_hi, emoji, name_en, name_hi, tag_en, status[0]))
    return (
        MARKER_BEGIN_EN + "\n"
        + '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">\n'
        + "\n".join(cards) + "\n"
        + "</div>\n"
        + MARKER_END_EN
    )


def _build_grid_hi() -> str:
    cards = []
    for slug, elem_hi, emoji, name_en, name_hi, tag_en, tag_hi, status in PRODUCTS:
        cards.append(_card_hi(slug, elem_hi, emoji, name_en, name_hi, tag_hi, status[1]))
    return (
        MARKER_BEGIN_HI + "\n"
        + '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">\n'
        + "\n".join(cards) + "\n"
        + "</div>\n"
        + MARKER_END_HI
    )


# Replace the existing EN grid (8 <a> tiles) with our new one.
# Pattern: <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
#   ...8 anchors...
#   </div>
OLD_GRID_RE = re.compile(
    r'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">\s*'
    r'(?:<a[\s\S]*?</a>\s*){7,9}'
    r'</div>',
    re.MULTILINE
)


def rebuild_grids(text: str) -> tuple[str, int]:
    # EN: replace first match that is NOT inside an HI (hindi) section
    # We rely on order in index.html: EN section comes before HI mirror.
    if MARKER_BEGIN_EN in text:
        return text, 0  # already patched

    matches = list(OLD_GRID_RE.finditer(text))
    if len(matches) < 2:
        return text, 0  # expected EN + HI grid

    # Replace HI first (higher offset) so EN offsets stay valid
    hi_match = matches[1]
    text = text[:hi_match.start()] + _build_grid_hi() + text[hi_match.end():]
    en_match = OLD_GRID_RE.search(text)  # re-find since text changed
    if en_match is None:
        return text, 1
    text = text[:en_match.start()] + _build_grid_en() + text[en_match.end():]
    return text, 2


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")

    text, n_pad = trim_padding(text)
    text, n_grid = rebuild_grids(text)

    INDEX.write_text(text, encoding="utf-8")
    print(f"padding trimmed on {n_pad} sections")
    print(f"product grids rebuilt: {n_grid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
