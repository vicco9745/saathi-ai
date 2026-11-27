p = 'app/main.py'
s = open(p, encoding='utf-8').read()
NEWFN = r'''def _pdf_long_html(prompt, ctx, system):
    import re, json, time
    from concurrent.futures import ThreadPoolExecutor
    t = prompt or ""
    full = t + (("\n\n" + ctx) if ctx else "")
    pw = r"(?:pages?|pgs?|पन्ने|पन्नों|पन्ना|पेज|पृष्ठ)"
    n = 0
    m = re.search(r"(\d{1,3})\s*[-]?\s*" + pw, t, re.I)
    if m:
        n = int(m.group(1))
    else:
        W = {"एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पाँच": 5, "पांच": 5, "छह": 6, "छः": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10,
             "बीस": 20, "तीस": 30, "चालीस": 40, "पचास": 50, "साठ": 60, "सत्तर": 70, "अस्सी": 80, "नब्बे": 90, "सौ": 100}
        m = re.search(r"(" + "|".join(W) + r")\s*" + pw, t)
        if m:
            n = W[m.group(1)]
    n = min(n, 100)
    if n < 4:
        return _call_groq(full, system=system)
    secs = []
    for st in range(0, n, 25):
        k = min(25, n - st)
        items = []
        try:
            o = _call_groq(
                t + "\n\nTITLES ALREADY PLANNED: " + " | ".join(str(x["title"]) for x in secs[-30:]),
                system=("You plan documents. The whole document has " + str(n) + " pages. Plan pages " + str(st + 1) + " to " + str(st + k) + ". "
                        "Reply with ONLY a JSON array of exactly " + str(k) + " objects, one per page, each like "
                        "{\"title\": \"short section title\", \"points\": \"what this page covers in one sentence\"}. "
                        "Do not repeat planned titles. Titles in the same language as the user's request. No markdown, no explanation."))
            o = (o or "").replace("```json", "").replace("```", "").strip()
            a = o.find("[")
            b = o.rfind("]")
            items = [x for x in json.loads(o[a:b + 1]) if isinstance(x, dict) and x.get("title")]
        except Exception as e:
            print("PDF outline error", repr(e)[:120])
        items = items[:k]
        while len(items) < k:
            items.append({"title": "Part " + str(st + len(items) + 1), "points": ""})
        secs.extend(items)
    titles = " | ".join(str(x.get("title")) for x in secs)[:3000]
    cx = ctx[:2500] if (ctx and n > 10) else ctx
    extra = (
        "\nYOU ARE WRITING ONE PAGE OF A LONGER DOCUMENT. Write ONLY the page you are asked for: an h2 heading and its content, about 220 words, "
        "as HTML with the allowed tags. Do not write html or body tags, and never repeat content of other pages. "
        "Put a chart, box or table tag only where it belongs on this page."
    )
    t0 = time.time()
    def one(i):
        if time.time() - t0 > 540:
            return None
        x = secs[i]
        head = "Start with the h1 title of the whole document and a one-line p subtitle, then the h2 heading of this page. " if i == 0 else ""
        last = " This is the last page: finish with a short conclusion." if i == len(secs) - 1 else ""
        up = ("DOCUMENT REQUEST:\n" + t + "\n\nFULL OUTLINE: " + titles + "\n\nWRITE ONLY PAGE " + str(i + 1) + " OF " + str(len(secs)) + ": "
              + str(x.get("title")) + " - " + str(x.get("points", "")) + ". " + head + last + (("\n\n" + cx) if cx else ""))
        for at in range(3):
            try:
                h = _call_groq(up, system=system + extra)
                h = (h or "").replace("```html", "").replace("```", "").strip()
                h = re.sub(r"</?(?:html|body|head)[^>]*>", "", h, flags=re.I).strip()
                if len(h) > 40:
                    return h
            except Exception as e:
                print("PDF section error", repr(e)[:120])
            time.sleep(2 * (at + 1))
        return "<h2>" + str(x.get("title")) + "</h2><p>[fill in]</p>"
    with ThreadPoolExecutor(max_workers=3) as ex:
        res = list(ex.map(one, range(len(secs))))
    parts = [r for r in res if r]
    if len(parts) < len(secs):
        parts.append("<p>[Stopped early: time limit reached, " + str(len(parts)) + " of " + str(len(secs)) + " pages written]</p>")
    return "<html>" + "<pagebreak/>".join(parts) + "</html>"

'''
if 'time.time() - t0 > 540' in s:
    print('pdf10: pehle se laga hai')
else:
    a = s.find('def _pdf_long_html(')
    b = s.find('def _pdf_theme_from_prompt(t):')
    if a < 0 or b < 0 or b < a:
        print('pdf10: jagah nahi mili', a, b)
    else:
        s = s[:a] + NEWFN + s[b:]
        open(p, 'w', encoding='utf-8').write(s)
        print('pdf10: laga diya')
