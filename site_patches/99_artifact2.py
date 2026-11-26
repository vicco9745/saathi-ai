p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __afDoc(h){h=String(h||'');const cs=getComputedStyle(document.documentElement);const g=function(ns,f){for(let i=0;i<ns.length;i++){const v=cs.getPropertyValue(ns[i]).trim();if(v)return v;}return f;};
const css='<style>:root{--s-bg:'+g(['--panel-bg','--page-bg'],'#ffffff')+';--s-panel:'+g(['--panel-bg'],'#ffffff')+';--s-text:'+g(['--text'],'#1d1d24')+';--s-soft:'+g(['--text-soft'],'#6b6b7a')+';--s-accent:'+g(['--accent','--primary','--brand','--purple','--theme'],'#5b4fd1')+';--s-accent-soft:'+g(['--accent-soft','--primary-soft'],'#dcd8fb')+';--s-border:'+g(['--border'],'#e3e1f0')+'}body{background:var(--s-bg);color:var(--s-text)}</style>';
return /<head[^>]*>/i.test(h)?h.replace(/<head[^>]*>/i,function(x){return x+css;}):css+h;}
"""
a1 = 'function __buildArtifactCard(m){'
old = ".srcdoc=String(a.html||'')"
if 'function __afDoc' in s:
    print('artifact2: pehle se laga hai')
elif s.count(a1) != 1 or s.count(old) != 2:
    print('artifact2: jagah nahi mili', s.count(a1), s.count(old))
else:
    s = s.replace(old, ".srcdoc=__afDoc(a.html)")
    s = s.replace(a1, FN + a1, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('artifact2: laga diya')
