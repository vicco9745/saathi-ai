p='index.html'
s=open(p,encoding='utf-8').read()
unl="""/*sndunlock74*/function __sndUnlock(){try{var AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!__sndCtx||__sndCtx.state==='closed')__sndCtx=new AC();if(__sndCtx.state!=='running')__sndCtx.resume();}catch(_){}}['pointerdown','touchstart','click','keydown'].forEach(function(e){document.addEventListener(e,__sndUnlock,true);});
"""
pairs=[
("function startCall(){__snd('open');", unl+"function startCall(){__snd('open');"),
("if(callActive)setTimeout(function(){__snd('end');},220);", "if(callActive)__snd('end');"),
("updateCallActionButton();setTimeout(listenOnce,450);}", "updateCallActionButton();listenOnce();}"),
]
if 'sndunlock74' in s:
    print('sndunlock: pehle se laga hai')
else:
    cnt=[s.count(a) for a,b in pairs]
    if cnt==[1,1,1]:
        for a,b in pairs:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('sndunlock: laga diya')
    else:
        print('sndunlock: jagah nahi mili',cnt)
