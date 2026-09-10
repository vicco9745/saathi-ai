from pathlib import Path

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

old = '''def save_to_learning_queue(user_text):
    text = user_text.strip()
    if not text:
        return

    normalized = normalize_text(text)'''

new = '''def save_to_learning_queue(user_text):
    text = user_text.strip()
    if not text:
        return

    sensitive_words = (
        "password", "passwd", "api key", "apikey",
        "secret", "token", "otp", "पासवर्ड",
        "एपीआई की", "ओटीपी"
    )

    lower_text = text.lower()

    if any(word in lower_text for word in sensitive_words):
        return

    normalized = normalize_text(text)'''

if old not in s:
    raise SystemExit("Expected learning function not found")

s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("Safe learning filter OK")
