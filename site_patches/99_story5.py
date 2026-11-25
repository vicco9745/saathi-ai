p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r"""__buildStoryCard2(m,row);messagesList.appendChild(row);return;}""",
 r"""__buildStoryCard2(m,row);{const _ac=buildMessageActions(m,idx,chat,idx===lastAiIdx);if(typeof m.__sc==='number'&&!m.__sdone){_ac.style.display='none';window.__stAct=window.__stAct||new Map();window.__stAct.set(m,_ac);}row.appendChild(_ac);}messagesList.appendChild(row);return;}"""),
(r"""function fin(){if(nb)nb.innerHTML=linkifyText(String(m.text));}""",
 r"""function fin(){if(nb)nb.innerHTML=linkifyText(String(m.text));try{const _a=window.__stAct&&window.__stAct.get(m);if(_a)_a.style.display='';}catch(_){}}"""),
]
if '__stAct' in s:
    print('story5: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story5: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story5: laga diya')
