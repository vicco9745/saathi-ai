p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r""".st-pic{width:100%;aspect-ratio:16/10;background:var(--page-bg);border:1px dashed var(--border);border-radius:16px;margin-bottom:12px}""",
 r""".st-pic{width:100%;aspect-ratio:7/3;background:var(--st-bg,#ddd9fb);border-radius:18px;margin-bottom:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:var(--st-fg,#5b45c9);padding:12px;text-align:center}
.st-pic svg{width:44px;height:44px;stroke-width:1.6}
.st-cap{font-size:15px;font-weight:500}
[data-theme="dark"] .story-card{--st-bg:#2b2850;--st-fg:#b9aeff}
.st-div{display:flex;align-items:center;gap:12px;color:var(--text-muted);font-size:14px;margin:4px 0 16px}
.st-div:before,.st-div:after{content:"";flex:1;height:1px;background:var(--border)}"""),
(r""".story-actions{display:flex;gap:10px;flex-wrap:wrap;border-top:1px solid var(--border);padding-top:16px}""",
 r""".story-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;border-top:1px solid var(--border);padding-top:16px}"""),
(r""".story-btn{display:inline-flex;align-items:center;gap:8px;""",
 r""".story-btn{display:inline-flex;justify-content:center;align-items:center;gap:8px;"""),
(r"""${sc.map(x=>`<div class="st-scene"><div class="st-pic"></div><p>${esc(x.text)}</p></div>`).join('')}""",
 r"""${sc.map((x,i)=>`${i?'<div class="st-div"><span>दृश्य '+(i+1)+'</span></div>':''}<div class="st-scene"><div class="st-pic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="1.6"/><path d="m21 15-5-5L5 21"/></svg><span class="st-cap">दृश्य ${i+1}${x.title?': '+esc(x.title):''}</span></div><p>${esc(x.text)}</p></div>`).join('')}"""),
(r"""story-btn primary st-listen""", r"""story-btn st-listen"""),
(r"""<svg viewBox="0 0 24 24"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>सुनो""",
 r"""<svg viewBox="0 0 24 24"><polygon points="6 4 20 12 6 20 6 4"/></svg>सुनो"""),
]
if 'st-cap' in s:
    print('story2: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story2: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story2: laga diya')
