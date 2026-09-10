import json
from pathlib import Path

MODEL_FILE = Path("ichat_ai/model/weights.json")


def save_model(model):
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "name": model.name,
        "vocab_size": model.vocab_size,
        "hidden_size": model.hidden_size,
        "weights": model.weights,
        "bias": model.bias,
        "trained_steps": model.trained_steps
    }

    MODEL_FILE.write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8"
    )

    print("Model weights saved:", MODEL_FILE)
