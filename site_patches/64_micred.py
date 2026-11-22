p='index.html'
s=open(p,encoding='utf-8').read()
css='<style id="micred64">.call-composer-wrap #callDictateBtn.muted{background:#fff;color:#1a1c2e}.call-composer-wrap #callDictateBtn:not(.muted):not(.has-text){background:#e5393a;color:#fff;box-shadow:0 4px 14px rgba(229,57,58,.35)}</style>'
if 'micred64' in s:
    print('micred: pehle se laga hai')
elif s.count('</head>')==1:
    open(p,'w',encoding='utf-8').write(s.replace('</head>',css+'</head>',1))
    print('micred: laga diya')
else:
    print('micred: jagah nahi mili',s.count('</head>'))
