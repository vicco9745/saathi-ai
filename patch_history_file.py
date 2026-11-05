p = "index.html"
s = open(p, encoding="utf-8").read()
a = s.find("<script>/*__saathiHistoryPatch*/")
if a != -1:
    b = s.find("</script>\n", a)
    if b != -1:
        s = s[:a] + s[b + len("</script>\n"):]
        print("purana inline patch hata diya")
if "saathi_history.js" in s:
    print("script tag pehle se hai")
else:
    i = s.rfind("</body>")
    if i == -1:
        print("</body> nahi mila, kuch nahi badla")
        raise SystemExit
    s = s[:i] + '<script src="saathi_history.js?v=1"></script>\n' + s[i:]
    print("script tag jod diya")
open(p, "w", encoding="utf-8").write(s)
