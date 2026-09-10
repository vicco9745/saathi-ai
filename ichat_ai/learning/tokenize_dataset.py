from ichat_ai.tokenizer.tokenizer import IChatTokenizer
from ichat_ai.learning.data_loader import load_training_texts


def main():
    tokenizer = IChatTokenizer()
    tokenizer.load("ichat_ai/tokenizer/vocab.json")

    texts = load_training_texts()

    print("Tokenized training data:")

    for i, text in enumerate(texts, 1):
        token_ids = tokenizer.encode(text)

        print(f"\nExample {i}")
        print("Text:", text[:100])
        print("IDs :", token_ids)


if __name__ == "__main__":
    main()
