from pathlib import Path

p = Path("ichat_ai/memory/memory.py")
s = p.read_text(encoding="utf-8")

addition = '''

def add_conversation(user_text, assistant_text, limit=10):
    memory = load_memory()

    history = memory.get("conversation_history", [])

    history.append({
        "user": user_text.strip(),
        "assistant": assistant_text.strip()
    })

    memory["conversation_history"] = history[-limit:]

    save_memory(memory)


def get_conversation_history():
    memory = load_memory()
    return memory.get("conversation_history", [])
'''

if "def add_conversation(" not in s:
    s += addition

p.write_text(s, encoding="utf-8")
print("Conversation memory update OK")
