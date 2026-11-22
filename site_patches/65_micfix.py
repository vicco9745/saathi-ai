import re
p='index.html'
s=open(p,encoding='utf-8').read()
pat=re.compile(r'<style id="micred64">.*?</style>',re.S)
new='<style id="micred64">.call-composer-wrap #callDictateBtn.muted{background:#e5393a;color:#fff;box-shadow:0 4px 14px rgba(229,57,58,.35)}</style>'
if len(pat.findall(s))==1:
    if new in s:
        print('micfix: pehle se laga hai')
    else:
        open(p,'w',encoding='utf-8').write(pat.sub(lambda m:new,s,count=1))
        print('micfix: laga diya')
else:
    print('micfix: jagah nahi mili',len(pat.findall(s)))
