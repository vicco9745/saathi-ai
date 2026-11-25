p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r"""const st=m.story||{};const sc=Array.isArray(st.scenes)?st.scenes:[];""",
 r"""const st=m.story||{};const sc=Array.isArray(st.scenes)?st.scenes:[];const ui=(st.ui&&typeof st.ui==='object')?st.ui:{};const L=function(k,d){return String(ui[k]||d);};"""),
(r"""const mins=st.minutes||Math.max(1,Math.round(full.length/900));""",
 r"""const mins=st.minutes||Math.max(1,Math.round(full.length/900));const rdl=L('read','{n} मिनट पढ़ने में');const rd=rdl.indexOf('{n}')>-1?rdl.split('{n}').join(mins):mins+' '+rdl;"""),
(r"""${mins} मिनट पढ़ने में""", r"""${esc(rd)}"""),
(r"""</svg>कहानी</span>""", r"""</svg>${esc(L('story','कहानी'))}</span>"""),
(r"""<span class="st-cap">दृश्य ${i+1}""", r"""<span class="st-cap">${esc(L('scene','दृश्य'))} ${i+1}"""),
(r"""'<div class="st-div"><span>दृश्य '+(i+1)+'</span></div>'""",
 r"""'<div class="st-div"><span>'+esc(L('scene','दृश्य'))+' '+(i+1)+'</span></div>'"""),
(r"""<polygon points="6 4 20 12 6 20 6 4"/></svg>सुनो</button>""",
 r"""<polygon points="6 4 20 12 6 20 6 4"/></svg>${esc(L('listen','सुनो'))}</button>"""),
(r"""<path d="M21 4v5h-5"/></svg>फिर से</button>""",
 r"""<path d="M21 4v5h-5"/></svg>${esc(L('again','फिर से'))}</button>"""),
(r"""<path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>कॉपी</button>""",
 r"""<path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>${esc(L('copy','कॉपी'))}</button>"""),
(r"""<path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>शेयर</button>""",
 r"""<path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>${esc(L('share','शेयर'))}</button>"""),
(r"""u.lang='hi-IN';""", r"""u.lang=st.lang||'hi-IN';"""),
]
if "L('story'" in s:
    print('story6: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story6: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story6: laga diya')
