from pathlib import Path

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

marker = "def find_similar_response(user_text):"

new_code = '''def find_context_response(user_text):
    text = normalize_text(user_text)

    followups = {
        "और बताओ",
        "थोड़ा और बताओ",
        "फिर क्या",
        "आगे क्या",
        "और"
    }

    if text in followups:
        history = get_recent_context(3)

        for item in reversed(history):
            previous_answer = item.get("assistant", "").strip()
            if previous_answer:
                return previous_answer

    return None


'''

if "def find_context_response(" not in s:
    s = s.replace(marker, new_code + marker)

old = '''    similar_answer = find_similar_response(original_text)
    if similar_answer:
        return similar_answer

    save_to_learning_queue(original_text)'''

new = '''    context_answer = find_context_response(original_text)
    if context_answer:
        reply = context_answer
        add_conversation(original_text, reply)
        return reply

    similar_answer = find_similar_response(original_text)
    if similar_answer:
        reply = similar_answer
        add_conversation(original_text, reply)
        return reply

    save_to_learning_queue(original_text)'''

if old not in s:
    raise SystemExit("Expected matching block not found")

s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("Context rule update OK")
