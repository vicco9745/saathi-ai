p = 'index.html'
s = open(p, encoding='utf-8').read()
old = "if(mediaAttachments.length>0&&analyzableFiles.length===0){"
new = "if(mediaAttachments.length>0&&analyzableFiles.length===0&&!mediaAttachments.some(a=>a.kind==='photo')){"
if new in s:
    print('pehle se laga hua hai')
elif s.count(old) != 1:
    print('jagah nahi mili ya ek se zyada hai:', s.count(old))
else:
    open(p, 'w', encoding='utf-8').write(s.replace(old, new))
    print('done')
