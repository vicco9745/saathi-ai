p = 'app/main.py'
s = open(p, encoding='utf-8').read()
R = [
(r'''"Warna: {\"real\": false, \"title\": \"...\", \"scenes\": [\"...\", \"...\", \"...\"]}\n"''',
 r'''"Warna: {\"real\": false, \"title\": \"...\", \"scenes\": [{\"title\": \"2-4 shabd ka chhota drishya naam\", \"text\": \"...\"}, {\"title\": \"...\", \"text\": \"...\"}, {\"title\": \"...\", \"text\": \"...\"}]}\n"'''),
(r'''sc = [str(x).strip() for x in d.get("scenes", []) if str(x).strip()]''',
 r'''sc = [x for x in d.get("scenes", []) if (x.get("text") if isinstance(x, dict) else x)]'''),
(r'''return {"title": title, "scenes": [{"text": x} for x in sc[:6]]}''',
 r'''return {"title": title, "scenes": [({"title": str(x.get("title", "")).strip(), "text": str(x.get("text", "")).strip()} if isinstance(x, dict) else {"text": str(x).strip()}) for x in sc[:6]]}'''),
]
if '2-4 shabd' in s:
    print('story2 server: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story2 server: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story2 server: laga diya')
