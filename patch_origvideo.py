import re, sys
ok = True
changed = False

# 1) saathi_video.js: thumbnail banne se pehle asli video ka link sambhalna
j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
a = "function grab(att) {"
if "__origUrl" in t:
    print("orig: saathi_video.js pehle se laga hai")
elif t.count(a) == 1:
    open(j, "w", encoding="utf-8").write(t.replace(a, a + " try { if (!att.__origUrl) att.__origUrl = att.dataUrl; } catch (e) {}"))
    print("orig: saathi_video.js badal di")
    changed = True
else:
    print("orig: saathi_video.js ki line nahi mili", t.count(a)); ok = False

# 2) format.js: server ko asli video bhejna
f = "format.js"
t = open(f, encoding="utf-8").read()
old = "if(p&&p.kind==='video'&&p.dataUrl&&p.dataUrl.length<9000000)a.push({kind:'video',dataUrl:p.dataUrl,name:p.name||'video.mp4'});"
new = "if(p&&p.kind==='video'){var __vu=p.__origUrl||p.dataUrl;if(__vu&&/^data:video/.test(__vu)&&__vu.length<9000000)a.push({kind:'video',dataUrl:__vu,name:p.name||'video.mp4'});}"
fchanged = False
if "__origUrl" in t:
    print("orig: format.js pehle se laga hai")
elif t.count(old) == 1:
    open(f, "w", encoding="utf-8").write(t.replace(old, new))
    print("orig: format.js badal di")
    changed = True
    fchanged = True
else:
    print("orig: format.js ki line nahi mili", t.count(old)); ok = False

# 3) server: seedhe video wale rasta ko chhota karna
p = "app/main.py"
s = open(p, encoding="utf-8").read()
o1 = "for model in _or_video_models()[:2]:"
o2 = "timeout=70,"
if s.count(o1) == 1 and s.count(o2) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(o1, "for model in _or_video_models()[:1]:").replace(o2, "timeout=45,"))
    print("orig: server wait chhota kiya")
else:
    print("orig: server wait wali line nahi mili (zaroori nahi)", s.count(o1), s.count(o2))

# 4) cache todne ke liye version badhana
if changed:
    for fn in ["index.html", "site_patches/98_video.py"]:
        x = open(fn, encoding="utf-8").read()
        if "saathi_video.js?v=8" in x:
            open(fn, "w", encoding="utf-8").write(x.replace("saathi_video.js?v=8", "saathi_video.js?v=9"))
            print(fn + ": saathi_video v=9")
        else:
            print(fn + ": saathi_video v=8 nahi mila")
    h = open("index.html", encoding="utf-8").read()
    def bump(m):
        n = int(m.group(3)) + 1 if m.group(3) else 1
        return m.group(1) + "format.js?v=" + str(n) + m.group(4)
    h2, c = re.subn(r"""(src=["'][^"']*)format\.js(\?v=(\d+))?(["'])""", bump, h, count=1)
    if c == 1:
        open("index.html", "w", encoding="utf-8").write(h2)
        print("index.html: format.js ka version badhaya")
    else:
        print("index.html: format.js ka tag nahi mila")
if not ok:
    sys.exit(1)
