import json
from pathlib import Path

CLEAN_DIR = Path("ichat_ai/dataset/cleaned")
OUTPUT = Path("ichat_ai/dataset/approved/training.jsonl")

def prepare():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with open(OUTPUT, "w", encoding="utf-8") as out:
        for file in CLEAN_DIR.glob("*.txt"):
            text = file.read_text(encoding="utf-8").strip()

            if not text:
                continue

            record = {
                "text": text,
                "source": file.name
            }

            out.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )
            count += 1

    print("Training documents:", count)
    print("Saved:", OUTPUT)

if __name__ == "__main__":
    prepare()
