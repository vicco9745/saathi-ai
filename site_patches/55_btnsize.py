p='index.html'
s=open(p,encoding='utf-8').read()
css='<style id="btnsize55">@media (min-width:900px){.msg-action-btn{width:44px;height:44px}.msg-action-btn svg{width:24px;height:24px}.msg-actions{gap:4px}}</style>'
if 'id="btnsize55"' in s:
    print('btnsize: pehle se laga hai')
elif s.count('</head>')==1:
    open(p,'w',encoding='utf-8').write(s.replace('</head>',css+'</head>',1))
    print('btnsize: laga diya')
else:
    print('btnsize: jagah nahi mili', s.count('</head>'))
