p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r"""__buildBudgetCard(m,row);messagesList.appendChild(row);return;}""",
 r"""__buildBudgetCard(m,row);if(m.budget.mode==='form'){const _ac=buildMessageActions(m,idx,chat,idx===lastAiIdx);window.__bAct=window.__bAct||new Map();window.__bAct.set(m,_ac);if(typeof m.__ba==='number'&&!m.__bdone)_ac.style.display='none';row.appendChild(_ac);}messagesList.appendChild(row);return;}"""),
(r"""const g=sg(__bGuideText(u));""", r"""m.text=__bGuideText(u);const g=sg(m.text);"""),
(r"""if(c>=total){clearInterval(id);m.__bdone=true;try{saveChats();}catch(_){}}""",
 r"""if(c>=total){clearInterval(id);m.__bdone=true;try{const _a=window.__bAct&&window.__bAct.get(m);if(_a)_a.style.display='';}catch(_){}try{saveChats();}catch(_){}}"""),
(r"""if(el.__gb)el.__gb.remove();""",
 r"""if(el.__gb)el.__gb.remove();try{const _a=window.__bAct&&window.__bAct.get(m);if(_a)_a.remove();}catch(_){}m.text='';"""),
]
if "window.__bAct.set(m,_ac)" in s:
    print('budget10: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('budget10: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget10: laga diya')
