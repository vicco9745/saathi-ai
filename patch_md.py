js=open('md_render.js',encoding='utf-8').read()
css='<style id="md-style">.md-h{font-weight:700;margin:12px 0 4px;line-height:1.35}.md-h1{font-size:1.3em}.md-h2{font-size:1.18em}.md-h3{font-size:1.08em}.md-h4,.md-h5,.md-h6{font-size:1em}.md-p{margin:0}.md-sp{height:8px}.md-l{margin:4px 0;padding-left:22px}.md-l li{margin:2px 0}.md-q{border-left:3px solid rgba(128,128,128,.5);padding:2px 0 2px 10px;margin:4px 0;opacity:.85}.md-hr{border:0;border-top:1px solid rgba(128,128,128,.3);margin:10px 0}.md-tw{overflow-x:auto;margin:8px 0}.md-t{border-collapse:collapse;font-size:.95em;min-width:100%}.md-t th,.md-t td{border:1px solid rgba(128,128,128,.3);padding:6px 10px;text-align:left;vertical-align:top}.md-t th{background:rgba(128,128,128,.12);font-weight:700}.md-ic{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.9em;background:rgba(128,128,128,.16);padding:1px 5px;border-radius:4px}</style>'
p='index.html'
s=open(p,encoding='utf-8').read()
if 'function mdRender(' in s:
    print('md: index.html mein pehle se hai')
else:
    a='function renderRichText(text){'
    b="if(before)out+=linkifyText(before.replace(/\\n$/,''));"
    c='if(rest)out+=linkifyText(rest);return out;}'
    d='element.textContent+=text[i++];'
    cnt=(s.count(a),s.count(b),s.count(c),s.count(d),s.count('</head>')>0)
    if cnt[:4]==(1,1,1,1) and cnt[4]:
        s=s.replace(a,js+'\n'+a,1)
        s=s.replace(b,b.replace('linkifyText','mdRender'),1)
        s=s.replace(c,c.replace('linkifyText','mdRender'),1)
        s=s.replace(d,"i++;if(i%3===0||i>=text.length||/\\s/.test(text[i-1])){element.innerHTML=renderRichText(text.slice(0,i));}",1)
        s=s.replace('</head>',css+'</head>',1)
        open(p,'w',encoding='utf-8').write(s)
        print('md: index.html laga diya')
    else:
        print('md: index.html mein jagah nahi mili',cnt)
p='format.js'
f=open(p,encoding='utf-8').read()
old="if(/^(SCRIPT|STYLE|TEXTAREA|INPUT|CODE|PRE|BUTTON|SVG|PATH)$/i.test(el.tagName))return;"
new=old+"if(el.closest&&el.closest('pre,code'))return;"
if "el.closest&&el.closest('pre,code')" in f:
    print('md: format.js mein pehle se hai')
elif f.count(old)==1:
    open(p,'w',encoding='utf-8').write(f.replace(old,new,1))
    print('md: format.js laga diya')
else:
    print('md: format.js mein jagah nahi mili',f.count(old))
