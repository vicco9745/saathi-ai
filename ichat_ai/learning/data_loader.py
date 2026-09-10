import json
from pathlib import Path

CHAT_DATA = Path("ichat_ai/dataset/approved.jsonl")
TEXT_DATA = Path("ichat_ai/dataset/approved/training.jsonl")


def load_training_texts():
    texts = []

    if CHAT_DATA.exists():
        with open(CHAT_DATA, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "user" in data and "assistant" in data:
                        texts.append(data["user"])
                        texts.append(data["assistant"])
                except json.JSONDecodeError:
                    pass

    if TEXT_DATA.exists():
        with open(TEXT_DATA, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "text" in data:
                        texts.append(data["text"])
                except json.JSONDecodeError:
                    pass

    return texts


if __name__ == "__main__":
    texts = load_training_texts()

    print("Training texts:", len(texts))

    for i, text in enumerate(texts, 1):
        print(f"{i}. {text[:100]}")
