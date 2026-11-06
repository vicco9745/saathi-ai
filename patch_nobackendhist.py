p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
old = "        if not history_messages:\n            try:\n                from ichat_ai.memory.memory import get_conversation_history\n"
new = "        if False and not history_messages:\n            try:\n                from ichat_ai.memory.memory import get_conversation_history\n"
if s.count(old) != 1:
    print("match nahi mila, kuch nahi badla")
    raise SystemExit
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("ai_providers.py badal gaya")
