p = 'index.html'
s = open(p, encoding='utf-8').read()
I = r"""const __bI={plus:'<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',user:'<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',rupee:'<svg viewBox="0 0 24 24"><path d="M6 4h12M6 9h12M9 4c5 0 7 2 7 5s-2 5-7 5h-3l8 7"/></svg>',list:'<svg viewBox="0 0 24 24"><path d="M9 6h11M9 12h11M9 18h11"/><path d="m3.5 6 1.5 1.5L7.5 5M3.5 12l1.5 1.5L7.5 11M3.5 18l1.5 1.5L7.5 17"/></svg>',save:'<svg viewBox="0 0 24 24"><path d="M5 3h11l4 4v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M8 3v5h7V3M8 21v-7h8v7"/></svg>'};
"""
CSS = r""".bd-neg{color:var(--danger)}
.bd-card,.bd-pg{--bd-p:#5b35e8;--bd-p2:#7a4cf5;--bd-soft:#ece8ff;--bd-ink:#1b1464;--bd-bd:#cfc8f3;--bd-bg:#ffffff;--bd-mut:#8a86b0}
[data-theme="dark"] .bd-card,[data-theme="dark"] .bd-pg{--bd-soft:#2a2550;--bd-ink:#ece9ff;--bd-bd:#4a4290;--bd-bg:#1c1a33;--bd-mut:#9a96c8}
.bd-card{background:linear-gradient(180deg,var(--bd-soft),var(--panel-bg) 55%);border-color:var(--bd-bd);box-shadow:0 6px 20px rgba(91,53,232,.10)}
.bd-head{display:inline-flex;align-items:center;gap:12px;background:var(--bd-soft);border-radius:18px;padding:6px 18px 6px 6px;margin-bottom:16px}
.bd-plus{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,var(--bd-p2),var(--bd-p));color:#fff;display:flex;align-items:center;justify-content:center}
.bd-plus svg{width:24px;height:24px;stroke-width:2.6}
.bd-htxt{font-size:19px;font-weight:700;color:var(--bd-ink)}
.bd-title{color:var(--bd-ink)}
.bd-fld{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px}
.bd-ic{width:42px;height:42px;border-radius:50%;background:var(--bd-soft);color:var(--bd-p);display:flex;align-items:center;justify-content:center;flex:none;margin-top:2px}
.bd-ic svg{width:22px;height:22px}
.bd-fb{flex:1;min-width:0}
.bd-lbl{font-size:16px;font-weight:700;color:var(--bd-ink);margin:0 0 6px}
.bd-lbl i{color:#e5484d;font-style:normal}
.bd-in{border:1.5px solid var(--bd-bd);background:var(--bd-bg);color:var(--bd-ink);border-radius:14px;padding:12px 14px}
.bd-in::placeholder{color:var(--bd-mut)}
.bd-in:focus{border-color:var(--bd-p);box-shadow:0 0 0 3px rgba(91,53,232,.15)}
.bd-chk{color:var(--bd-ink)}
.bd-chk input{accent-color:var(--bd-p)}
.bd-btn.primary{background:linear-gradient(135deg,var(--bd-p2),var(--bd-p));border:0;color:#fff;border-radius:16px;padding:15px;font-size:18px;font-weight:700;box-shadow:0 8px 18px rgba(91,53,232,.30)}
.bd-btn.primary svg{width:22px;height:22px}
.bd-kpis div{background:var(--bd-soft)}
.bd-kpis b,.bd-sum b{color:var(--bd-ink)}
.bd-kpis b.bd-neg,.bd-sum b.bd-neg{color:var(--danger)}
"""
R = [
(r""".bd-neg{color:var(--danger)}
`;document.head.appendChild(c);}""", CSS + r"""`;document.head.appendChild(c);}"""),
(r"""function __bCss(){""", I + r"""function __bCss(){"""),
(r"""'<div class="bd-title">नया बजट</div>'""",
 r"""'<div class="bd-head"><span class="bd-plus">'+__bI.plus+'</span><span class="bd-htxt">नया बजट</span></div>'"""),
(r"""'<label class="bd-lbl">नाम</label><input class="bd-in" id="bn" placeholder="जैसे: घर का बजट" value="'+__bEsc(d.name||'')+'">'""",
 r"""'<div class="bd-fld"><span class="bd-ic">'+__bI.user+'</span><div class="bd-fb"><label class="bd-lbl">नाम <i>*</i></label><input class="bd-in" id="bn" placeholder="जैसे: घर का बजट" value="'+__bEsc(d.name||'')+'"></div></div>'"""),
(r"""'<label class="bd-lbl">कुल बजट (₹)</label><input class="bd-in" id="bt" type="number" inputmode="decimal" value="'+__bEsc(d.total||'')+'">'""",
 r"""'<div class="bd-fld"><span class="bd-ic">'+__bI.rupee+'</span><div class="bd-fb"><label class="bd-lbl">कुल बजट (₹) <i>*</i></label><input class="bd-in" id="bt" type="number" inputmode="decimal" placeholder="रकम लिखो" value="'+__bEsc(d.total||'')+'"></div></div>'"""),
(r"""'<label class="bd-lbl">खर्च — टिक लगाओ और रकम भरो</label>'""",
 r"""'<div class="bd-fld" style="margin-bottom:8px"><span class="bd-ic">'+__bI.list+'</span><div class="bd-fb"><label class="bd-lbl" style="margin:10px 0 0">खर्च — टिक लगाओ और रकम भरो</label></div></div>'"""),
(r"""'<div class="bd-err" id="be"></div><button class="bd-btn primary" id="bsub">सबमिट</button>'""",
 r"""'<div class="bd-err" id="be"></div><button class="bd-btn primary" id="bsub">'+__bI.save+'सबमिट</button>'"""),
]
if 'const __bI=' in s:
    print('budget2: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('budget2: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget2: laga diya')
