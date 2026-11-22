p='index.html'
s=open(p,encoding='utf-8').read()
old="callDictateIcon.innerHTML=callMuted?MIC_OFF_SVG:MIC_ON_SVG;"
new="callDictateIcon.innerHTML=callMuted?MIC_ON_SVG:MIC_OFF_SVG;/*micswap66*/"
if 'micswap66' in s:
    print('micswap: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('micswap: laga diya')
else:
    print('micswap: jagah nahi mili',s.count(old))
