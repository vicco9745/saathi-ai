from ichat_ai.tokenizer.tokenizer import IChatTokenizer
from ichat_ai.learning.data_loader import load_training_texts
from ichat_ai.model.model import IChatModel


def main():
    tokenizer = IChatTokenizer()
    tokenizer.load("ichat_ai/tokenizer/vocab.json")

    texts = load_training_texts()
    sequences = [tokenizer.encode(text) for text in texts]

    model = IChatModel(len(tokenizer.vocab))

    print("=== Saathi Training Engine ===")
    print("Training data:", len(sequences))
    print("Vocabulary:", len(tokenizer.vocab))

    model.train(sequences)

    print("Training pipeline finished.")
    print(model.info())


if __name__ == "__main__":
    main()
