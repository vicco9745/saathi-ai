p='index.html'
s=open(p,encoding='utf-8').read()
snd="""/*callsnd72*/var __sndCtx=null;function __snd(k){try{var AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;if(!__sndCtx)__sndCtx=new AC();var c=__sndCtx;if(c.state==='suspended')c.resume();var seq={open:[[660,0],[880,.11]],end:[[660,0],[440,.11]],mute:[[330,0]],unmute:[[520,0]]}[k]||[];var t0=c.currentTime;seq.forEach(function(n){var o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=n[0];g.gain.setValueAtTime(0.0001,t0+n[1]);g.gain.exponentialRampToValueAtTime(0.12,t0+n[1]+0.02);g.gain.exponentialRampToValueAtTime(0.0001,t0+n[1]+0.16);o.connect(g);g.connect(c.destination);o.start(t0+n[1]);o.stop(t0+n[1]+0.2);});}catch(_){}}
"""
pairs=[
("function startCall(){callActive=true;callMuted=false;", snd+"function startCall(){__snd('open');callActive=true;callMuted=false;"),
("function stopCall(){callActive=false;callMuted=false;", "function stopCall(){try{if(callActive)__snd('end');}catch(_){}callActive=false;callMuted=false;"),
("callDictateBtn.addEventListener('click',()=>{callMuted=!callMuted;", "callDictateBtn.addEventListener('click',()=>{callMuted=!callMuted;__snd(callMuted?'mute':'unmute');"),
]
if 'callsnd72' in s:
    print('callsnd: pehle se laga hai')
else:
    cnt=[s.count(a) for a,b in pairs]
    if cnt==[1,1,1]:
        for a,b in pairs:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('callsnd: laga diya')
    else:
        print('callsnd: jagah nahi mili',cnt)
