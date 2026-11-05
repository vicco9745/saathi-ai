p = "ichat_ai/response_engine.py"
s = open(p, encoding="utf-8").read()
edits = [
 ("_GREETINGS_HI) and not history:\n", "_GREETINGS_HI) and False:\n"),
 ("_IDENTITY_PATTERNS) and not history:\n", "_IDENTITY_PATTERNS) and False:\n"),
]
for old, new in edits:
    if s.count(old) != 1:
        print("match nahi mila, kuch nahi badla:", old)
        raise SystemExit
for old, new in edits:
    s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("response_engine.py badal gaya")
