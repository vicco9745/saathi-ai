p = 'index.html'
s = open(p, encoding='utf-8').read()
old = "box-shadow:0 6px 24px rgba(0,0,0,.18)';\ndocument.body.appendChild(box);"
new = "box-shadow:0 6px 24px rgba(0,0,0,.18)';"
if 'function __siteFix' not in s:
    print('sitehide: pehle patch_sitefix.py lagana hoga')
elif s.count(old) != 1:
    print('sitehide: pehle se hidden hai ya jagah nahi mili', s.count(old))
else:
    s = s.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('sitehide: laga diya')
