import re
p='index.html'
s=open(p,encoding='utf-8').read()
new='<svg class="sorticon56" viewBox="0 -960 960 960" fill="currentColor"><path d="M120-240v-80h240v80H120Zm0-200v-80h480v80H120Zm0-200v-80h720v80H120Z"/></svg>'
for bid in ('hamburgerBtn','callMenuBtn','allChatsBack'):
    pat=re.compile(r'(<button[^>]*id="'+bid+r'"[^>]*>)<svg(?![^>]*sorticon56).*?</svg>',re.S)
    n=len(pat.findall(s))
    if n==1:
        s=pat.sub(lambda m:m.group(1)+new,s,count=1)
        print('sorticon:',bid,'laga diya')
    else:
        print('sorticon:',bid,'skip',n)
open(p,'w',encoding='utf-8').write(s)
