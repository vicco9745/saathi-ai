p = 'app/main.py'
s = open(p, encoding='utf-8').read()
THEME_FN = r'''def _pdf_theme_from_prompt(t):
    t = (t or "").lower()
    if any(x in t for x in ["premium", "gold", "black", "luxury", "dark theme"]):
        return "premium"
    if any(x in t for x in ["colorful", "colourful", "rainbow", "kids", "रंगीन", "बच्चों"]):
        return "colorful"
    if any(x in t for x in ["book", "ebook", "e-book", "chapter", "novel", "किताब", "उपन्यास"]):
        return "book"
    if any(x in t for x in ["business", "report", "stock", "market", "trading", "profit", "invoice", "budget", "financial", "dark blue", "navy", "रिपोर्ट", "बिज़नेस", "बजट", "शेयर"]):
        return "business"
    return "auto"

'''
NEWSYS = r'''    system = (
        "You are a professional document writer. Write the document the user asks for as clean HTML. "
        "Reply with ONLY the HTML, from <html> to </html>, no markdown fences, no explanation, no CSS, no style attributes, no emoji. "
        "Write all text in the same language as the user's request. "
        "Allowed tags only: h1, h2, h3, p, ul, li, blockquote, table with tr, th and td, and <pagebreak/>. "
        "STRUCTURE: start with exactly one h1 as the document title, then one short p as a subtitle or purpose line. "
        "Then a short summary section (h2), then the main sections (h2), each with clear paragraphs, lists or tables, then a conclusion. "
        "Use tables wherever data is compared or listed (first row th headers, equal number of cells in every row). "
        "Put <pagebreak/> between major sections when the document is long (more than 2 pages). "
        "LENGTH: write enough real content for the number of pages the user asked for, about 300 words per page; if no length is given, 2 to 4 pages. "
        "ACCURACY: never invent prices, market data, trading results, statistics, names or facts. "
        "Use only data the user supplied. Where data is needed but missing, leave a clearly marked empty field such as [fill in] in the table. "
        "QUALITY: no repeated sentences, no filler, consistent headings, short paragraphs, no text that cuts off in the middle."
    )
'''
CALL_OLD = 'pdf_bytes = _build_pdf_multilang(html_body)'
CALL_NEW = 'pdf_bytes = _build_pdf_multilang(html_body, theme=_pdf_theme_from_prompt(body.prompt))'
if '_pdf_theme_from_prompt' in s:
    print('pdf1: pehle se laga hai')
else:
    st = s.find('def pdf(body: GenericRequest')
    en = s.find('@app.post("/v1/code")', st)
    a = s.find('    system = (', st)
    b = s.find('    html_body = _call_groq(body.prompt, system=system)', a)
    dec = s.rfind('@app.post("/v1/pdf")', 0, st)
    reg = s[st:en] if st >= 0 and en > st else ''
    if st < 0 or en < 0 or a < 0 or b < 0 or dec < 0 or not (a < b < en) or b - a > 1500 or reg.count(CALL_OLD) != 1:
        print('pdf1: jagah nahi mili', st, en, a, b, dec, reg.count(CALL_OLD))
    else:
        s = s[:a] + NEWSYS + s[b:]
        s = s.replace(CALL_OLD, CALL_NEW, 1)
        s = s[:dec] + THEME_FN + s[dec:]
        open(p, 'w', encoding='utf-8').write(s)
        print('pdf1: laga diya')
