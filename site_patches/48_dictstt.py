HP='index.html'
ht=open(HP,encoding='utf-8').read()

BLOCK=r"""/*dictstt*/var __dtStream=null,__dtCtx=null,__dtAn=null,__dtBuf=null,__dtTimer=null,__dtRec=null,__dtChunks=[];
function __dtMime(){var L=['audio/webm;codecs=opus','audio/webm','audio/mp4','audio/ogg;codecs=opus'];for(var i=0;i<L.length;i++){try{if(MediaRecorder.isTypeSupported(L[i]))return L[i];}catch(_){}}return '';}
function __dtOk(){return window.__dtMic!==false&&!!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia&&window.MediaRecorder&&(window.AudioContext||window.webkitAudioContext));}
function __dtRelease(){
  clearInterval(__dtTimer);__dtTimer=null;
  try{if(__dtStream)__dtStream.getTracks().forEach(function(t){t.stop();});}catch(_){}
  __dtStream=null;try{if(__dtCtx)__dtCtx.close();}catch(_){}__dtCtx=null;__dtAn=null;
}
function __dtCancel(){
  var r=__dtRec;__dtRec=null;
  if(r){r.ondataavailable=null;r.onstop=null;try{if(r.state!=='inactive')r.stop();}catch(_){}}
  __dtChunks=[];__dtRelease();
}
function __dtStart(){
  window.__speaking=false;window.__speechAct=0;
  isDictating=true;updateDictateButton();updateActionButton();
  navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}}).then(function(st){
    if(!isDictating){st.getTracks().forEach(function(t){t.stop();});return;}
    __dtStream=st;
    var AC=window.AudioContext||window.webkitAudioContext;__dtCtx=new AC();
    __dtAn=__dtCtx.createAnalyser();__dtAn.fftSize=512;__dtCtx.createMediaStreamSource(st).connect(__dtAn);
    __dtBuf=new Uint8Array(__dtAn.fftSize);
    __dtTimer=setInterval(function(){
      if(!__dtAn)return;
      __dtAn.getByteTimeDomainData(__dtBuf);
      var sum=0;for(var i=0;i<__dtBuf.length;i++){var v=(__dtBuf[i]-128)/128;sum+=v*v;}
      if(Math.sqrt(sum/__dtBuf.length)>0.02)window.__speechAct=Date.now();
    },70);
    var mt=__dtMime();__dtChunks=[];
    __dtRec=mt?new MediaRecorder(st,{mimeType:mt}):new MediaRecorder(st);
    __dtRec.ondataavailable=function(e){if(e.data&&e.data.size)__dtChunks.push(e.data);};
    __dtRec.start(250);
  }).catch(function(){
    window.__dtMic=false;isDictating=false;updateDictateButton();updateActionButton();
    showToast('Mic ki ijazat nahi mili. Browser mein Allow karein');
  });
}
function __dtFinish(sendAfter){
  var r=__dtRec;__dtRec=null;
  var mime=(r&&r.mimeType)||'audio/webm';
  var done=function(){
    isDictating=false;updateDictateButton();updateActionButton();
    var blob=new Blob(__dtChunks,{type:mime});__dtChunks=[];__dtRelease();
    if(blob.size<1500)return;
    showToast('Likh raha hoon...');
    __dtSend(blob,mime,sendAfter);
  };
  if(!r){done();return;}
  r.onstop=done;
  try{r.stop();}catch(_){done();}
}
function __dtSend(blob,mime,sendAfter){
  var KEY=localStorage.getItem('saathi_api_key'),rd=new FileReader();
  rd.onload=function(){
    var b64=String(rd.result).split(',')[1]||'';
    fetch(SAATHI_API_BASE+'/v1/stt',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({audio:b64,mime:mime,lang:'hi'})})
    .then(function(r){if(!r.ok){var e=new Error('stt '+r.status);e.status=r.status;throw e;}return r.json();})
    .then(function(d){
      var text=String((d&&d.text)||'').trim();
      if(!text){showToast('Awaaz samajh nahi aayi, dobara boliye');return;}
      var base=msgInput.value?msgInput.value.trim()+' ':'';
      msgInput.value=base+text;window.__voiceIn=true;autoResizeInput();msgInput.focus();updateActionButton();
      if(sendAfter&&msgInput.value.trim().length>0)sendMessage();
    }).catch(function(e){
      if(e&&(e.status===404||e.status===405||e.status===503))window.__dtMic=false;
      showToast('Awaaz likhne mein dikkat aayi, dobara koshish karein');
    });
  };
  rd.readAsDataURL(blob);
}
"""

EDITS=[
 ("function startDictation(){const SR=",
  BLOCK+"function startDictation(){if(__dtOk()){__dtStart();return;}const SR="),
 ("function finalizeDictationThen(sendAfter){if(!isDictating)return;",
  "function finalizeDictationThen(sendAfter){if(__dtRec||__dtStream){__dtFinish(sendAfter);return;}if(!isDictating)return;"),
 ("function cancelDictation(){stopDictateEngine();",
  "function cancelDictation(){__dtCancel();stopDictateEngine();"),
 ("function finalizeDictation(){stopDictateEngine();",
  "function finalizeDictation(){if(__dtRec||__dtStream){__dtFinish(false);return;}stopDictateEngine();"),
 ("function stopDictateEngine(){dictateManualStop=true;",
  "function stopDictateEngine(){__dtCancel();dictateManualStop=true;"),
]

if '/*callstt*/' not in ht:
    print('dictstt: pehle 47_callstt laga hona chahiye')
elif '/*dictstt*/' in ht:
    print('dictstt: pehle se laga hai')
else:
    bad=[a[:45] for a,_ in EDITS if ht.count(a)!=1]
    if bad:
        print('dictstt: jagah nahi mili ->',bad)
    else:
        for a,b in EDITS:
            ht=ht.replace(a,b,1)
        open(HP,'w',encoding='utf-8').write(ht)
        print('dictstt: laga diya')
