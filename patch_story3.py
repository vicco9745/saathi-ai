p = 'app/main.py'
s = open(p, encoding='utf-8').read()
R = [
(r'''"Antim scene par ruk jao: koi seekh, nichod, sawaal ya 'aur sunaun' jaisa vakya nahi."''',
 r'''"Antim scene par ruk jao: koi seekh, nichod, sawaal ya 'aur sunaun' jaisa vakya nahi. "
    "JSON mein scenes ke bahar ek key \"note\" bhi do: usi bhasha mein 1-2 chhote vakya jo bataye ki kahani kis baare mein hai aur teen drishyon mein taiyaar hai; "
    "koi seekh nahi, koi sawaal nahi, 'aur sunaun' jaisa kuch nahi, koi emoji nahi."'''),
(r'''return {"title": title, "scenes": [(''',
 r'''return {"note": str(d.get("note", "")).strip(), "title": title, "scenes": [('''),
(r'''"reply": "", "story": _st,''',
 r'''"reply": _st.get("note", ""), "story": _st,'''),
]
if '"note"' in s:
    print('story3 server: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story3 server: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story3 server: laga diya')
