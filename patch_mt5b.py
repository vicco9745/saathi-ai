pc = 'app/mt5_chart.py'
pp = 'app/pdf_multilang.py'
c = open(pc, encoding='utf-8').read()
q = open(pp, encoding='utf-8').read()
RC = [
("fig, ax = plt.subplots(figsize=(7, 4.6), dpi=150)", "fig, ax = plt.subplots(figsize=(7, 6.2), dpi=150)"),
("ax.text(0.01, y, left, transform=tr, color=color, fontsize=8, va='bottom', ha='left', zorder=5)",
 "ax.annotate(left, xy=(0.01, y), xycoords=tr, xytext=(0, 3), textcoords='offset points', color=color, fontsize=8, va='bottom', ha='left', zorder=5)"),
]
RQ = [
("if bt == 'chart':\n            _np(90)", "if bt == 'chart':\n            _np(150 if bd.get('type') == 'candlestick' else 90)"),
("max(60, (pdf.h - y - 30) * 7 / 4)", "max(60, (pdf.h - y - 30) * (7 / 6.2 if ctype == 'candlestick' else 7 / 4))"),
]
if '7, 6.2' in c:
    print('mt5b: pehle se laga hai')
else:
    bad = [('c', i) for i, (a, b) in enumerate(RC) if c.count(a) != 1] + [('q', i) for i, (a, b) in enumerate(RQ) if q.count(a) != 1]
    if bad:
        print('mt5b: jagah nahi mili', bad)
    else:
        for a, b in RC:
            c = c.replace(a, b, 1)
        for a, b in RQ:
            q = q.replace(a, b, 1)
        open(pc, 'w', encoding='utf-8').write(c)
        open(pp, 'w', encoding='utf-8').write(q)
        print('mt5b: laga diya')
