from pathlib import Path
import json

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    'APPROVED_FILE = BASE_DIR / "ichat_ai" / "dataset" / "approved.jsonl"',
    'APPROVED_FILE = BASE_DIR / "ichat_ai" / "dataset" / "approved.jsonl"\nLEARNING_FILE = BASE_DIR / "ichat_ai" / "dataset" / "learning_queue.jsonl"'
)

marker = "def normalize_text(text):"

new_function = '''def save_to_learning_queue(user_text):
    text = user_text.strip()
    if not text:
        return

    normalized = normalize_text(text)
    existing = set()

    if LEARNING_FILE.exists():
        with open(LEARNING_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    existing.add(normalize_text(data.get("user", "")))
                except json.JSONDecodeError:
                    pass

    if normalized in existing:
        return

    with open(LEARNING_FILE, "a", encoding="utf-8") as f:
        json.dump({"user": text}, f, ensure_ascii=False)
        f.write("\\n")


'''

s = s.replace(marker, new_function + marker)
s = s.replace(
    '    return "मैं अभी यह जवाब सीख रहा हूँ।"',
    '    save_to_learning_queue(original_text)\n    return "मैं अभी यह जवाब सीख रहा हूँ।"'
)

p.write_text(s, encoding="utf-8")
print("Saathi learning update OK")
