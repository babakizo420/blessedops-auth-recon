# auth_recon.py
# -----------------------------------------
# BlessedOps Operator Tool
# Purpose: Automatically tag & classify authentication-related endpoints
#          for bug bounty recon, using smart pattern matching.
# Input: A text file of URLs (e.g., highvalue_auth.txt)
# Output: Tagged files, a summary, and a master tagged list
# -----------------------------------------

import re
import os
from pathlib import Path

# === CONFIG SECTION ===
# These are keyword patterns we use to recognize different auth-related URLs.
# Each tag points to a category of interest (LOGIN, RESET, etc.)

TAG_PATTERNS = {
    "ADMIN": [
        r"admin", r"administrator", r"backoffice", r"\bbo\b", r"tableau[-_ ]?de[-_ ]?bord", r"gestion",
        r"dashboard", r"cms", r"console", r"backend", r"staff", r"superviseur", r"superadmin"
    ],
    "RESET": [
        r"reset", r"forgot", r"recover", r"change", r"create", r"oubli", r"modifier",
        r"reinitialiser", r"reinit", r"mot[-_ ]?de[-_ ]?passe"
    ],
    "TOKEN": [
        r"token", r"jwt", r"session", r"refresh", r"access[-_ ]?token", r"id[-_ ]?token", 
        r"jeton", r"cle[-_ ]?api", r"grant_type=", r"access_token=", r"refresh_token="
    ],
    "LOGIN": [
        r"login", r"sign[-_ ]?in", r"auth(enticate)?", r"connexion", r"connecter",
        r"se[-_ ]?connecter", r"identification", r"authentification"
    ]
}

# === FUNCTION: Tag a single line ===
# This goes through one URL line and checks which category it fits based on the patterns above.
def tag_line(line: str) -> str:
    for tag, patterns in TAG_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, line, flags=re.IGNORECASE):
                return f"[{tag}] {line.strip()}"  # Tag the line like [LOGIN] /login.php
    return f"[OTHER] {line.strip()}"  # If no match, classify as OTHER

# === FUNCTION: Process the full input file ===
# This reads every URL, applies a tag, and saves each into its category file.
def process_file(input_path: str, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)  # Create output folder if it doesn't exist
    counts = {}  # Keeps count of how many endpoints per tag
    tagged_lines = []  # Saves the tagged lines for full output later

    with open(input_path, 'r') as infile:
        for line in infile:
            tagged = tag_line(line)  # Run our tagger on each line
            tagged_lines.append(tagged)  # Save the tagged version
            tag = tagged.split(']')[0][1:]  # Extract the tag name like LOGIN

            # Count how many lines per tag
            counts[tag] = counts.get(tag, 0) + 1

            # Save each raw line into its tag-based file (e.g., login.txt, reset.txt)
            with open(f"{output_dir}/{tag.lower()}.txt", "a") as tagfile:
                tagfile.write(line)

    # Save the full master tagged list
    with open(f"{output_dir}/tagged_auth.txt", "w") as masterfile:
        for line in tagged_lines:
            masterfile.write(f"{line}\n")

    # Show summary counts in terminal
    print("\n=== Tag Counts ===")
    for tag in sorted(counts):
        print(f"{tag}: {counts[tag]}")

# === MAIN FUNCTION: Command-line interface ===
# Allows running the tool with:
#    python3 auth_recon.py -i highvalue_auth.txt -o auth_tags

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Auth Recon Tagger (BlessedOps Edition)")
    parser.add_argument("-i", "--input", required=True, help="Path to highvalue_auth.txt file")
    parser.add_argument("-o", "--output", default="auth_tags", help="Folder to save results")
    args = parser.parse_args()

    process_file(args.input, args.output)
