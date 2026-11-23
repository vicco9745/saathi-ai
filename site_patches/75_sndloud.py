p='index.html'
s=open(p,encoding='utf-8').read()
old="g.gain.exponentialRampToValueAtTime(0.45,t0+n[1]+0.02);"
new="g.gain.exponentialRampToValueAtTime(0.9,t0+n[1]+0.02);/*sndloud75*/"
if 'sndloud75' in s:
    print('sndloud: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('sndloud: laga diya')
else:
    print('sndloud: jagah nahi mili',s.count(old))
