p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''_ACTION_HINT = {}
_FOREIGN_WORDS = {
    "para", "pero", "quiero", "crea", "crear", "hazme", "puedes", "una", "los", "las", "del", "sitio",
    "pour", "une", "les", "des", "je", "mon", "fais", "peux",
    "und", "ich", "ein", "eine", "mit", "bitte", "erstelle", "mach", "webseite",
    "crie", "fazer", "fammi", "sito", "per", "con", "che",
    "yang", "dan", "untuk", "buatkan", "tolong", "saya", "bisa", "situs",
    "bir", "bana", "een", "het", "voor", "maak", "mij", "dla", "gumawa", "paki",
}
_INTENT_SYSTEM = (
    "You are an intent classifier. The user message can be in ANY language. "
    "Decide if the user is asking you RIGHT NOW to create (a) a WEBSITE / web page / landing page, "
    "or (b) an IMAGE / picture / photo / drawing / illustration. "
    "Questions about websites or images, or anything else, are NONE. "
    "Reply with exactly one line and nothing else: 'website' or "
    "'image|<one detailed English description of the picture to generate>' or 'none'."
)


def _needs_lang_check(msg):
    m = (msg or "").strip()
    if not m or len(m) > 600:
        return False
    for ch in m:
        if ord(ch) > 127 and ch.isalpha() and not ("\u0900" <= ch <= "\u097f"):
            return True
    import re as _re2
    words = set(_re2.findall(r"[a-z]+", m.lower()))
    return bool(words & _FOREIGN_WORDS)


def _detect_action(msg: str) -> str:
    base = _detect_action_base(msg)
    if base in ("analyze", "pdf", "website", "image"):
        return base
    try:
        if _needs_lang_check(msg):
            out = _call_groq(msg.strip()[:600], system=_INTENT_SYSTEM).strip().strip("`'\" ").lower()
            if out.startswith("website"):
                return "website"
            if out.startswith("image"):
                hint = out.split("|", 1)[1].strip() if "|" in out else ""
                if hint:
                    if len(_ACTION_HINT) > 200:
                        _ACTION_HINT.clear()
                    _ACTION_HINT[msg] = hint
                return "image"
    except Exception:
        pass
    return base


'''
d1 = 'def _detect_action(msg: str) -> str:'
e1 = 'encoded = _up.quote(body.message)'
e2 = 'encoded = _up.quote(_ACTION_HINT.pop(body.message, None) or body.message)'
if '_detect_action_base' in s:
    print('langcard: pehle se laga hai')
elif s.count(d1) == 1 and s.count(e1) == 1:
    s = s.replace(d1, BLOCK + 'def _detect_action_base(msg: str) -> str:', 1).replace(e1, e2, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('langcard: laga diya')
else:
    print('langcard: jagah nahi mili', s.count(d1), s.count(e1))
