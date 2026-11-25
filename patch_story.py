p = 'app/main.py'
s = open(p, encoding='utf-8').read()
FN = r'''import re as _re_story, json as _json_story
_STORY_WORD = _re_story.compile(r"(kahani|kahaani|कहानी|story|stories)", _re_story.I)
_STORY_VERB = _re_story.compile(r"(suna|bana|likh|bata|de do|tell|write|narrate|सुना|बना|लिख|बता)", _re_story.I)
_STORY_SYSTEM = (
    "Tum kahani likhne wale ho. Sirf ek JSON do, aur kuch nahi, koi backtick nahi.\n"
    "Agar maang kisi asli, aitihasik ya jeevit insaan ki zindagi ya sachchi ghatna ke baare mein hai, to sirf: {\"real\": true}\n"
    "Warna: {\"real\": false, \"title\": \"...\", \"scenes\": [\"...\", \"...\", \"...\"]}\n"
    "Niyam: exactly 3 scenes, har scene 2 se 4 chhote vakya. Bhasha wahi jo user ne maangi; "
    "agar nahi maangi to user ke sandesh ki bhasha (Hindi ya Hinglish ho to Devanagari Hindi). "
    "Sirf kahani likho: koi film, saal, 'logon ne kaha', lekhak ya sachchi jaankari mat jodo. "
    "Lok-kathao ke paatra (jaise Shekhchilli, Birbal) ki seedhi saral kahani likho. "
    "Antim scene par ruk jao: koi seekh, nichod, sawaal ya 'aur sunaun' jaisa vakya nahi."
)
def _story_card(msg):
    t = (msg or "").strip()
    if len(t) > 300 or "```" in t or t.startswith("/"):
        return None
    if not (_STORY_WORD.search(t) and _STORY_VERB.search(t)):
        return None
    try:
        out = _call_groq(t, system=_STORY_SYSTEM).strip()
        i = out.find("{")
        j = out.rfind("}")
        d = _json_story.loads(out[i:j + 1])
        if d.get("real"):
            return None
        title = str(d.get("title", "")).strip()
        sc = [str(x).strip() for x in d.get("scenes", []) if str(x).strip()]
        if not title or len(sc) < 2:
            return None
        return {"title": title, "scenes": [{"text": x} for x in sc[:6]]}
    except Exception:
        return None

'''
a1 = 'def _detect_action(msg: str) -> str:'
a2 = '    action = _detect_action(body.message)\n'
n2 = a2 + '''    _st = _story_card(body.message)
    if _st:
        return {"service": "chat", "reply": "", "story": _st, "model": "saathi", "kind": "story"}
'''
if '_story_card' in s:
    print('story server: pehle se laga hai')
elif s.count(a1) == 1 and s.count(a2) == 1:
    s = s.replace(a1, FN + a1, 1).replace(a2, n2, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('story server: laga diya')
else:
    print('story server: jagah nahi mili', s.count(a1), s.count(a2))
