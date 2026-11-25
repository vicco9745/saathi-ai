p = 'index.html'
s = open(p, encoding='utf-8').read()
a = r"""function __bDir(el,u){if(/^(ar|he|iw|fa|ur|ps|sd|yi|ckb)/i.test(u.lang)){el.dir='rtl';el.style.textAlign='right';}else{el.dir='ltr';el.style.textAlign='left';}}"""
b = r"""function __bDir(el,u){el.dir='ltr';el.style.textAlign='left';}"""
if s.count(a) == 1:
    s = s.replace(a, b, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('budget8: laga diya')
elif b in s:
    print('budget8: pehle se laga hai')
else:
    print('budget8: jagah nahi mili', s.count(a))
