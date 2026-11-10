import re

# 1) index.html mein saathi_video.js ka script tag (v=2) lagana
p = "index.html"
s = open(p, encoding="utf-8").read()
TAG = '<script src="saathi_video.js?v=6"></script>\n'

if "saathi_video.js?v=6" in s:
    print("video: index.html mein v=2 tag pehle se hai")
elif s.count("saathi_video.js?v=1") == 1:
    open(p, "w", encoding="utf-8").write(s.replace("saathi_video.js?v=1", "saathi_video.js?v=6"))
    print("video: tag v=1 se v=2 kar diya")
else:
    i = s.rfind("</body>")
    if i == -1:
        print("video: </body> nahi mila, index.html nahi badla")
    else:
        s = s[:i] + TAG + s[i:]
        open(p, "w", encoding="utf-8").write(s)
        print("video: script tag jod diya")

# 2) server: vision ko 3 ki jagah 5 frame lene dena
q = "app/main.py"
try:
    m = open(q, encoding="utf-8").read()
    if "for img in images[:5]:" in m:
        print("video: vision limit pehle se 5 hai")
    else:
        t, n = re.subn(
            r'(def _call_vision_v2\(prompt: str, images: list\) -> str:\n[^\n]*\n)    for img in images\[:3\]:',
            r'\1    for img in images[:5]:',
            m, count=1)
        if n == 1:
            open(q, "w", encoding="utf-8").write(t)
            print("video: vision limit 5 kar di")
        else:
            print("video: vision limit wali line nahi mili, main.py nahi badla")
except FileNotFoundError:
    print("video: app/main.py nahi mili")
