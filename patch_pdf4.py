pm = 'app/main.py'
pp = 'app/pdf_multilang.py'
m = open(pm, encoding='utf-8').read()
q = open(pp, encoding='utf-8').read()
PAGE_FN = r'''def _pdf_page_from_prompt(t):
    import re as _r
    t = (t or "").lower()
    S = {"a0": (841, 1189), "a1": (594, 841), "a2": (420, 594), "a3": (297, 420), "a4": (210, 297), "a5": (148, 210), "a6": (105, 148),
         "letter": (215.9, 279.4), "legal": (215.9, 355.6), "tabloid": (279.4, 431.8)}
    fmt = S["a4"]
    cm = _r.search(r"(\d+(?:\.\d+)?)\s*(?:x|×|by)\s*(\d+(?:\.\d+)?)\s*(mm|cm|inch|in)\b", t)
    ak = _r.search(r"\ba([0-6])\b", t)
    if cm:
        f = {"mm": 1.0, "cm": 10.0, "inch": 25.4, "in": 25.4}[cm.group(3)]
        w, h = float(cm.group(1)) * f, float(cm.group(2)) * f
        if 50 <= w <= 1500 and 50 <= h <= 1500:
            fmt = (min(w, h), max(w, h))
    elif ak:
        fmt = S["a" + ak.group(1)]
    elif _r.search(r"\btabloid\b", t):
        fmt = S["tabloid"]
    elif _r.search(r"us letter|\bletter (size|format|page)", t):
        fmt = S["letter"]
    elif _r.search(r"\blegal (size|format|page|paper)", t):
        fmt = S["legal"]
    orient = "L" if _r.search(r"landscape|horizontal|आड़ा|आड़े|चौड़ा", t) else "P"
    return fmt, orient

'''
TYPES = '''        "DOCUMENT TYPES: adapt the structure to the request. Invoice or bill: title, a table of items with quantity, rate and amount, then totals and payment details as empty [fill in] fields. "
        "Resume or CV: the name as h1, then Summary, Experience, Education, Skills. Certificate: short formal text with [name] and [date] fields. "
        "Report about a city, country, market, company or topic: introduction, key facts, several sections, a table of key figures, conclusion. "
        "Book or story: chapters as h2 with full flowing paragraphs. Notes or study material: headings, short points, examples. "
        "Budget, trading or profit and loss: tables with the columns the user gave, plus a summary box. Catalogue or brochure: a section per product or service with a short description table. "
'''
ACC_OLD = '''        "ACCURACY: never invent prices, market data, trading results, statistics, names or facts. "
        "Use only data the user supplied. Where data is needed but missing, leave a clearly marked empty field such as [fill in] in the table. "
'''
ACC_NEW = '''        "ACCURACY: write well-known general facts (history, geography, how things work) correctly and in full. "
        "Never invent live or specific numbers: prices, market data, trading results, statistics, personal names, dates of events you are unsure about. "
        "Use only numbers the user supplied; where such a number is needed but missing, leave a clearly marked [fill in] in the table. "
'''
Q_OLD = '        "QUALITY: no repeated'
CALL_OLD = 'pdf_bytes = _build_pdf_multilang(html_body, theme=_pdf_theme_from_prompt(body.prompt))'
CALL_NEW = '_pg = _pdf_page_from_prompt(body.prompt)\n        pdf_bytes = _build_pdf_multilang(html_body, theme=_pdf_theme_from_prompt(body.prompt), page_format=_pg[0], orientation=_pg[1])'
DEF_OLD = 'def _build_pdf_multilang(html_body: str, theme: str = "auto") -> bytes:'
DEF_NEW = 'def _build_pdf_multilang(html_body: str, theme: str = "auto", page_format=(210, 297), orientation="P") -> bytes:'
FPDF_OLD = "pdf = _FPDF(format='A4')"
FPDF_NEW = "pdf = _FPDF(orientation=orientation, format=page_format)"
IMG_OLD = "pdf.image(tpath, x=18, y=y, w=pdf.w - 36)"
IMG_NEW = "_cw = min(pdf.w - 36, max(60, (pdf.h - y - 30) * 7 / 4)); pdf.image(tpath, x=(pdf.w - _cw) / 2, y=y, w=_cw)"
if '_pdf_page_from_prompt' in m:
    print('pdf4: pehle se laga hai')
else:
    bad = []
    if m.count(ACC_OLD) != 1: bad.append('accuracy')
    if m.count(Q_OLD) != 1: bad.append('quality')
    if m.count(CALL_OLD) != 1: bad.append('call')
    if m.count('def _pdf_theme_from_prompt(t):') != 1: bad.append('themefn')
    if q.count(DEF_OLD) != 1: bad.append('def')
    if q.count(FPDF_OLD) != 1: bad.append('fpdf')
    if bad:
        print('pdf4: jagah nahi mili', bad)
    else:
        m = m.replace(ACC_OLD, ACC_NEW, 1)
        m = m.replace(Q_OLD, TYPES + Q_OLD, 1)
        m = m.replace(CALL_OLD, CALL_NEW, 1)
        m = m.replace('def _pdf_theme_from_prompt(t):', PAGE_FN + 'def _pdf_theme_from_prompt(t):', 1)
        q = q.replace(DEF_OLD, DEF_NEW, 1)
        q = q.replace(FPDF_OLD, FPDF_NEW, 1)
        if q.count(IMG_OLD) == 1:
            q = q.replace(IMG_OLD, IMG_NEW, 1)
        else:
            print('pdf4: chart ki chaudai wali line nahi mili, wo hissa chhoda')
        open(pm, 'w', encoding='utf-8').write(m)
        open(pp, 'w', encoding='utf-8').write(q)
        print('pdf4: laga diya')
