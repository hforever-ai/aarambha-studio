#!/usr/bin/env bash
# Pre-commit hook: keep generated assets in lockstep with source across every commit.
# - Cache-bust translations.js/CSS references
# - Inject GA4 tag into any new HTML page
# - Inject breadcrumb JSON-LD into any new HTML page
# - Apply a11y/SEO patches (skip-link, focus styles, tap targets, aria-current, etc.)
# - Regenerate Atom feed from briefs.yaml

set -e
ROOT="$(git rev-parse --show-toplevel)"

python3 "$ROOT/scripts/set_cache_bust.py"
python3 "$ROOT/scripts/add_ga.py"
python3 "$ROOT/scripts/wire_logos.py" 2>/dev/null || true
python3 "$ROOT/scripts/add_breadcrumbs.py" 2>/dev/null || true
python3 "$ROOT/scripts/a11y_seo_patch.py"  2>/dev/null || true
python3 "$ROOT/scripts/generate_feed.py"   2>/dev/null || true

# Stage any tracked-file changes the scripts made (including deep blog paths)
# so they land in this commit rather than creating post-commit drift.
cd "$ROOT" && git add -u
