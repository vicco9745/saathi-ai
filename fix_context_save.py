from pathlib import Path

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

old = '''    for item in load_responses():
        if user_text == normalize_text(item["user"]):
            return item["assistant"]'''

new = '''    for item in load_responses():
        if user_text == normalize_text(item["user"]):
            reply = item["assistant"]
            add_conversation(original_text, reply)
            return reply'''

if old not in s:
    raise SystemExit("Exact response block not found")

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("Context save fix OK")
