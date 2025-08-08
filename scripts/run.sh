#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="${1:-highvalue_auth.txt}"
OUT_DIR="${2:-auth_tags}"

echo "[*] Running BlessedOps Auth Tagger"
python3 auth_recon.py -i "$INPUT_FILE" -o "$OUT_DIR"
echo "[*] Done. See: $OUT_DIR/"
