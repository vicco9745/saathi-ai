p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDEO_SYSTEM_VIS" in s:
    print("visual: pehle se laga hai")
    raise SystemExit

consts = r'''VIDEO_SYSTEM_VIS = """Tum Saathi ho. Tumhe EK video ke frames kram mein diye gaye hain. Inhe photo mat samjho, aur 'photo', 'frame' ya 'image' shabd use mat karo; sab kuch 'video mein' ke roop mein batao.
Sirf wahi batao jo video mein DIKH raha hai. Screen par likha hua text, subtitles, watermark ya bola hua BILKUL mat batao, na hi uska zikr karo.
Jawab Roman Hinglish mein, saaf aur seedha. Do hisson mein likho:
**Video mein kya dikh raha hai** - shuru se ant tak scene-by-scene. Har scene mein batao: kitne log dikhte hain (ginti), kaun-kaun hai (umar ka andaaza, kapde, bhaav, kya kar raha hai), jagah ya mahaul kaisa hai, rang aur roshni kaisi hai. Jo hissa kala ya dhundhla ho use waisa hi kehkar batao ('kala hissa', 'dhundhla hissa'); andaaza mat lagao ki uske peeche kya hai.
**Matlab** - agar dikhne wali cheezon se video ka matlab ya sandesh saaf samajh aata ho to 1-2 line mein batao, nahi to ye hissa chhod do.
Niyam: kisi asli insaan ko chehre se pehchaan kar naam mat batao; sirf wahi batao jo dikhta hai. Jo saaf na dikhe use 'andaaza' kehkar batao, banao mat. Spelling ya grammar ki galtiyan mat nikalo."""

VIDEO_RULES_VIS = """VIDEO MODE (photo/document wale rules aur koi bhi purana format IGNORE karo):
Neeche di gayi tasveerein EK hi video ke frames hain, kram mein. Sirf dikhne wali cheezein batao: scene-by-scene, kitne log hain, kaun kaisa dikhta hai, kya kar raha hai, jagah, rang, kala ya dhundhla hissa. Screen par likha text, subtitles, watermark aur bola hua mat batao. Do hisse: 'Video mein kya dikh raha hai' aur (zaroorat ho to) 'Matlab'. Chehre se kisi asli insaan ka naam mat batao. Jo saaf na dikhe use 'andaaza' kehkar batao."""

'''

anchor = "# VIDNATIVE helpers"
r1o = '{"role": "system", "content": VIDEO_SYSTEM}'
r1n = '{"role": "system", "content": (VIDEO_SYSTEM_VIS if "[[VISUAL_ONLY]]" in (prompt or "") else VIDEO_SYSTEM)}'
r2o = '(VIDEO_SYSTEM if is_video else SYSTEM_INSTRUCTION)'
r2n = '((VIDEO_SYSTEM_VIS if "[[VISUAL_ONLY]]" in (prompt or "") else VIDEO_SYSTEM) if is_video else SYSTEM_INSTRUCTION)'
r3o = r'''    text = VIDEO_RULES + "\n\nUSER KA SAWAAL: " + (prompt or "Is video mein kya ho raha hai, poori detail se batao.")'''
r3n = r'''    text = (VIDEO_RULES_VIS if "[[VISUAL_ONLY]]" in (prompt or "") else VIDEO_RULES) + "\n\nUSER KA SAWAAL: " + (prompt or "Is video mein kya ho raha hai, poori detail se batao.").replace("[[VISUAL_ONLY]]", "")'''
r4o = r'''        text_prompt = VIDEO_RULES + "\n\nUSER KA SAWAAL: " + (prompt or default_prompt)'''
r4n = r'''        text_prompt = (VIDEO_RULES_VIS if "[[VISUAL_ONLY]]" in (prompt or "") else VIDEO_RULES) + "\n\nUSER KA SAWAAL: " + (prompt or default_prompt).replace("[[VISUAL_ONLY]]", "")'''
r5o = '        if _tr:\n            _vmsg = (body.message or'
r5n = r'''        _WANT_TEXT = _re2.compile(r"text|likha|likhe|subtitle|caption|bola|bol\s+raha|bol\s+rahi|bolta|keh|awaaz|aawaaz|transcript|shabd|dialogue|baat")
        if not _WANT_TEXT.search((body.message or "").lower()):
            _vmsg = (body.message or "Is video mein kya dikh raha hai, poori detail se batao.") + " [[VISUAL_ONLY]]"
        elif _tr:
            _vmsg = (body.message or'''

cnt = [s.count(x) for x in (anchor, r1o, r3o, r4o, r5o)]
if cnt != [1, 1, 1, 1, 1] or s.count(r2o) < 1:
    print("visual: lines nahi mili, kuch nahi badla", cnt, s.count(r2o))
    raise SystemExit
s = s.replace(anchor, consts + anchor).replace(r1o, r1n).replace(r2o, r2n).replace(r3o, r3n).replace(r4o, r4n).replace(r5o, r5n)
open(p, "w", encoding="utf-8").write(s)
print("visual: patch lag gaya")
