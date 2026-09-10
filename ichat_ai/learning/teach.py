from ichat_ai.learning.filter import save_approved


def main():
    print("=== Saathi Teaching Mode ===")

    user_text = input("Sawal: ").strip()
    assistant_text = input("Sahi jawab: ").strip()

    if save_approved(user_text, assistant_text):
        print("Saathi ne naya jawab save kar liya.")
    else:
        print("Data save nahi hua. Sawal aur jawab check karo.")


if __name__ == "__main__":
    main()
