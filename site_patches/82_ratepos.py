p='index.html'
s=open(p,encoding='utf-8').read()
old="b.style.top='142px';/*ratelook80*/"
new="b.style.top='102px';/*ratepos82*/"
if 'ratepos82' in s:
    print('ratepos: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('ratepos: laga diya')
else:
    print('ratepos: jagah nahi mili',s.count(old))
