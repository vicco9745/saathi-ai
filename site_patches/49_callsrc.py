p='index.html'
s=open(p,encoding='utf-8').read()

BLOCK=r"""/*callsrc*/function __cvWantSearch(q){return /search|सर्च|khoj|खोज|dhundh|dhoondh|ढूंढ|ढूँढ|news|न्यूज़|न्यूज|samachar|समाचार|kahani|कहानी/i.test(q||'');}
function __cvFav(u){try{return 'https://icons.duckduckgo.com/ip3/'+new URL(u).hostname+'.ico';}catch(_){return '';}}
function __cvDom(u){try{return new URL(u).hostname.replace(/^www\./,'');}catch(_){return u;}}
function __cvHideSrc(){var c=document.getElementById('callSrcCard');if(c){c.classList.remove('on');c.innerHTML='';}}
function __cvShowSrc(src){
  try{
    var ov=document.getElementById('callOverlay');if(!ov)return;
    var list=(src||[]).filter(function(s){return s&&s.url;}).slice(0,10);
    if(!list.length){__cvHideSrc();return;}
    var c=document.getElementById('callSrcCard');
    if(!c){c=document.createElement('div');c.id='callSrcCard';ov.appendChild(c);}
    var box=document.createElement('div');box.className='cvs-box';
    var head=document.createElement('div');head.className='cvs-head';
    var ic=document.createElement('span');ic.className='cvs-ic';
    list.slice(0,3).forEach(function(s){var im=document.createElement('img');im.src=__cvFav(s.url);im.alt='';im.onerror=function(){im.style.visibility='hidden';};ic.appendChild(im);});
    var n=document.createElement('span');n.textContent=list.length+(list.length===1?' साइट':' साइटें');
    head.appendChild(ic);head.appendChild(n);
    var row=document.createElement('div');row.className='cvs-row';
    list.forEach(function(s){
      var a=document.createElement('a');a.className='cvs-item';a.href=s.url;a.target='_blank';a.rel='noopener noreferrer';
      var t=document.createElement('div');t.className='cvs-t';
      var ti=document.createElement('div');ti.className='cvs-title';ti.textContent=s.title||s.url;
      var d=document.createElement('div');d.className='cvs-dom';
      var di=document.createElement('img');di.src=__cvFav(s.url);di.alt='';di.onerror=function(){di.style.display='none';};
      var dt=document.createElement('span');dt.textContent=__cvDom(s.url);
      d.appendChild(di);d.appendChild(dt);t.appendChild(ti);t.appendChild(d);a.appendChild(t);
      var th=s.image||s.thumbnail;
      if(th&&/^https?:/i.test(th)){var tm=document.createElement('img');tm.className='cvs-th';tm.src=th;tm.alt='';tm.onerror=function(){tm.style.display='none';};a.appendChild(tm);}
      row.appendChild(a);
    });
    box.appendChild(head);box.appendChild(row);c.innerHTML='';c.appendChild(box);
    var w=document.getElementById('callWavesWrap'),top=300;
    if(w){var r=w.getBoundingClientRect(),o=ov.getBoundingClientRect();top=Math.round(r.bottom-o.top+54);}
    c.style.top=top+'px';c.classList.add('on');
  }catch(_){}
}
"""

CSS='''<style id="callsrc-style">
#callSrcCard{position:absolute;left:14px;right:14px;z-index:6;display:none}
#callSrcCard.on{display:block;animation:cvsIn .28s ease}
#callOverlay.chat-open #callSrcCard{display:none!important}
.cvs-box{background:rgba(241,242,247,.95);border-radius:28px;padding:14px 12px 12px;box-shadow:0 6px 24px rgba(40,50,120,.12)}
.cvs-head{display:flex;align-items:center;gap:10px;padding:0 6px 10px;color:#1a1c2e;font-size:16px;font-weight:600}
.cvs-ic{display:inline-flex}
.cvs-ic img{width:28px;height:28px;border-radius:50%;border:2px solid #f1f2f7;background:#fff;margin-left:-8px}
.cvs-ic img:first-child{margin-left:0}
.cvs-row{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
.cvs-row::-webkit-scrollbar{display:none}
.cvs-item{flex:0 0 88%;scroll-snap-align:start;display:flex;align-items:center;gap:10px;background:#fff;border-radius:20px;padding:12px 14px;text-decoration:none;color:#1a1c2e;min-width:0;box-sizing:border-box}
.cvs-t{flex:1;min-width:0}
.cvs-title{font-size:15px;font-weight:500;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cvs-dom{display:flex;align-items:center;gap:6px;margin-top:8px;font-size:13px;color:#555a70}
.cvs-dom img{width:18px;height:18px;border-radius:5px}
.cvs-th{width:78px;height:60px;object-fit:cover;border-radius:10px;flex-shrink:0}
@keyframes cvsIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
</style>
'''

EDITS=[
 ("function startCall(){callActive=true;callMuted=false;",
  BLOCK+"function startCall(){callActive=true;callMuted=false;"),
 ("\n  fetch(SAATHI_API_BASE+'/v1/chat',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({message:q,model:currentModel,memory:(addMemoryOn?memoryNotes:[]),learning:getSmartLearningContext(),allow_web_search:addWebSearchOn,",
  "\n  fetch(SAATHI_API_BASE+'/v1/chat',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({message:q,model:currentModel,memory:(addMemoryOn?memoryNotes:[]),learning:getSmartLearningContext(),allow_web_search:(addWebSearchOn||__cvWantSearch(q)),"),
 ("var fresh={role:'ai',text:'',typing:true};",
  "__cvHideSrc();var fresh={role:'ai',text:'',typing:true};"),
 ("fresh.text=data.reply||'Saathi se jawab nahi mila.';",
  "fresh.text=data.reply||'Saathi se jawab nahi mila.';if(Array.isArray(data.sources)&&data.sources.length>0)fresh.sources=data.sources.slice(0,10);"),
 ("if(callActive)__cvSpeak(fresh.text);else callBusy=false;",
  "if(callActive){__cvShowSrc(fresh.sources);__cvSpeak(fresh.text);}else callBusy=false;"),
 ("function stopCall(){callActive=false;callMuted=false;__cvMicClose();__cvStop();",
  "function stopCall(){callActive=false;callMuted=false;__cvHideSrc();__cvMicClose();__cvStop();"),
]

if '/*callsrc*/' in s: print('pehle se laga hai')
else:
    bad=[a[:50] for a,_ in EDITS if s.count(a)!=1]
    i=s.rfind('</body>')
    if bad or i<0: print('jagah nahi mili',bad)
    else:
        for a,b in EDITS: s=s.replace(a,b,1)
        i=s.rfind('</body>')
        open(p,'w',encoding='utf-8').write(s[:i]+CSS+s[i:]); print('card laga diya')
