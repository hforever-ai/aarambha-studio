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
