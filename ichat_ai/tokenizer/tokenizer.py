import re
import json
from pathlib import Path

class IChatTokenizer:
    def __init__(self):
        self.vocab = {}
        self.id_to_token = {}

    def split_text(self, text):
        return re.findall(
            r'[\u0900-\u097F]+|[a-zA-Z]+|\d+|[^\w\s]',
            text,
            re.UNICODE
        )

    def train(self, texts):
        tokens = set()

        for text in texts:
            tokens.update(self.split_text(text))

        special = ["<PAD>", "<UNK>", "<BOS>", "<EOS>"]
        all_tokens = special + sorted(tokens)

        self.vocab = {
            token: i for i, token in enumerate(all_tokens)
        }

        self.id_to_token = {
            i: token for token, i in self.vocab.items()
        }

    def encode(self, text):
        unk = self.vocab.get("<UNK>", 1)
        return [
            self.vocab.get(token, unk)
            for token in self.split_text(text)
        ]

    def decode(self, ids):
        return " ".join(
            self.id_to_token.get(i, "<UNK>")
            for i in ids
        )

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                self.vocab,
                f,
                ensure_ascii=False,
                indent=2
            )

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.vocab = json.load(f)

        self.id_to_token = {
            int(i): token
            for token, i in self.vocab.items()
        }
