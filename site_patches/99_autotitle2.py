p = 'index.html'
s = open(p, encoding='utf-8').read()
NEW = r"""function __tSeg(t){try{return Array.from(new Intl.Segmenter(undefined,{granularity:'grapheme'}).segment(String(t)),function(x){return x.segment;});}catch(_){return Array.from(String(t));}}
function __tCut(t,max){const a=__tSeg(String(t).replace(/\s+/g,' ').trim());if(a.length<=max)return a.join('');let s=a.slice(0,max).join('');const i=s.lastIndexOf(' ');if(i>max*0.5)s=s.slice(0,i);return s.replace(/[\s,.;:!?।、，。\-]+$/,'')+'…';}
function __autoTitle(raw){
try{
const chat=getCurrentChat();
if(!chat||chat.__tDone||chat.title!=='New chat')return;
if(chat.messages&&chat.messages.length>2)return;
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
"""
a = s.find('function __autoTitle(raw){')
b = s.find('function renderMessages(){')
if 'function __tCut' in s:
    print('autotitle2: pehle se laga hai')
elif a < 0 or b < a or 'chat.__tDone' not in s[a:b] or b - a > 4000:
    print('autotitle2: jagah nahi mili', a, b)
else:
    s = s[:a] + NEW + s[b:]
    open(p, 'w', encoding='utf-8').write(s)
    print('autotitle2: laga diya')
