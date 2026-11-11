p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDEO_SYSTEM_VIS" not in s:
    print("askonly: pehle patch_visual.py chalao (woh abhi laga nahi hai), kuch nahi badla")
    raise SystemExit
if "NIYAM_ASK" in s:
    print("askonly: pehle se laga hai")
    raise SystemExit

N = "PEHLA NIYAM (NIYAM_ASK): agar user ne koi KHAAS sawaal poocha hai (jaise 'kitne aadmi hain', 'kya likha hai', 'dhundhla kya hai', 'kya bol raha hai', 'iska matlab kya hai'), to SIRF usi sawaal ka jawab do, apni taraf se kuch aur mat batao aur koi heading mat banao. Agar user arth ya matlab poochhe to uska matlab samjhao. Neeche ke hisse sirf tab likho jab user ne aam sawaal poocha ho ('video dekh kar batao', 'kya kya hai')."

pairs = [
    ("Jawab Roman Hinglish mein, saaf aur seedha. In teen hisson mein likho:",
     "Jawab Roman Hinglish mein, saaf aur seedha. " + N + " Tab in teen hisson mein likho:"),
    ("Jawab Roman Hinglish mein, saaf aur seedha. Do hisson mein likho:",
     "Jawab Roman Hinglish mein, saaf aur seedha. " + N + " Tab do hisson mein likho:"),
    ("Jawab Hinglish mein, saaf aur seedha, in hisson mein:",
     "Jawab Hinglish mein, saaf aur seedha. " + N + " Tab in hisson mein:"),
    ("Do hisse: 'Video mein kya dikh raha hai' aur (zaroorat ho to) 'Matlab'.",
     N + " Tab do hisse: 'Video mein kya dikh raha hai' aur (zaroorat ho to) 'Matlab'."),
    ('        if not _SEE.search((body.message or "").lower()):',
     '        _SP = _re2.compile(r"bol|awaaz|aawaaz|sun|transcript|shabd|dialogue|kehta|kya\\s+keh|said|speech|audio")\n'
     '        _qq = (body.message or "").strip().lower()\n'
     '        if (not _qq) or (_SP.search(_qq) and not _SEE.search(_qq)):'),
]
bad = [(i, s.count(o)) for i, (o, n) in enumerate(pairs) if s.count(o) != 1]
if bad:
    print("askonly: lines nahi mili, kuch nahi badla", bad)
    raise SystemExit
for o, n in pairs:
    s = s.replace(o, n)
open(p, "w", encoding="utf-8").write(s)
print("askonly: patch lag gaya")
