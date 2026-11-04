p = 'index.html'
s = open(p, encoding='utf-8').read()
old = "function __buildGenReplyNew(kind,o){\nif(kind!=='website')return __buildGenReplyOld(kind,o);"
new = "function __buildGenReplyNew(kind,o){\nif(kind==='pdf'){var _c=((o&&o.caption)||'').trim();if(_c.length>=40)return _c;}\nif(kind!=='website')return __buildGenReplyOld(kind,o);"
if "kind==='pdf'){var _c" in s:
    print('pdftext: pehle se laga hai')
elif s.count(old) == 1:
    open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('pdftext: laga diya')
else:
    print('pdftext: jagah nahi mili', s.count(old))
