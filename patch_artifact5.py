p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''import re as _re_art
_ART_CLASSIFY = (
    "Decide if the user's message asks you to MAKE something that can be shown as one web page: "
    "any design, poster, layout, map, floor plan, diagram, chart, table, planner, calendar, tool, calculator, game, quiz, "
    "form, card, animation, dashboard, simulation, visualisation, resume, invitation, menu, logo or anything similar, "
    "in ANY language or spelling. A plain question, a story, an essay, an explanation or ordinary chat is NOT. "
    "Answer with exactly YES or NO."
)
_ART_SYSTEM = (
    "You build things as a single self-contained HTML document. "
    "Output ONLY the HTML document, starting with <!DOCTYPE html>, no markdown fences, no explanation. "
    "Rules: inline CSS and JS only, no external files, fonts, images or network calls; mobile-first and responsive; "
    "polished modern look that uses ONLY these CSS variables for every colour: var(--s-bg) page background, var(--s-panel) cards, "
    "var(--s-text) text, var(--s-soft) secondary text, var(--s-accent) main colour for buttons, headings and highlights, "
    "var(--s-accent-soft) light tint, var(--s-border) borders; do not invent other colours unless the user asks for specific colours "
    "or the thing needs them (map, chart legend); "
    "all visible text in the same language as the user's message; "
    "keep it under about 250 lines; include a <title> that is a short descriptive name (max 6 words) in that language; "
    "make any interactive parts really work; for a map, floor plan or route draw a clear labelled schematic in inline SVG (no map tiles); "
    "for charts and diagrams use inline SVG or canvas."
)
_ART_NOTE = (
    "In the same language as the user's message, write 2 short sentences describing what was made and how to use it. "
    "No emoji, no markdown, no questions, no offers of more help."
)
def _artifact_card(msg):
    t = (msg or "").strip()
    if not t or len(t) > 1500 or "```" in t or "=== file" in t or t.startswith("/"):
        return None
    try:
        c = _call_groq(t, system=_ART_CLASSIFY)
    except Exception:
        return None
    if not (c or "").strip().upper().startswith("YES"):
        return None
    from concurrent.futures import ThreadPoolExecutor
    def build():
        try:
            return _call_groq(t, system=_ART_SYSTEM)
        except Exception:
            return ""
    def note():
        try:
            return _call_groq(t, system=_ART_NOTE).strip()
        except Exception:
            return ""
    with ThreadPoolExecutor(max_workers=2) as ex:
        fb = ex.submit(build)
        fn = ex.submit(note)
        out = (fb.result() or "").strip()
        nt = (fn.result() or "").strip()
    out = out.replace("```html", "").replace("```", "").strip()
    i = out.lower().find("<!doctype")
    if i < 0:
        i = out.lower().find("<html")
    if i < 0:
        return None
    out = out[i:]
    if "</html>" not in out.lower():
        out += "\n</body></html>"
    if len(out) < 200:
        return None
    mt = _re_art.search(r"<title>(.*?)</title>", out, _re_art.I | _re_art.S)
    title = (mt.group(1).strip() if mt else "")[:60]
    return {"html": out, "title": title, "note": nt[:400]}

'''
CALL = '''    if action not in ("analyze", "pdf", "website", "image", "story"):
        _ar = _artifact_card(body.message)
        if _ar:
            return {"service": "chat", "reply": _ar["note"], "html": _ar["html"], "title": _ar["title"], "model": "saathi", "kind": "artifact"}
'''
if '_artifact_card' in s:
    print('artifact5: pehle se laga hai')
else:
    a = s.find('def _detect_action(msg: str) -> str:')
    k = s.find('"kind": "story"}')
    e = s.find('\n', k) + 1 if k >= 0 else -1
    if a < 0 or k < 0 or '_call_groq' not in s or k < a:
        print('artifact5: jagah nahi mili', a, k)
    else:
        s = s[:e] + CALL + s[e:]
        s = s[:a] + BLOCK + s[a:]
        open(p, 'w', encoding='utf-8').write(s)
        print('artifact5: laga diya')
