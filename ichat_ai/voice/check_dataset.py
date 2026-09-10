import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST = BASE_DIR / "data" / "manifest.jsonl"

print("=== Saathi Voice Dataset Check ===")

total = 0
valid = 0

with open(MANIFEST, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        total += 1
        item = json.loads(line)

        audio = BASE_DIR / "data" / item["audio"]
        text = item["text"]

        if audio.exists() and audio.stat().st_size > 0 and text.strip():
            print(f"OK: {audio.name} | {text}")
            valid += 1
        else:
            print(f"ERROR: {audio}")

print(f"\nTotal samples: {total}")
print(f"Valid samples: {valid}")

if total == valid:
    print("Dataset ready.")
else:
    print("Dataset has errors.")
