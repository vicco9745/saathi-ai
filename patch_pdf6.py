pm = 'app/main.py'
pp = 'app/pdf_multilang.py'
m = open(pm, encoding='utf-8').read()
q = open(pp, encoding='utf-8').read()
P_OLD = "    parser = _P()\n"
P_NEW = r"""    html = _re.sub(r'(<<(?:CHART|IMG|BOX|TABLE)_B_\d+>>|<<PAGEBREAK_B>>)', r'<p>\1</p>', html)
    parser = _P()
"""
S_OLD = r"""    import os, re, datetime
    from concurrent.futures import ThreadPoolExecutor
"""
S_NEW = S_OLD + r"""    if len(re.findall(r"\d", prompt or "")) > 40:
        return ""
"""
Q_OLD = '        "QUALITY: no repeated'
Q_NEW = r'''        "WHEN THE USER SUPPLIED DATA (candles, numbers, a table): use only that data and keep the text short: title, one summary line, the chart or table, and a small table of the given levels. "
        "Do not add analysis, pip counts, strategy, reasons, history, code examples or any fact the user did not give, and never write the word chart or box tag in the text. "
        "Every chart and box tag must stand on its own line, not inside a sentence. "
''' + Q_OLD
if 'WHEN THE USER SUPPLIED DATA' in m:
    print('pdf6: pehle se laga hai')
else:
    bad = []
    if q.count(P_OLD) != 1: bad.append('parser')
    if m.count(S_OLD) != 1: bad.append('search')
    if m.count(Q_OLD) != 1: bad.append('prompt')
    if bad:
        print('pdf6: jagah nahi mili', bad)
    else:
        q = q.replace(P_OLD, P_NEW, 1)
        m = m.replace(S_OLD, S_NEW, 1)
        m = m.replace(Q_OLD, Q_NEW, 1)
        open(pm, 'w', encoding='utf-8').write(m)
        open(pp, 'w', encoding='utf-8').write(q)
        print('pdf6: laga diya')
