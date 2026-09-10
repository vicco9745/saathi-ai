from pathlib import Path

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "from ichat_ai.memory.memory import add_conversation",
    "from ichat_ai.memory.memory import add_conversation, get_conversation_history"
)

marker = "def get_response(user_text):"

new_code = '''def get_recent_context(limit=5):
    history = get_conversation_history()
    return history[-limit:]


'''

if "def get_recent_context(" not in s:
    s = s.replace(marker, new_code + marker)

p.write_text(s, encoding="utf-8")
print("History context reader OK")
