import re
p='index.html'
s=open(p,encoding='utf-8').read()
a=re.compile(r'(#cvCap\{position:absolute;left:24px;right:24px;bottom:)\d+px')
b=re.compile(r'(#cvFb\{position:absolute;left:0;right:0;bottom:)\d+px;(?:/\*fbdown61\*/)?')
css='<style id="cvsmall62">#callSrcCard .cvs-box{padding:10px;border-radius:22px}#callSrcCard .cvs-head{padding:0 4px 6px;font-size:14px;gap:8px}#callSrcCard .cvs-ic img{width:20px;height:20px;margin-left:-6px}#callSrcCard .cvs-ic img:first-child{margin-left:0}#callSrcCard .cvs-item{padding:7px 12px;border-radius:16px}#callSrcCard .cvs-title{font-size:13px;line-height:1.25}#callSrcCard .cvs-dom{margin-top:3px;font-size:11px}#callSrcCard .cvs-dom img{width:14px;height:14px}#callSrcCard .cvs-th{width:72px;height:52px;border-radius:10px}</style>'
if 'cvsmall62' in s:
    print('srcsmall: pehle se laga hai')
elif len(a.findall(s))==1 and len(b.findall(s))==1 and s.count('</head>')==1:
    s=a.sub(lambda m:m.group(1)+'190px',s,count=1)
    s=b.sub(lambda m:m.group(1)+'130px;/*fbdown61*/',s,count=1)
    s=s.replace('</head>',css+'</head>',1)
    open(p,'w',encoding='utf-8').write(s)
    print('srcsmall: laga diya')
else:
    print('srcsmall: jagah nahi mili',len(a.findall(s)),len(b.findall(s)),s.count('</head>'))
