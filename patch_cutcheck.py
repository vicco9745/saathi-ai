p = "app/main.py"
s = open(p, encoding="utf-8").read()
old = "(content and not content.rstrip().endswith("
new = "(len(content) > 200 and not content.rstrip().endswith("
if s.count(old) != 1:
    print("match nahi mila, kuch nahi badla:", s.count(old))
    raise SystemExit
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("main.py badal gaya")
