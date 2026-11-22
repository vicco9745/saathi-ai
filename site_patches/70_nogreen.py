p='index.html'
s=open(p,encoding='utf-8').read()
css='<style id="nogreen70">.composer:focus-within{border-color:var(--border)!important;box-shadow:0 4px 20px var(--shadow-color)!important}</style>'
if 'nogreen70' in s:
    print('nogreen: pehle se laga hai')
elif s.count('</head>')==1:
    open(p,'w',encoding='utf-8').write(s.replace('</head>',css+'</head>',1))
    print('nogreen: laga diya')
else:
    print('nogreen: jagah nahi mili',s.count('</head>'))
