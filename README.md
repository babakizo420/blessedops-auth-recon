# BlessedOps Recon — Auth Tagger (Phase 2.5)

A tiny operator tool that **tags and classifies authentication-related endpoints** (LOGIN / RESET / TOKEN / ADMIN / OTHER) from a flat list of URLs.

- Built during a live 10‑day bounty sprint (“Auth Dominance”).
- Multilingual aware (FR/EN) — catches `connexion`, `mot-de-passe`, `backoffice`, etc.
- Output is **category files** + a **master tagged list** you can feed into Burp or scripts.

## Why
Before you exploit, you map. This tool turns a messy list (wayback/GAU/etc.) into **a prioritized hit list** for auth tests.

## Features (v1)
- Smart pattern tagging (FR + EN)
- Outputs:
  - `auth_tags/login.txt`, `reset.txt`, `token.txt`, `admin.txt`, `other.txt`
  - `auth_tags/tagged_auth.txt` (master view)
- Console counts for fast logging

## Quick Start
```bash
# (Optional) create and activate venv
python3 -m venv .venv && source .venv/bin/activate

# Install deps (none required for v1)
pip install -r requirements.txt

# Run
python3 auth_recon.py -i examples/highvalue_auth.sample.txt -o auth_tags

Input

A plain text file, one URL per line:

https://example.com/login
https://example.com/bo/
https://example.com/password/reset?token=abc
https://example.com/api/token/refresh

Output

auth_tags/
├── admin.txt
├── login.txt
├── reset.txt
├── token.txt
├── other.txt
└── tagged_auth.txt

Roadmap

    --headers mode: fetch status codes + Set-Cookie/Authorization hints

    --forms mode: detect <input name="password">, otp, etc.

    --burp export: generate .urls list for Burp scope/import

    Language packs (ES/DE) via config.json

Ops Notes

    Designed to accelerate Day 3+ auth testing (ADMIN → TOKEN → LOGIN → RESET).

License

MIT
