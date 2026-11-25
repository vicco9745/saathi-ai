p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r"""m.text='';m.story=d.story;""",
 r"""m.text=String(d.reply||(d.story&&d.story.note)||'');m.story=d.story;"""),
(r"""if(m.role==='ai'&&m.story&&!m.typing){row.appendChild(__buildStoryCard(m));messagesList.appendChild(row);return;}""",
 r"""if(m.role==='ai'&&m.story&&!m.typing){row.appendChild(__buildStoryCard(m));if(m.text){const _sb=document.createElement('div');_sb.className='bubble';_sb.innerHTML=linkifyText(m.text);row.appendChild(_sb);}messagesList.appendChild(row);return;}"""),
]
if 'const _sb=' in s:
    print('story3: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story3: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story3: laga diya')
