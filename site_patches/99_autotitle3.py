p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __autoTitle2(chat,raw){
try{
const t=String(raw||'').split('=== file')[0].replace(/\s+/g,' ').trim();
if(!t)return;
const cjk=/[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]/.test(t);
const MAX=cjk?16:25,MIN=cjk?5:14;
const local=__tCut(t,MAX);
chat.__titled=true;chat.__autoTitle=false;chat.title=local;
try{saveChats();renderChatList();}catch(_){}
function apply(x){chat.title=x;chat.__tDone=true;try{saveChats();renderChatList();}catch(_){}}
fetch(SAATHI_API_BASE+'/v1/title2',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({message:t.slice(0,300)})}).then(function(r){return r.ok?r.json():null;}).then(function(d){const x=d&&d.title?String(d.title).replace(/["“”]/g,'').trim():'';apply(x&&__tSeg(x).length>=MIN?__tCut(x,MAX+3):local);}).catch(function(){apply(local);});
}catch(_){}}
function __bTitleSweep(){
try{
const chat=getCurrentChat();
if(!chat||chat.__tDone||chat.title!=='New chat')return;
const um=(chat.messages||[]).find(function(x){return x&&x.role==='user'&&typeof x.text==='string'&&x.text.trim();});
if(!um)return;
__autoTitle2(chat,um.text);
}catch(_){}}
setInterval(__bTitleSweep,1000);
"""
a1 = 'function renderMessages(){'
if 'function __bTitleSweep' in s:
    print('autotitle3: pehle se laga hai')
elif s.count(a1) != 1 or 'function __tCut' not in s:
    print('autotitle3: jagah nahi mili', s.count(a1), 'function __tCut' in s)
else:
    s = s.replace(a1, FN + a1, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('autotitle3: laga diya')
