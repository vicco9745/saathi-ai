p = "ichat_ai/response_engine.py"
s = open(p, encoding="utf-8").read()
edits = [
 ("results = search_web(cleaned_query, limit=3)", "results = search_web(cleaned_query, limit=8)"),
 ("if url and title and len(sources) < 3:", "if url and title and len(sources) < 8:"),
]
for old, new in edits:
    if s.count(old) != 1:
        print("match nahi mila, kuch nahi badla:", old)
        raise SystemExit
for old, new in edits:
    s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(s)
print("sources 8 kar diye")
