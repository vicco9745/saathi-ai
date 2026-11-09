j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
if "var N = Math.max(6" in t:
    print("vidhd: js pehle se laga hai")
else:
    a1 = "var FRAMES = 5, MAXW = 900;"
    a2 = "for (var i = 0; i < FRAMES; i++) times.push(Math.min(Math.max(d - 0.1, 0), d * (i + 0.5) / FRAMES));"
    a3 = "setTimeout(finish, 45000)"
    if t.count(a1) == 1 and t.count(a2) == 1 and t.count(a3) == 1:
        t = t.replace(a1, "var FRAMES = 5, MAXW = 1280;")
        t = t.replace(a2, "var N = Math.max(6, Math.min(10, Math.round(d / 2))); for (var i = 0; i < N; i++) times.push(Math.min(Math.max(d - 0.1, 0), d * (i + 0.5) / N));")
        t = t.replace(a3, "setTimeout(finish, 90000)")
        t = t.replace("'image/jpeg', 0.72", "'image/jpeg', 0.8")
        open(j, "w", encoding="utf-8").write(t)
        print("vidhd: saathi_video.js badal di")
    else:
        print("vidhd: js lines nahi mili", t.count(a1), t.count(a2), t.count(a3))

p = "app/main.py"
m = open(p, encoding="utf-8").read()
n = m.count("images[:3]") + m.count("images[:5]")
if n == 0:
    print("vidhd: server limit pehle se badli hai")
else:
    m = m.replace("images[:3]", "images[:10]").replace("images[:5]", "images[:10]")
    open(p, "w", encoding="utf-8").write(m)
    print("vidhd: server limit 10 kar di (%d jagah)" % n)

for f in ["index.html", "site_patches/98_video.py"]:
    s = open(f, encoding="utf-8").read()
    if "saathi_video.js?v=4" in s:
        open(f, "w", encoding="utf-8").write(s.replace("saathi_video.js?v=4", "saathi_video.js?v=5"))
        print(f + ": v=5 kar diya")
    else:
        print(f + ": v=4 nahi mila, chhoda")
