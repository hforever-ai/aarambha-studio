#!/usr/bin/env bash
# Pre-commit hook: rewrite cache-bust on translations.js references in HTML
# before every commit so HTML and JS stay in lockstep.

set -e
ROOT="$(git rev-parse --show-toplevel)"
python3 "$ROOT/scripts/set_cache_bust.py"
# Stage any HTML changes the script made so they land in this commit.
git add "$ROOT"/*.html "$ROOT"/*/*.html 2>/dev/null || true
