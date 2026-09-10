from pathlib import Path

p = Path("ichat_ai/response_engine.py")
s = p.read_text(encoding="utf-8")

marker = "def get_response(user_text):"

new_code = '''def similarity_score(text1, text2):
    words1 = set(normalize_text(text1).split())
    words2 = set(normalize_text(text2).split())

    if not words1 or not words2:
        return 0.0

    common = words1.intersection(words2)
    return len(common) / max(len(words1), len(words2))


def find_similar_response(user_text):
    best_answer = None
    best_score = 0.0

    for item in load_responses():
        score = similarity_score(user_text, item["user"])

        if score > best_score:
            best_score = score
            best_answer = item["assistant"]

    if best_score >= 0.5:
        return best_answer

    return None


'''

if "def similarity_score(" not in s:
    s = s.replace(marker, new_code + marker)

old = '''    for item in load_responses():
        if user_text == normalize_text(item["user"]):
            return item["assistant"]

    save_to_learning_queue(original_text)'''

new = '''    for item in load_responses():
        if user_text == normalize_text(item["user"]):
            return item["assistant"]

    similar_answer = find_similar_response(original_text)
    if similar_answer:
        return similar_answer

    save_to_learning_queue(original_text)'''

if old not in s:
    raise SystemExit("Expected response block not found")

s = s.replace(old, new)
p.write_text(s, encoding="utf-8")
print("Smart matching update OK")
