from pathlib import Path

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "from pathlib import Path",
    "from pathlib import Path\nfrom ichat_ai.memory.memory import add_conversation"
)

old = '''def get_response(user_text):
    from ichat_ai.memory.memory import remember, recall'''

new = '''def get_response(user_text):
    from ichat_ai.memory.memory import remember, recall'''

# Keep existing memory imports unchanged.

old_return = '''    if normalized_original in ("मेरा नाम क्या है", "मुझे क्या नाम से जानते हो"):
        name = recall("user_name")
        if name:
            return f"आपका नाम {name} है।"
        return "मुझे अभी आपका नाम याद नहीं है।"'''

new_return = '''    if normalized_original in ("मेरा नाम क्या है", "मुझे क्या नाम से जानते हो"):
        name = recall("user_name")
        if name:
            reply = f"आपका नाम {name} है।"
        else:
            reply = "मुझे अभी आपका नाम याद नहीं है।"
        add_conversation(original_text, reply)
        return reply'''

if old_return in s:
    s = s.replace(old_return, new_return)

# Add conversation recording for the normal response path.
old_end = '''    save_to_learning_queue(original_text)
    return "मैं अभी यह जवाब सीख रहा हूँ।"'''

new_end = '''    save_to_learning_queue(original_text)
    reply = "मैं अभी यह जवाब सीख रहा हूँ।"
    add_conversation(original_text, reply)
    return reply'''

if old_end in s:
    s = s.replace(old_end, new_end)

p.write_text(s, encoding="utf-8")
print("Context engine update OK")
