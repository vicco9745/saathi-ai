p='index.html'
s=open(p,encoding='utf-8').read()

MARK='/*callvoice*/'

BLOCK=r"""/*callvoice*/var callBusy=false,__cvPend='',__cvT=null,__cvAudio=null,__cvTok=0;
function __cvClean(t){return String(t||'').replace(/```[\s\S]*?```/g,' ').replace(/`([^`]*)`/g,'$1').replace(/!?\[([^\]]*)\]\([^)]*\)/g,'$1').replace(/https?:\/\/\S+/g,' ').replace(/[*#_>~|]+/g,' ').replace(/\s+/g,' ').trim();}
function __cvSplit(t){var out=[],s=t;while(s.length>0&&out.length<4){if(s.length<=260){out.push(s);break;}var cut=-1,m,re=/[\u0964.!?]\s/g,head=s.slice(0,260);while((m=re.exec(head))!==null)cut=m.index+1;if(cut<80)cut=s.lastIndexOf(' ',260);if(cut<1)cut=260;out.push(s.slice(0,cut).trim());s=s.slice(cut).trim();}return out;}
function __cvStop(){__cvTok++;try{if(__cvAudio)__cvAudio.pause();}catch(_){}__cvAudio=null;window.__saathiAudio=null;window.__saathiSpeaking=false;}
function __cvDone(tok){if(tok!==__cvTok)return;window.__saathiSpeaking=false;__cvAudio=null;window.__saathiAudio=null;callBusy=false;if(callActive&&!callMuted)setTimeout(listenOnce,300);}
function __cvSpeak(text){
  var tok=++__cvTok,clean=__cvClean(text);
  if(!clean){__cvDone(tok);return;}
  var lang=detectSpeechLang(clean),px=String(lang).split('-')[0].toLowerCase(),KEY=localStorage.getItem('saathi_api_key');
  var fallback=function(){if(tok!==__cvTok)return;try{speakText(clean,function(){__cvDone(tok);});}catch(_){__cvDone(tok);}};
  if((px!=='hi'&&px!=='en')||!KEY){fallback();return;}
  var parts=__cvSplit(clean),jobs=[];
  var load=function(i){if(i<parts.length&&!jobs[i])jobs[i]=fetch(SAATHI_API_BASE+'/v1/tts',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({text:parts[i],lang:lang})}).then(function(r){if(!r.ok)throw new Error('tts');return r.blob();});return jobs[i];};
  window.__saathiSpeaking=true;
  var play=function(i){
    if(tok!==__cvTok)return;
    if(i>=parts.length){__cvDone(tok);return;}
    load(i).then(function(b){
      if(tok!==__cvTok)return;
      load(i+1);
      var a=new Audio(URL.createObjectURL(b));__cvAudio=a;window.__saathiAudio=a;
      try{a.volume=window.__saathiSpkOff?0:1;}catch(_){}
      a.onended=function(){play(i+1);};
      a.onerror=function(){if(i===0)fallback();else __cvDone(tok);};
      var pr=a.play();if(pr&&pr.catch)pr.catch(function(){if(i===0)fallback();else __cvDone(tok);});
    }).catch(function(){if(i===0)fallback();else __cvDone(tok);});
  };
  play(0);
}
function __cvAsk(t){__cvPend=(__cvPend+' '+t).trim();clearTimeout(__cvT);__cvT=setTimeout(__cvSend,1300);}
function __cvSend(){
  var q=__cvPend;__cvPend='';
  if(!q||!callActive)return;
  var KEY=localStorage.getItem('saathi_api_key');
  if(!KEY){showToast('API key nahi mili');return;}
  var chat=getCurrentChat();if(!chat)return;
  callBusy=true;try{if(recognition)recognition.abort();}catch(_){}
  var fresh={role:'ai',text:'',typing:true};chat.messages.push(fresh);saveChats();renderMessages();
  if(callOverlay.classList.contains('chat-open'))renderCallChatMessages();
  fetch(SAATHI_API_BASE+'/v1/chat',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({message:q,model:currentModel,memory:(addMemoryOn?memoryNotes:[]),learning:getSmartLearningContext(),allow_web_search:addWebSearchOn,think:addThinkOn})})
  .then(async function(res){var data=await res.json();if(!res.ok)throw new Error(data.detail||data.error||'API error');return data;})
  .then(function(data){
    fresh.typing=false;fresh.text=data.reply||'Saathi se jawab nahi mila.';
    saveChats();renderMessages();if(callOverlay.classList.contains('chat-open'))renderCallChatMessages();
    if(callActive)__cvSpeak(fresh.text);else callBusy=false;
  })
  .catch(function(err){
    fresh.typing=false;fresh.text='Saathi connection error: '+err.message;
    saveChats();renderMessages();if(callOverlay.classList.contains('chat-open'))renderCallChatMessages();
    callBusy=false;if(callActive&&!callMuted)setTimeout(listenOnce,300);
  });
}
"""

EDITS=[
 ("function startCall(){callActive=true;callMuted=true;",
  BLOCK+"function startCall(){callActive=true;callMuted=false;"),
 ("function listenOnce(){if(!callActive||callMuted)return;",
  "function listenOnce(){if(!callActive||callMuted||callBusy)return;"),
 ("if(!SR){return;}try{recognition=new SR();",
  "if(!SR){showToast('Is browser mein mic se baat support nahi hai. Chrome mein kholiye.');return;}try{recognition=new SR();"),
 ("if(liveFinal.trim()){addLiveUserText(liveFinal.trim());}",
  "if(liveFinal.trim()){addLiveUserText(liveFinal.trim());__cvAsk(liveFinal.trim());}"),
 ("recognition.onerror=()=>{};",
  "recognition.onerror=(ev)=>{if(ev&&(ev.error==='not-allowed'||ev.error==='service-not-allowed'))showToast('Mic ki permission nahi mili');};"),
 ("recognition.onend=()=>{if(callActive&&!callMuted){",
  "recognition.onend=()=>{if(callActive&&!callMuted&&!callBusy){"),
 ("function stopCall(){callActive=false;callMuted=false;",
  "function stopCall(){callActive=false;callMuted=false;__cvStop();clearTimeout(__cvT);__cvPend='';callBusy=false;"),
 ("try{speaking=!!(window.speechSynthesis&&window.speechSynthesis.speaking);}catch(_){}",
  "try{speaking=!!(window.__saathiSpeaking||(window.speechSynthesis&&window.speechSynthesis.speaking));}catch(_){}"),
 ("$('cv2Spk').addEventListener('click',function(){spkOff=!spkOff;tick();",
  "$('cv2Spk').addEventListener('click',function(){spkOff=!spkOff;window.__saathiSpkOff=spkOff;try{if(window.__saathiAudio)window.__saathiAudio.volume=spkOff?0:1;}catch(_){}tick();"),
]

if MARK in s:
    print('callvoice: pehle se laga hai')
else:
    bad=[a for a,_ in EDITS if s.count(a)!=1]
    if bad:
        print('callvoice: jagah nahi mili ->', [b[:50] for b in bad])
    else:
        for a,b in EDITS:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('callvoice: laga diya')
