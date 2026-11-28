pp = 'app/pdf_multilang.py'
pm = 'app/main.py'
q = open(pp, encoding='utf-8').read()
m = open(pm, encoding='utf-8').read()
THEME = '''        "guide": {"bg": (255,255,255), "text": (33,43,54), "accent": (26,54,93), "accent2": (47,111,190), "muted": (110,120,135), "header_band": (232,240,254), "header_text": (26,54,93), "light": True, "guide": True},
'''
A_MK = '        "auto": {"bg": (255,255,255), "text": (26,26,46), "accent": (16,163,127)'
T_OLD = "    if title:\n        bh = pdf.h * 0.24\n"
T_NEW = '''    if title and T.get('guide'):
        pdf.set_y(28)
        SF('B', 24, T['accent'])
        pdf.multi_cell(0, 12, title[:90], align='C')
        _gy = pdf.get_y() + 3
        pdf.set_draw_color(205, 215, 230); pdf.set_line_width(0.4)
        pdf.line(18, _gy, pdf.w - 18, _gy)
        pdf.set_y(_gy + 8)
        skipped = False
    elif title:
        bh = pdf.h * 0.24
'''
H_OLD = "        if bt == 'h1':\n            pdf.ln(4); y = pdf.get_y()\n"
H_NEW = '''        if T.get('guide') and bt in ('h1', 'h2', 'h3'):
            if bt == 'h3':
                pdf.ln(2); SF('B', 13, T['accent2']); pdf.multi_cell(0, 8, bd); pdf.ln(1.5)
            else:
                pdf.ln(4 if bt == 'h1' else 3); SF('B', 18 if bt == 'h1' else 15, T['accent']); pdf.multi_cell(0, 9, bd); pdf.ln(1.5)
        elif bt == 'h1':
            pdf.ln(4); y = pdf.get_y()
'''
F_OLD = "        pdf.set_y(pdf.h - 15)\n        SF('', 9, T['muted'])\n        pdf.cell(0, 6, '— ' + str(i) + ' —', align='C')\n"
F_NEW = '''        if T.get('guide'):
            pdf.set_draw_color(215, 220, 230); pdf.set_line_width(0.3)
            pdf.line(18, pdf.h - 18, pdf.w - 18, pdf.h - 18)
            pdf.set_y(pdf.h - 15)
            SF('', 8, T['muted'])
            _tt = str(title or '')[:70]
            pdf.cell(pdf.w - 70, 6, _tt, align='L')
            pdf.cell(0, 6, ('पेज ' if _re.search(r'[\\u0900-\\u097F]', _tt) else 'Page ') + str(i), align='R')
        else:
            pdf.set_y(pdf.h - 15)
            SF('', 9, T['muted'])
            pdf.cell(0, 6, '— ' + str(i) + ' —', align='C')
'''
if '"guide": {' in q:
    print('guide: pehle se laga hai')
else:
    bad = []
    for nm, old in (('theme', A_MK), ('title', T_OLD), ('heading', H_OLD), ('footer', F_OLD)):
        if q.count(old) != 1: bad.append(nm)
    a = m.find('def _pdf_theme_from_prompt(t):')
    b = m.find('\n\n', a) if a >= 0 else -1
    seg = m[a:b] if a >= 0 and b > a else ''
    if seg.count('return "business"') != 1 or not seg.rstrip().endswith('return "auto"'):
        bad.append('main theme')
    if bad:
        print('guide: jagah nahi mili', bad)
    else:
        q = q.replace(A_MK, THEME + A_MK, 1)
        q = q.replace(T_OLD, T_NEW, 1)
        q = q.replace(H_OLD, H_NEW, 1)
        q = q.replace(F_OLD, F_NEW, 1)
        seg2 = seg.replace('return "business"', 'return "guide"').rstrip()
        seg2 = seg2[:-len('return "auto"')] + 'return "guide"'
        m = m[:a] + seg2 + m[b:]
        open(pp, 'w', encoding='utf-8').write(q)
        open(pm, 'w', encoding='utf-8').write(m)
        print('guide: laga diya')
