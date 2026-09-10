import json
from pathlib import Path
from ichat_ai.tokenizer.tokenizer import IChatTokenizer

CHAT_DATA = Path("ichat_ai/dataset/approved.jsonl")
TEXT_DATA = Path("ichat_ai/dataset/approved/training.jsonl")
VOCAB_FILE = Path("ichat_ai/tokenizer/vocab.json")


def load_chat_data():
    records = []

    if CHAT_DATA.exists():
        with open(CHAT_DATA, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "user" in data and "assistant" in data:
                        records.append(data)
                except json.JSONDecodeError:
                    pass

    return records


def load_text_data():
    records = []

    if TEXT_DATA.exists():
        with open(TEXT_DATA, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "text" in data:
                        records.append(data)
                except json.JSONDecodeError:
                    pass

    return records


def main():
    chat_records = load_chat_data()
    text_records = load_text_data()

    texts = []

    for record in chat_records:
        texts.append(record["user"])
        texts.append(record["assistant"])

    for record in text_records:
        texts.append(record["text"])

    print("Chat examples:", len(chat_records))
    print("Training documents:", len(text_records))

    if not texts:
        print("Training data nahi mila.")
        return

    tokenizer = IChatTokenizer()
    tokenizer.train(texts)
    tokenizer.save(VOCAB_FILE)

    print("Multilingual vocabulary ready.")
    print("Vocabulary size:", len(tokenizer.vocab))
    print("Saved:", VOCAB_FILE)


if __name__ == "__main__":
    main()
