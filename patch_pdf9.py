p = 'app/main.py'
s = open(p, encoding='utf-8').read()
FN = r'''def _pdf_long_html(prompt, ctx, system):
    import re, json
    from concurrent.futures import ThreadPoolExecutor
    t = prompt or ""
    full = t + (("\n\n" + ctx) if ctx else "")
    m = re.search(r"(\d{1,2})\s*[-]?\s*(?:pages?|pgs?|पन्ने|पन्नों|पन्ना|पेज|पृष्ठ)", t, re.I)
    n = int(m.group(1)) if m else 0
    if n < 4:
        return _call_groq(full, system=system)
    n = min(n, 20)
    secs = []
    try:
        o = _call_groq(t, system=(
            "You plan documents. The user wants a document of about " + str(n) + " pages. "
            "Reply with ONLY a JSON array of exactly " + str(n) + " objects, one per page, each like "
            "{\"title\": \"short section title\", \"points\": \"what this page covers in one sentence\"}. "
            "Titles in the same language as the user's request. No markdown, no explanation."
        ))
        o = (o or "").replace("```json", "").replace("```", "").strip()
        a = o.find("[")
        b = o.rfind("]")
        secs = json.loads(o[a:b + 1])
        secs = [x for x in secs if isinstance(x, dict) and x.get("title")]
    except Exception as e:
        print("PDF outline error", repr(e)[:120])
        secs = []
    if len(secs) < 3:
        return _call_groq(full, system=system)
    titles = " | ".join(str(x.get("title")) for x in secs)
    extra = (
        "\nYOU ARE WRITING ONE PAGE OF A LONGER DOCUMENT. Write ONLY the page you are asked for: an h2 heading and its content, about 220 words, "
        "as HTML with the allowed tags. Do not write html or body tags, and never repeat content of other pages. "
        "Put a chart, box or table tag only where it belongs on this page."
    )
    def one(i):
        x = secs[i]
        head = "Start with the h1 title of the whole document and a one-line p subtitle, then the h2 heading of this page. " if i == 0 else ""
        last = " This is the last page: finish with a short conclusion." if i == len(secs) - 1 else ""
        up = ("DOCUMENT REQUEST:\n" + t + "\n\nFULL OUTLINE: " + titles + "\n\nWRITE ONLY PAGE " + str(i + 1) + " OF " + str(len(secs)) + ": "
              + str(x.get("title")) + " - " + str(x.get("points", "")) + ". " + head + last + (("\n\n" + ctx) if ctx else ""))
        for _ in range(2):
            try:
                h = _call_groq(up, system=system + extra)
                h = (h or "").replace("```html", "").replace("```", "").strip()
                h = re.sub(r"</?(?:html|body|head)[^>]*>", "", h, flags=re.I).strip()
                if len(h) > 40:
                    return h
            except Exception as e:
                print("PDF section error", repr(e)[:120])
        return "<h2>" + str(x.get("title")) + "</h2><p>[fill in]</p>"
    with ThreadPoolExecutor(max_workers=3) as ex:
        parts = list(ex.map(one, range(len(secs))))
    return "<html>" + "<pagebreak/>".join(parts) + "</html>"

'''
OLD = r'''    html_body = _call_groq(body.prompt + (("\n\n" + _ctx) if _ctx else ""), system=system)'''
NEW = '    html_body = _pdf_long_html(body.prompt, _ctx, system)'
MK = 'def _pdf_theme_from_prompt(t):'
if '_pdf_long_html' in s:
    print('pdf9: pehle se laga hai')
else:
    bad = []
    if s.count(OLD) != 1: bad.append('call')
    if s.count(MK) != 1: bad.append('marker')
    if bad:
        print('pdf9: jagah nahi mili', bad)
    else:
        s = s.replace(OLD, NEW, 1)
        s = s.replace(MK, FN + MK, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('pdf9: laga diya')
