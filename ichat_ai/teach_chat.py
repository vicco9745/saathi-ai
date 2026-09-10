from ichat_ai.response_engine import get_response
from ichat_ai.learning.filter import save_approved
from ichat_ai.memory.memory import remember, recall

print("=== Saathi Teaching Chat ===")
print("सिखाने के लिए: /teach")
print("Memory save karne ke liye: /remember")
print("बाहर निकलने के लिए: /exit")

while True:
    user_text = input("\nYou: ").strip()

    if user_text.lower() == "/exit":
        print("Saathi: Bye!")
        break

    if user_text.lower() == "/remember":
        key = input("Memory key: ").strip()
        value = input("Memory value: ").strip()
        if key and value:
            remember(key, value)
            print("Saathi: Memory save ho gayi.")
        else:
            print("Saathi: Key aur value dono chahiye.")
        continue

    if user_text.lower() == "/teach":
        question = input("Sawal: ").strip()
        answer = input("Sahi jawab: ").strip()

        if save_approved(question, answer):
            print("Saathi: Naya jawab save ho gaya.")
        else:
            print("Saathi: Data save nahi hua.")
        continue

    if user_text:
        print("Saathi:", get_response(user_text))
