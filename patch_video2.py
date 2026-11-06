import re
p = "index.html"
s = open(p, encoding="utf-8").read()
if "saathi_video.js?v=2" in s:
    print("index.html pehle se v=2 hai")
elif s.count("saathi_video.js?v=1") == 1:
    open(p, "w", encoding="utf-8").write(s.replace("saathi_video.js?v=1", "saathi_video.js?v=2"))
    print("index.html v=2 kar diya")
else:
    print("script tag nahi mila, index.html nahi badla")
q = "app/main.py"
m = open(q, encoding="utf-8").read()
t, n = re.subn(r'(def _call_vision_v2\(prompt: str, images: list\) -> str:\n[^\n]*\n)    for img in images\[:3\]:', r'\1    for img in images[:5]:', m, count=1)
if n == 1:
    open(q, "w", encoding="utf-8").write(t)
    print("vision limit 5 kar di")
else:
    print("vision limit wali line nahi mili, main.py nahi badla")
