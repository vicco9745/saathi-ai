from ichat_ai.tokenizer.tokenizer import IChatTokenizer
from ichat_ai.model.load_model import load_model
from ichat_ai.response_engine import get_response
from ichat_ai.memory.memory import remember, recall


def main():
    print("=== Saathi ===")
    print("Model loading...")

    model = load_model()

    tokenizer = IChatTokenizer()
    tokenizer.load("ichat_ai/tokenizer/vocab.json")

    print("Chat ready. Exit ke liye 'exit' likho.")

    while True:
        user_text = input("\nYou: ").strip()

        if user_text.lower() == "exit":
            print("Saathi: Bye!")
            break

        if not user_text:
            continue

        response = get_response(user_text)

        print("Saathi:", response)


if __name__ == "__main__":
    main()
