p = "index.html"
s = open(p, encoding="utf-8").read()
if "saathi_video.js" in s:
    print("script tag pehle se hai")
else:
    i = s.rfind("</body>")
    if i == -1:
        print("</body> nahi mila, kuch nahi badla")
        raise SystemExit
    s = s[:i] + '<script src="saathi_video.js?v=1"></script>\n' + s[i:]
    open(p, "w", encoding="utf-8").write(s)
    print("script tag jod diya")
