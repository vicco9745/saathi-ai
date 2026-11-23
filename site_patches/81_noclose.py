p='index.html'
s=open(p,encoding='utf-8').read()
old=r"""<span class="crd"></span><button type="button" data-r="close" aria-label="Close">'+ic('<path d="M18 6 6 18M6 6l12 12"/>')+'</button>';"""
new="""';/*noclose81*/"""
if 'noclose81' in s:
    print('noclose: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('noclose: laga diya')
else:
    print('noclose: jagah nahi mili',s.count(old))
