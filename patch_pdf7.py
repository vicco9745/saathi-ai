pm = 'app/main.py'
pp = 'app/pdf_multilang.py'
m = open(pm, encoding='utf-8').read()
q = open(pp, encoding='utf-8').read()
R_Q = [
(r"""    html = _re.sub(r'(<<(?:CHART|IMG|BOX|TABLE)_B_\d+>>|<<PAGEBREAK_B>>)', r'<p>\1</p>', html)""",
 r"""    html = _re.sub(r'<<((?:CHART|IMG|BOX|TABLE)_B_\d+|PAGEBREAK_B)>>', r'<p>&lt;&lt;\1&gt;&gt;</p>', html)"""),
("SF('B', 14, T['accent2'] if T['light'] else T['accent'])",
 "SF('B', 14, T['accent2'] if T['light'] else T['bg'])"),
]
R_M = [
('"premium", "gold", "black"', '"premium", "golden", "black"'),
('"business", "report", "stock", "market", "trading",', '"business", "report", "stock", "market", "trading", "candle", "xauusd", "forex", "chart",'),
]
if '&lt;&lt;' in q:
    print('pdf7: pehle se laga hai')
else:
    bad = [('q', i) for i, (a, b) in enumerate(R_Q) if q.count(a) != 1] + [('m', i) for i, (a, b) in enumerate(R_M) if m.count(a) != 1]
    if bad:
        print('pdf7: jagah nahi mili', bad)
    else:
        for a, b in R_Q:
            q = q.replace(a, b, 1)
        for a, b in R_M:
            m = m.replace(a, b, 1)
        open(pp, 'w', encoding='utf-8').write(q)
        open(pm, 'w', encoding='utf-8').write(m)
        print('pdf7: laga diya')
