p='index.html'
s=open(p,encoding='utf-8').read()
pairs=[
("b.style.bottom=(r?Math.max(10,window.innerHeight-r.top+10):90)+'px';", "b.style.top='57%';/*ratemid78*/"),
("function __callRate(){try{", "function __callRate(){if(!window.__callTalked)return;try{"),
("function addLiveUserText(text){", "function addLiveUserText(text){window.__callTalked=true;"),
("function startCall(){__snd('open');", "function startCall(){window.__callTalked=false;__snd('open');"),
]
if 'ratemid78' in s:
    print('ratemid: pehle se laga hai')
else:
    cnt=[s.count(a) for a,b in pairs]
    if cnt==[1,1,1,1]:
        for a,b in pairs:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('ratemid: laga diya')
    else:
        print('ratemid: jagah nahi mili',cnt)
