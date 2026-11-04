import os
src = open('.new_pdf_func.py', encoding='utf-8').read()
if 'def _build_pdf_multilang' not in src:
    print('pdffix: function nahi mili')
    raise SystemExit
out = []
if not os.path.exists('app/pdf_multilang.py'):
    open('app/pdf_multilang.py', 'w', encoding='utf-8').write(src)
    out.append('module: bana diya')
else:
    out.append('module: pehle se hai')
r = open('requirements.txt', encoding='utf-8').read()
if 'fpdf2' not in r:
    open('requirements.txt', 'w', encoding='utf-8').write(r.rstrip('\n') + '\nfpdf2\n')
    out.append('requirements: fpdf2 joda')
else:
    out.append('requirements: pehle se hai')
p = 'app/main.py'
s = open(p, encoding='utf-8').read()
R = [
    ('\n    from xhtml2pdf import pisa\n', '\n'),
    ('    pdf_buffer = BytesIO()\n    pisa.CreatePDF(full_html, dest=pdf_buffer, encoding="utf-8")\n    pdf_bytes = pdf_buffer.getvalue()\n    pdf_buffer.close()\n',
     '    try:\n        from app.pdf_multilang import _build_pdf_multilang\n        pdf_bytes = _build_pdf_multilang(html_body)\n    except Exception as e:\n        raise HTTPException(500, "PDF banane mein problem: " + str(e))\n'),
    ('            from xhtml2pdf import pisa as _pisa\n', ''),
    ('            buf = _BIO()\n            _pisa.CreatePDF(full_html, dest=buf, encoding="utf-8")\n            pdf_b64 = _b64.b64encode(buf.getvalue()).decode("utf-8")\n            buf.close()\n',
     '            from app.pdf_multilang import _build_pdf_multilang\n            pdf_b64 = _b64.b64encode(_build_pdf_multilang(html_body)).decode("utf-8")\n'),
]
if 'app.pdf_multilang' in s:
    out.append('main.py: pehle se laga hai')
elif all(s.count(a) == 1 for a, b in R):
    for a, b in R:
        s = s.replace(a, b, 1)
    open(p, 'w', encoding='utf-8').write(s)
    out.append('main.py: laga diya')
else:
    out.append('main.py: jagah nahi mili %s' % [s.count(a) for a, b in R])
print('\n'.join(out))
