p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __autoTitle(raw){
try{
const chat=getCurrentChat();
if(!chat||chat.__tDone||chat.title!=='New chat')return;
if(chat.messages&&chat.messages.length>2)return;
const t=String(raw||'').split('=== file')[0].replace(/\s+/g,' ').trim();
if(!t)return;
const local=t.length>48?t.slice(0,48).replace(/\s+\S*$/,'')+'…':t;
chat.__titled=true;chat.__autoTitle=false;chat.title=local;
try{saveChats();renderChatList();}catch(_){}
function apply(x){chat.title=x;chat.__tDone=true;try{saveChats();renderChatList();}catch(_){}}
fetch(SAATHI_API_BASE+'/v1/title2',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({message:t.slice(0,300)})}).then(function(r){return r.ok?r.json():null;}).then(function(d){const x=d&&d.title?String(d.title).replace(/["“”]/g,'').trim():'';apply(x||local);}).catch(function(){apply(local);});
}catch(_){}}
"""
a1 = 'function renderMessages(){'
a2 = "if(__budgetHandle(pendingReply,combinedText)){return;}"
if 'function __autoTitle' in s:
    print('autotitle: pehle se laga hai')
elif s.count(a1) != 1 or s.count(a2) != 1:
    print('autotitle: jagah nahi mili', s.count(a1), s.count(a2))
else:
    s = s.replace(a2, "try{__autoTitle(combinedText);}catch(_){}" + a2, 1).replace(a1, FN + a1, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('autotitle: laga diya')
