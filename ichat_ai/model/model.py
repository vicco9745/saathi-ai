import json
import math
import random
from pathlib import Path


class IChatModel:
    def __init__(self, vocab_size, hidden_size=32, seed=42):
        self.name = "Saathi"
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size

        random.seed(seed)

        self.weights = [
            [random.uniform(-0.01, 0.01) for _ in range(vocab_size)]
            for _ in range(hidden_size)
        ]

        self.bias = [0.0 for _ in range(hidden_size)]
        self.trained_steps = 0

    def _forward(self, token_ids):
        if not token_ids:
            return [0.0] * self.hidden_size

        output = []

        for h in range(self.hidden_size):
            total = self.bias[h]

            for token_id in token_ids:
                if 0 <= token_id < self.vocab_size:
                    total += self.weights[h][token_id]

            output.append(math.tanh(total))

        return output

    def train(self, token_sequences, epochs=3, learning_rate=0.01):
        if not token_sequences:
            print("Training data nahi mila.")
            return

        print("=== Actual Learning Started ===")

        for epoch in range(1, epochs + 1):
            total_loss = 0.0

            for sequence in token_sequences:
                if not sequence:
                    continue

                output = self._forward(sequence)

                target = 0.5
                loss = sum((x - target) ** 2 for x in output) / len(output)

                error = target - sum(output) / len(output)

                for h in range(self.hidden_size):
                    self.bias[h] += learning_rate * error

                    for token_id in sequence:
                        if 0 <= token_id < self.vocab_size:
                            self.weights[h][token_id] += (
                                learning_rate * error / len(sequence)
                            )

                total_loss += loss
                self.trained_steps += 1

            print(
                f"Epoch {epoch}/{epochs} | "
                f"Loss: {total_loss:.6f}"
            )

        print("=== Actual Learning Finished ===")

    def info(self):
        return {
            "name": "Saathi",
            "vocab_size": self.vocab_size,
            "hidden_size": self.hidden_size,
            "training_steps": self.trained_steps,
            "status": "trainable model ready"
        }


def main():
    from ichat_ai.tokenizer.tokenizer import IChatTokenizer
    from ichat_ai.learning.data_loader import load_training_texts

    tokenizer = IChatTokenizer()
    tokenizer.load("ichat_ai/tokenizer/vocab.json")

    texts = load_training_texts()
    sequences = [tokenizer.encode(text) for text in texts]

    model = IChatModel(len(tokenizer.vocab))

    model.train(
        sequences,
        epochs=3,
        learning_rate=0.01
    )

    print(model.info())

    from ichat_ai.model.save_model import save_model
    save_model(model)


if __name__ == "__main__":
    main()
