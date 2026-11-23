import re
p='index.html'
s=open(p,encoding='utf-8').read()
fn="""/*sndfix73*/var __sndCtx=null;function __snd(k){try{var AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!__sndCtx||__sndCtx.state==='closed')__sndCtx=new AC();var c=__sndCtx;var seq={open:[[660,0],[880,.12]],end:[[660,0],[440,.12]],mute:[[330,0]],unmute:[[520,0]]}[k]||[];var go=function(){var t0=c.currentTime+0.03;seq.forEach(function(n){var o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=n[0];g.gain.setValueAtTime(0.0001,t0+n[1]);g.gain.exponentialRampToValueAtTime(0.45,t0+n[1]+0.02);g.gain.exponentialRampToValueAtTime(0.0001,t0+n[1]+0.2);o.connect(g);g.connect(c.destination);o.start(t0+n[1]);o.stop(t0+n[1]+0.25);});};if(c.state==='running')go();else c.resume().then(go).catch(go);}catch(_){}}
"""
pat=re.compile(r"var __sndCtx=null;function __snd\(k\)\{[^\n]*\n")
o2="function stopCall(){try{if(callActive)__snd('end');}catch(_){}callActive=false;"
n2="function stopCall(){try{if(callActive)setTimeout(function(){__snd('end');},220);}catch(_){}callActive=false;"
o3="callOverlay.classList.remove('chat-open');updateCallActionButton();listenOnce();}"
n3="callOverlay.classList.remove('chat-open');updateCallActionButton();setTimeout(listenOnce,450);}"
if 'sndfix73' in s:
    print('sndfix: pehle se laga hai')
else:
    cnt=[len(pat.findall(s)),s.count(o2),s.count(o3)]
    if cnt==[1,1,1]:
        s=pat.sub(lambda m:fn,s,count=1).replace(o2,n2,1).replace(o3,n3,1)
        open(p,'w',encoding='utf-8').write(s)
        print('sndfix: laga diya')
    else:
        print('sndfix: jagah nahi mili',cnt)
