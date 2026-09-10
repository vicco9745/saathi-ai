import json
from pathlib import Path

MODEL_FILE = Path("ichat_ai/model/weights.json")


def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Model file nahi mili: {MODEL_FILE}")

    data = json.loads(
        MODEL_FILE.read_text(encoding="utf-8")
    )

    print("Model loaded successfully.")
    print("Name:", data["name"])
    print("Vocabulary:", data["vocab_size"])
    print("Hidden size:", data["hidden_size"])
    print("Training steps:", data["trained_steps"])

    return data


if __name__ == "__main__":
    load_model()
