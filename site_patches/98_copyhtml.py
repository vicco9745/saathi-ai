p = 'format.js'
f = open(p, encoding='utf-8').read()
old = "return code.test(s)?s:clean0(s);"
new = r"return (code.test(s)||/<\/?[a-z!][^>]*>|\/\*|\{[^{}]*;[^{}]*\}|^\s*(?:function\b|const |let |var )/m.test(s))?s:clean0(s);/*html-safe*/"
if 'html-safe' in f:
    print('copyhtml: pehle se laga hai')
elif f.count(old) == 1:
    open(p, 'w', encoding='utf-8').write(f.replace(old, new, 1))
    print('copyhtml: laga diya')
else:
    print('copyhtml: jagah nahi mili', f.count(old))
