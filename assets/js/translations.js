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
