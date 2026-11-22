p='index.html'
s=open(p,encoding='utf-8').read()
a="top=Math.round(r.bottom-o.top+54);"
a2="top=Math.round(r.bottom-o.top+14);/*capgap60*/"
b="#cvCap{position:absolute;left:24px;right:24px;bottom:190px;"
b2="#cvCap{position:absolute;left:24px;right:24px;bottom:150px;"
if 'capgap60' in s:
    print('capgap: pehle se laga hai')
elif s.count(a)==1 and s.count(b)==1:
    s=s.replace(a,a2,1).replace(b,b2,1)
    open(p,'w',encoding='utf-8').write(s)
    print('capgap: laga diya')
else:
    print('capgap: jagah nahi mili',s.count(a),s.count(b))
