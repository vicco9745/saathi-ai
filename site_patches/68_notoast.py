p='index.html'
s=open(p,encoding='utf-8').read()
old="function showToast(msg){const t=document.createElement('div');"
new="function showToast(msg){return;/*notoast68*/const t=document.createElement('div');"
if 'notoast68' in s:
    print('notoast: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('notoast: laga diya')
else:
    print('notoast: jagah nahi mili',s.count(old))
