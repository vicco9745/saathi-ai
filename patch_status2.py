import json, os, re

AJ = "ichat_ai/abilities.json"
AP = "ichat_ai/abilities.py"
MP = "app/main.py"
KEYS = {"Video padhna": "video", "Photo padhna": "photo", "Saathi Private Chrome": "chrome"}

DEFAULT = [
    {"name": "Video padhna", "key": "video", "status": "ok", "note": "",
     "text": "user video bheje to uske frames dekhe jaate hain aur aawaaz (Hindi) likhi jaati hai. Bina kuch likhe video bhejne par bole gaye shabd bataye jaate hain, aur 'video dekh kar batao' likhne par jo dikh raha hai woh bataya jaata hai.",
     "needs_any": ["GROQ_API_KEY", "OPENROUTER_API_KEY"]},
    {"name": "Photo padhna", "key": "photo", "status": "ok", "note": "",
     "text": "user photo bheje to use dekh kar padh sakte ho aur uske baare mein bata sakte ho.",
     "needs_any": ["GROQ_API_KEY", "OPENROUTER_API_KEY"]},
    {"name": "Saathi Private Chrome", "key": "chrome", "status": "ok", "note": "",
     "text": "tumhari banayi hui website ko asli Chromium browser mein desktop, tablet aur mobile size par khol kar jaancha jaata hai (JavaScript galtiyan, tooti images aur links, bekaar buttons) aur report jawab ke neeche judti hai. Tum kisi dusre ki website apni marzi se nahi khol sakte.",
     "needs_env": ["CHROME_URL", "CHROME_KEY"]},
]

if os.path.exists(AJ):
    items = json.load(open(AJ, encoding="utf-8"))
    for it in items:
        if it.get("name") in KEYS:
            it.setdefault("key", KEYS[it["name"]])
        it.setdefault("status", "ok")
        it.setdefault("note", "")
    print("status: abilities.json pehle se thi, status jodi")
else:
    items = DEFAULT
    print("status: abilities.json bana di")
with open(AJ, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

PY = r'''import json, os

_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abilities.json")


def _load():
    try:
        with open(_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def ability_down(key):
    for it in _load():
        if it.get("key") == key and it.get("status") == "broken":
            return True, it.get("note") or ""
    return False, ""


def abilities_text():
    on, down = [], []
    for it in _load():
        name = str(it.get("name", ""))
        if it.get("status") == "broken":
            down.append("- " + name + ": ABHI KHARAB HAI. Gadbadi: " + (it.get("note") or "abhi theek ho rahi hai"))
            continue
        need = it.get("needs_env") or []
        any_of = it.get("needs_any") or []
        if need and not all(os.environ.get(k) for k in need):
            continue
        if any_of and not any(os.environ.get(k) for k in any_of):
            continue
        on.append("- " + name + ": " + str(it.get("text", "")))
    out = ""
    if on:
        out += (
            "\n\nTUMHARI ABHI KI KSHAMTAYEN (yeh suchi apne aap banti hai: isme jo likha hai wahi tumhare paas hai, "
            "aur jo isme nahi hai uske baare mein mat kaho ki tumhare paas hai):\n"
            + "\n".join(on)
            + "\nJab user poochhe ki tumhare paas kya hai ya kya tum koi kaam kar sakte ho, to isi suchi ke hisaab se "
            "apne shabdon mein jawab do; koi tay vaakya mat dohrao."
        )
    if down:
        out += (
            "\n\nYEH SUVIDHAYEN ABHI KHARAB HAIN:\n" + "\n".join(down)
            + "\nAgar user inmein se koi suvidha maange, to apne shabdon mein kaho ki ismein abhi gadbadi hai, "
            "team ise theek karne mein lagi hai, jaldi theek ho jaayegi, aur abhi tum ise nahi kar sakte. "
            "Kharab ya adhoora kaam dene ki koshish mat karo aur banawati jawab mat banao."
        )
    return out
'''
with open(AP, "w", encoding="utf-8") as f:
    f.write(PY)
print("status: abilities.py bana diya")

p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
if "# ABILITIES" in s:
    print("status: ai_providers mein hook pehle se hai")
else:
    for tag in ("VIDEOCAP2", "CHROMECAP"):
        s, n = re.subn(r"\n*# " + tag + r"\nSYSTEM_INSTRUCTION \+= \(\n.*?\n\)\n?", "\n", s, flags=re.S)
        print("status:", tag, "purana hissa hataya" if n else "pehle se nahi tha")
    s = s.rstrip("\n") + "\n\n# ABILITIES\ntry:\n    from ichat_ai.abilities import abilities_text as _abilities_text\n    SYSTEM_INSTRUCTION += _abilities_text()\nexcept Exception:\n    pass\n"
    open(p, "w", encoding="utf-8").write(s)
    print("status: ai_providers mein hook jod diya")

s = open(MP, encoding="utf-8").read()
if "ABILDOWN" in s:
    print("status: main.py pehle se laga hai")
else:
    a1 = '    videos = [a for a in (body.attachments or []) if a.kind == "video" and a.dataUrl]\n'
    a2 = "def _site_check_report(html):\n"
    if s.count(a1) != 1 or s.count(a2) != 1:
        print("status: main.py ki lines nahi mili, kuch nahi badla", s.count(a1), s.count(a2))
        raise SystemExit(1)
    blk1 = a1 + r'''    # ABILDOWN: kharab suvidha ko chalaya na jaye
    try:
        from ichat_ai.abilities import ability_down as _ad
        _hints = ""
        _real = [i for i in images if "video-frame" not in (getattr(i, "name", "") or "")]
        if videos and _ad("video")[0]:
            _hints += " [User ne video bheja hai, par video padhna abhi kharab hai]"
            videos = []
            images = _real
        if _real and _ad("photo")[0]:
            _hints += " [User ne photo bheji hai, par photo padhna abhi kharab hai]"
            images = [i for i in images if i not in _real]
        if _hints:
            body.message = (body.message or "") + _hints
    except Exception:
        pass
'''
    blk2 = a2 + '''    try:
        from ichat_ai.abilities import ability_down as _adc
        if _adc("chrome")[0]:
            return ""
    except Exception:
        pass
'''
    s = s.replace(a1, blk1).replace(a2, blk2)
    open(MP, "w", encoding="utf-8").write(s)
    print("status: main.py mein jod diya")
