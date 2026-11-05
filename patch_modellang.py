p = "ichat_ai/response_engine.py"
s = open(p, encoding="utf-8").read()
edits = [
 ('    if normalized_original in _GREETINGS_EN or normalized_original in _GREETINGS_HI:\n        if normalized_original in _GREETINGS_HI or _lang == "hi":\n',
  '    if (normalized_original in _GREETINGS_EN or normalized_original in _GREETINGS_HI) and not history:\n        if False:\n'),
 ('    if _matches_any(normalized_original, _IDENTITY_PATTERNS):\n        if _lang == "hi":\n',
  '    if _matches_any(normalized_original, _IDENTITY_PATTERNS) and not history:\n        if False:\n'),
]
for old, new in edits:
    if s.count(old) != 1:
        print("match nahi mila, kuch nahi badla")
        raise SystemExit
for old, new in edits:
    s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("response_engine.py badal gaya")
