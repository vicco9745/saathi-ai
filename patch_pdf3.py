p = 'app/pdf_multilang.py'
s = open(p, encoding='utf-8').read()
R = [
("bh = pdf.h * 0.42", "bh = pdf.h * 0.24"),
("pdf.set_xy(20, bh * 0.32)", "pdf.set_xy(20, bh * 0.28)"),
("cy = bh * 0.32 + 30", "cy = bh - 12"),
("        pdf.set_y(bh + 25)\n        skipped = True\n", "        pdf.set_y(bh + 16)\n        skipped = False\n"),
("    total = pdf.page_no()\n", "    total = pdf.page_no()\n    pdf.set_auto_page_break(auto=False)\n"),
]
if 'bh = pdf.h * 0.24' in s:
    print('pdf3: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('pdf3: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('pdf3: laga diya')
