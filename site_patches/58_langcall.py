p='index.html'
s=open(p,encoding='utf-8').read()
old="allow_web_search:(addWebSearchOn||__cvWantSearch(q)),"
new=old+"/*langcall58*/lang_pref:(function(){try{var l=String(detectSpeechLang(q)||'').split('-')[0].toLowerCase();return l||null;}catch(_){return null;}})(),"
if 'langcall58' in s:
    print('langcall: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('langcall: laga diya')
else:
    print('langcall: jagah nahi mili',s.count(old))
