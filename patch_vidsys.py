p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDEO_SYSTEM" in s:
    print("vidsys: server pehle se laga hai")
else:
    vs = '''VIDEO_SYSTEM = """Tum Saathi ho. Tumhe EK video ke frames kram mein diye gaye hain. Inhe photo ya document mat samjho, aur 'photo', 'frame' ya 'image' shabd use mat karo; sab kuch 'video mein' ke roop mein batao.
Jawab Roman Hinglish mein, saaf aur seedha. In teen hisson mein likho:
**Video mein kya ho raha hai** - shuru se ant tak scene-by-scene: kaun dikh raha hai (kapde, bhaav, jagah), woh kya kar raha hai, scene kaise badalte hain.
**Jo likha ya bola dikha** - screen par jo subtitles ya text dikhe use bilkul waisa hi likho jaisa likha hai (spelling mat badlo), aur batao ki yeh kya keh raha hai. Tum aawaaz nahi sun sakte, isliye bola hua sirf tab batao jab woh likha dikhe.
**Matlab aur sandesh** - video kis baare mein hai, ismein se kya seekh milti hai, aur agar baat kamyabi ya tarakki ki hai to kamyab hone ke liye video kya sikhata hai.
Niyam: kisi asli insaan ko chehre se pehchaan kar naam mat batao; sirf wahi batao jo dikhta ya likha hai. Jo saaf na dikhe use 'andaaza' kehkar batao. Watermark ya credit (jaise @naam) dikhe to ek line mein batao. Spelling ya grammar ki galtiyan mat nikalo."""

'''
    a = "def _call_vision_v2("
    i = s.find(a)
    j = s.find("\nclass TitleRequest", i)
    if s.count(a) != 1 or j == -1:
        print("vidsys: function nahi mili, kuch nahi badla", s.count(a), j)
        raise SystemExit
    seg = s[i:j]
    c1 = '{"role": "system", "content": SYSTEM_INSTRUCTION}'
    c2 = r'text_prompt = VISION_RULES + "\n\n" + VIDEO_RULES + "\n\nUSER KA SAWAAL: " + (prompt or default_prompt)'
    n1, n2 = seg.count(c1), seg.count(c2)
    if n1 < 1 or n2 != 1:
        print("vidsys: lines nahi mili", n1, n2)
        raise SystemExit
    seg = seg.replace(c1, '{"role": "system", "content": (VIDEO_SYSTEM if is_video else SYSTEM_INSTRUCTION)}')
    seg = seg.replace(c2, r'text_prompt = VIDEO_RULES + "\n\nUSER KA SAWAAL: " + (prompt or default_prompt)')
    s = s[:i] + vs + seg + s[j:]
    open(p, "w", encoding="utf-8").write(s)
    print("vidsys: server patch lag gaya, system jagah:", n1)

j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
if "var N = Math.max(6" in t:
    print("vidsys: js pehle se laga hai")
else:
    a1 = "var FRAMES = 5, MAXW = 900;"
    a2 = "for (var i = 0; i < FRAMES; i++) times.push(Math.min(Math.max(d - 0.1, 0), d * (i + 0.5) / FRAMES));"
    a3 = "setTimeout(finish, 45000)"
    if t.count(a1) == 1 and t.count(a2) == 1 and t.count(a3) == 1:
        t = t.replace(a1, "var FRAMES = 5, MAXW = 1024;")
        t = t.replace(a2, "var N = Math.max(6, Math.min(8, Math.round(d / 1.5))); for (var i = 0; i < N; i++) times.push(Math.min(Math.max(d - 0.1, 0), d * (i + 0.5) / N));")
        t = t.replace(a3, "setTimeout(finish, 90000)")
        t = t.replace("'image/jpeg', 0.72", "'image/jpeg', 0.75")
        open(j, "w", encoding="utf-8").write(t)
        print("vidsys: js badal di (8 frame tak)")
    else:
        print("vidsys: js lines nahi mili", t.count(a1), t.count(a2), t.count(a3))

for f in ["index.html", "site_patches/98_video.py"]:
    x = open(f, encoding="utf-8").read()
    if "saathi_video.js?v=7" in x:
        open(f, "w", encoding="utf-8").write(x.replace("saathi_video.js?v=7", "saathi_video.js?v=8"))
        print(f + ": v=8 kar diya")
    else:
        print(f + ": v=7 nahi mila, chhoda")
