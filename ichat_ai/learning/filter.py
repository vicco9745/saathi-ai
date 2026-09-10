import json
from pathlib import Path

APPROVED_FILE = Path("ichat_ai/dataset/approved.jsonl")

def normalize_text(text):
    return " ".join(text.strip().lower().split())

def is_good_data(user_text, assistant_text):
    if not user_text or not assistant_text:
        return False

    if len(user_text.strip()) < 2:
        return False

    if len(assistant_text.strip()) < 2:
        return False

    return True

def save_approved(user_text, assistant_text):
    if not is_good_data(user_text, assistant_text):
        return False

    APPROVED_FILE.parent.mkdir(parents=True, exist_ok=True)

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
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return True
