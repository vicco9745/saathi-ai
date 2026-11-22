p='index.html'
s=open(p,encoding='utf-8').read()
old="function fixMic(){if(di&&di.innerHTML.indexOf('x1=\"2\"')>-1)di.innerHTML=MICON;}"
new="function fixMic(){/*fixmic69*/}"
if 'fixmic69' in s:
    print('fixmic: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('fixmic: laga diya')
else:
    print('fixmic: jagah nahi mili',s.count(old))
