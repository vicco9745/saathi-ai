from pathlib import Path
import json

p = Path("ichat_ai/learning/filter.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    'APPROVED_FILE = Path("ichat_ai/dataset/approved.jsonl")',
    '''APPROVED_FILE = Path("ichat_ai/dataset/approved.jsonl")

def normalize_text(text):
    return " ".join(text.strip().lower().split())'''
)

old = '''    APPROVED_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "user": user_text.strip(),
        "assistant": assistant_text.strip()
    }

    with open(APPROVED_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\\n")

    return True'''

new = '''    APPROVED_FILE.parent.mkdir(parents=True, exist_ok=True)

    question = user_text.strip()
    answer = assistant_text.strip()

    if APPROVED_FILE.exists():
        with open(APPROVED_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if normalize_text(data.get("user", "")) == normalize_text(question):
                        return False
                except json.JSONDecodeError:
                    pass

    record = {
        "user": question,
        "assistant": answer
    }

    with open(APPROVED_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\\n")

    return True'''

if old not in s:
    raise SystemExit("Expected code block not found")

s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("Filter duplicate protection OK")
