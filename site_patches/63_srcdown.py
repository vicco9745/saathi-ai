import re
p='index.html'
s=open(p,encoding='utf-8').read()
pat=re.compile(r'top=Math\.round\(r\.bottom-o\.top\+\d+\);/\*capgap60\*/')
if len(pat.findall(s))==1:
    if 'top=Math.round(r.bottom-o.top+44);/*capgap60*/' in s:
        print('srcdown: pehle se laga hai')
    else:
        open(p,'w',encoding='utf-8').write(pat.sub('top=Math.round(r.bottom-o.top+44);/*capgap60*/',s,count=1))
        print('srcdown: laga diya')
else:
    print('srcdown: jagah nahi mili',len(pat.findall(s)))
