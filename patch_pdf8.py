pp = 'app/pdf_multilang.py'
q = open(pp, encoding='utf-8').read()
OLD = "pdf.image(tpath, x=(pdf.w - _cw) / 2, y=y, w=_cw)"
NEW = "pdf.image(tpath, x=(pdf.w - _cw) / 2, y=y, w=_cw); pdf.set_y(y + _cw * (6.2 / 7 if ctype == 'candlestick' else 4 / 7))"
if 'pdf.set_y(y + _cw' in q:
    print('pdf8: pehle se laga hai')
elif q.count(OLD) != 1:
    print('pdf8: jagah nahi mili', q.count(OLD))
else:
    q = q.replace(OLD, NEW, 1)
    open(pp, 'w', encoding='utf-8').write(q)
    print('pdf8: laga diya')
