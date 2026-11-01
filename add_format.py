p = 'index.html'
s = open(p, encoding='utf-8').read()
tag = '<script src="format.js"></script>'
if 'format.js' in s:
    print('pehle se juda hua hai')
else:
    i = s.rfind('</body>')
    if i == -1:
        print('</body> nahi mila')
    else:
        open(p, 'w', encoding='utf-8').write(s[:i] + tag + '\n' + s[i:])
        print('done')
