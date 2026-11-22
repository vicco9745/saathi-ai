p='index.html'
s=open(p,encoding='utf-8').read()
ch=0
o1="callDictateIcon.innerHTML=callMuted?MIC_OFF_SVG:MIC_ON_SVG;"
n1="callDictateIcon.innerHTML=callMuted?MIC_ON_SVG:MIC_OFF_SVG;/*micswap66*/"
if 'micswap66' not in s:
    if s.count(o1)==1:
        s=s.replace(o1,n1,1);ch+=1;print('micswap: laga diya')
    else:
        print('micswap: jagah nahi mili',s.count(o1))
else:
    print('micswap: pehle se laga hai')
o2="renderCallMicIcon();showToast(callMuted?'Mic band (mute)':'Mic chalu');});"
n2="renderCallMicIcon();/*micquiet67*/});"
if 'micquiet67' in s:
    print('micquiet: pehle se laga hai')
elif s.count(o2)==1:
    s=s.replace(o2,n2,1);ch+=1;print('micquiet: laga diya')
else:
    print('micquiet: jagah nahi mili',s.count(o2))
if ch:
    open(p,'w',encoding='utf-8').write(s)
