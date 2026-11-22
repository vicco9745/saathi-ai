p='index.html'
s=open(p,encoding='utf-8').read()
a="#cvFb{position:absolute;left:0;right:0;bottom:130px;"
a2="#cvFb{position:absolute;left:0;right:0;bottom:92px;/*fbdown61*/"
if 'fbdown61' in s:
    print('fbdown: pehle se laga hai')
elif s.count(a)==1:
    open(p,'w',encoding='utf-8').write(s.replace(a,a2,1))
    print('fbdown: laga diya')
else:
    print('fbdown: jagah nahi mili',s.count(a))
