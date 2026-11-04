p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __describeSite(m,prompt,html){try{fetch(SAATHI_API_BASE+'/v1/describe',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':localStorage.getItem('saathi_api_key')},body:JSON.stringify({prompt:String(prompt||'')+'\n\n=====HTML=====\n'+String(html||'').slice(0,6000)})}).then(function(r){return r.ok?r.json():null;}).then(function(d){var t=d&&d.reply?String(d.reply).trim():'';if(t.length>=40){m.text=t;try{saveChats();}catch(_){}try{renderMessages();}catch(_){}}}).catch(function(){});}catch(_){}}
"""
a1 = 'function linkifyText(text){'
oldT = "pendingReply.text=buildGenReply('website',{caption:data.caption,html:html,prompt:sitePrompt});"
newT = oldT + "__describeSite(pendingReply,sitePrompt,html);/*site-desc*/"
if 'site-desc' in s:
    print('sitedesc: pehle se laga hai')
elif s.count(a1) == 1 and s.count(oldT) == 1:
    s = s.replace(a1, FN + a1, 1).replace(oldT, newT, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('sitedesc: laga diya')
else:
    print('sitedesc: jagah nahi mili', s.count(a1), s.count(oldT))
