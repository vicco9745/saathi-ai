p='index.html'
s=open(p,encoding='utf-8').read()
a_old="||typeof SAATHI_KEY==='undefined'||typeof detectSpeechLang!=='function')return false;"
a_new="||!localStorage.getItem('saathi_api_key')||typeof detectSpeechLang!=='function')return false;"
b_old="fetch(SAATHI_API_BASE+'/v1/tts',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY}"
b_new="fetch(SAATHI_API_BASE+'/v1/tts',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':localStorage.getItem('saathi_api_key')}"
if a_new in s and b_new in s:
    print('ttskey: pehle se laga hai')
elif s.count(a_old)==1 and s.count(b_old)==1:
    s=s.replace(a_old,a_new,1).replace(b_old,b_new,1)
    open(p,'w',encoding='utf-8').write(s)
    print('ttskey: laga diya')
else:
    print('ttskey: jagah nahi mili', s.count(a_old), s.count(b_old))
