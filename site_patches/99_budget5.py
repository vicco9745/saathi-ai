p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r"""const list=__bLoad();const low=t.toLowerCase();""",
 r"""window.__bT=t;const list=__bLoad();const low=t.toLowerCase();"""),
(r"""try{const c=getCurrentChat();if(c&&c.title==='New chat'){c.title=__bU(b.ui).L.budget;c.__autoTitle=false;}}catch(_){}""",
 r"""try{const c=getCurrentChat();if(c&&c.title==='New chat'){const _L=(b.ui&&b.ui.labels&&b.ui.labels.budget)||'';const _t=String(window.__bT||'').trim();c.title=_L||(_t.length>28?_t.slice(0,28)+'…':_t)||__bU(b.ui).L.budget;c.__autoTitle=false;}}catch(_){}"""),
]
if 'window.__bT=t;' in s:
    print('budget5 site: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('budget5 site: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget5 site: laga diya')
