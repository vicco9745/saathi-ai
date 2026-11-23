p='index.html'
s=open(p,encoding='utf-8').read()
css='<style id="wavebub71">.msg-row.user .bubble.live-voice::before{width:16px!important;height:16px!important;top:15px!important;background:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%23555\' stroke-width=\'2.2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Cpath d=\'M4 9v6M8 5v14M12 2v20M16 6v12M20 9v6\'/%3E%3C/svg%3E") center/contain no-repeat!important}</style>'
if 'wavebub71' in s:
    print('wavebub: pehle se laga hai')
elif s.count('</head>')==1:
    open(p,'w',encoding='utf-8').write(s.replace('</head>',css+'</head>',1))
    print('wavebub: laga diya')
else:
    print('wavebub: jagah nahi mili',s.count('</head>'))
