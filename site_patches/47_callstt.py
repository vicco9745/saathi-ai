import os
SP='app/main.py'
HP='index.html'
sv=open(SP,encoding='utf-8').read()
ht=open(HP,encoding='utf-8').read()

SERVER=r'''class STTRequest(BaseModel):
    audio: str
    mime: str = "audio/webm"
    lang: str = "hi"

@app.post("/v1/stt")
def stt(body: STTRequest, key=Depends(require_api_key)):
    import base64, requests
    gkey = os.environ.get("GROQ_API_KEY")
    if not gkey:
        raise HTTPException(503, "stt provider not configured")
    try:
        raw = base64.b64decode(body.audio)
    except Exception:
        raise HTTPException(400, "bad audio")
    if len(raw) < 800 or len(raw) > 24 * 1024 * 1024:
        return {"text": ""}
    record_usage(key, "voice")
    mime = (body.mime or "audio/webm").split(";")[0]
    ext = "mp4" if "mp4" in mime else ("ogg" if "ogg" in mime else "webm")
    data = {"response_format": "json", "temperature": "0"}
    lg = (body.lang or "").split("-")[0].lower()
    if lg in ("hi", "en"):
        data["language"] = lg
    for model in ("whisper-large-v3-turbo", "whisper-large-v3"):
        try:
            d = dict(data)
            d["model"] = model
            r = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": "Bearer " + gkey},
                files={"file": ("a." + ext, raw, mime)},
                data=d,
                timeout=40,
            )
            if r.status_code == 200:
                return {"text": (r.json().get("text") or "").strip()[:3000]}
            print("STT", model, r.status_code, r.text[:150])
        except Exception as e:
            print("STT error", model, repr(e)[:150])
    raise HTTPException(502, "stt fail")

'''

SITE=r"""/*callstt*/var __cvStream=null,__cvCtx=null,__cvAn=null,__cvBuf=null,__cvTimer=null,__cvRec=null,__cvChunks=[],__cvFloor=0.008,__cvSpeech=0,__cvSil=0,__cvVoiced=0,__cvRecT=0,__cvOpening=false;
function __cvMime(){var L=['audio/webm;codecs=opus','audio/webm','audio/mp4','audio/ogg;codecs=opus'];for(var i=0;i<L.length;i++){try{if(window.MediaRecorder&&MediaRecorder.isTypeSupported(L[i]))return L[i];}catch(_){}}return '';}
function __cvMicOpen(){
  if(__cvStream&&__cvTimer)return;
  if(__cvOpening)return;
  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia||!window.MediaRecorder||!(window.AudioContext||window.webkitAudioContext)){window.__cvMic=false;listenOnce();return;}
  __cvOpening=true;
  navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}}).then(function(st){
    __cvOpening=false;
    if(!callActive){st.getTracks().forEach(function(t){t.stop();});return;}
    __cvStream=st;
    var AC=window.AudioContext||window.webkitAudioContext;__cvCtx=new AC();
    var src=__cvCtx.createMediaStreamSource(st);__cvAn=__cvCtx.createAnalyser();__cvAn.fftSize=1024;src.connect(__cvAn);
    __cvBuf=new Uint8Array(__cvAn.fftSize);
    if(__cvCtx.state==='suspended'){try{__cvCtx.resume();}catch(_){}}
    __cvTimer=setInterval(__cvTick,60);
  }).catch(function(){
    __cvOpening=false;window.__cvMic=false;showToast('Mic ki permission nahi mili');if(callActive)listenOnce();
  });
}
function __cvMicClose(){
  clearInterval(__cvTimer);__cvTimer=null;__cvRecDrop();
  try{if(__cvStream)__cvStream.getTracks().forEach(function(t){t.stop();});}catch(_){}
  __cvStream=null;try{if(__cvCtx)__cvCtx.close();}catch(_){}__cvCtx=null;__cvAn=null;
}
function __cvRecStart(){
  try{
    var mt=__cvMime();__cvChunks=[];
    __cvRec=mt?new MediaRecorder(__cvStream,{mimeType:mt}):new MediaRecorder(__cvStream);
    __cvRec.ondataavailable=function(e){if(e.data&&e.data.size)__cvChunks.push(e.data);};
    __cvRec.start(250);
    __cvSpeech=0;__cvSil=0;__cvVoiced=0;__cvRecT=Date.now();
  }catch(_){__cvRec=null;}
}
function __cvRecDrop(){
  var r=__cvRec;__cvRec=null;
  if(r){r.ondataavailable=null;r.onstop=null;try{if(r.state!=='inactive')r.stop();}catch(_){}}
  __cvChunks=[];__cvSpeech=0;__cvSil=0;__cvVoiced=0;
}
function __cvRecSend(){
  var r=__cvRec;if(!r)return;__cvRec=null;
  var mime=r.mimeType||'audio/webm';
  r.onstop=function(){
    var blob=new Blob(__cvChunks,{type:mime});__cvChunks=[];
    __cvSpeech=0;__cvSil=0;__cvVoiced=0;
    __cvTranscribe(blob,mime);
  };
  callBusy=true;
  try{r.stop();}catch(_){callBusy=false;}
}
function __cvTranscribe(blob,mime){
  var KEY=localStorage.getItem('saathi_api_key');
  var rd=new FileReader();
  rd.onload=function(){
    var b64=String(rd.result).split(',')[1]||'';
    fetch(SAATHI_API_BASE+'/v1/stt',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({audio:b64,mime:mime,lang:'hi'})})
    .then(function(r){if(!r.ok){var e=new Error('stt '+r.status);e.status=r.status;throw e;}return r.json();})
    .then(function(d){
      var t=String((d&&d.text)||'').trim();
      if(!callActive){callBusy=false;return;}
      if(t.length<2||/^(thank you|thanks for watching|you)\W*$/i.test(t)){callBusy=false;return;}
      addLiveUserText(t);__cvPend=t;clearTimeout(__cvT);__cvSend();
    }).catch(function(e){
      callBusy=false;
      if(e&&(e.status===404||e.status===405||e.status===503)){window.__cvMic=false;__cvMicClose();showToast('Naya mic server abhi ready nahi hai, purana mic chal raha hai');if(callActive)listenOnce();}
      else showToast('Awaaz samajh nahi aayi, dobara boliye');
    });
  };
  rd.readAsDataURL(blob);
}
function __cvTick(){
  if(!callActive){__cvMicClose();return;}
  if(callMuted||callBusy||window.__cvMic===false){if(__cvRec)__cvRecDrop();return;}
  if(!__cvStream||!__cvAn)return;
  if(!__cvRec){__cvRecStart();if(!__cvRec)return;}
  __cvAn.getByteTimeDomainData(__cvBuf);
  var sum=0;for(var i=0;i<__cvBuf.length;i++){var v=(__cvBuf[i]-128)/128;sum+=v*v;}
  var rms=Math.sqrt(sum/__cvBuf.length),th=Math.max(0.02,__cvFloor*3);
  if(rms>th){__cvVoiced+=60;__cvSil=0;if(__cvVoiced>=200)__cvSpeech=1;}
  else{__cvSil+=60;if(!__cvSpeech){__cvFloor=__cvFloor*0.95+rms*0.05;__cvVoiced=0;}}
  var now=Date.now();
  if(__cvSpeech&&(__cvSil>=1700||now-__cvRecT>60000)){__cvRecSend();return;}
  if(!__cvSpeech&&now-__cvRecT>15000)__cvRecDrop();
}
"""

EDITS=[
 ("function startCall(){callActive=true;callMuted=false;",
  SITE+"function startCall(){callActive=true;callMuted=false;"),
 ("function listenOnce(){if(!callActive||callMuted||callBusy)return;",
  "function listenOnce(){if(!callActive||callMuted||callBusy)return;if(window.__cvMic!==false){__cvMicOpen();return;}"),
 ("function stopCall(){callActive=false;callMuted=false;__cvStop();",
  "function stopCall(){callActive=false;callMuted=false;__cvMicClose();__cvStop();"),
 ("while(s.length>0&&out.length<4)",
  "while(s.length>0&&out.length<12)"),
]

if '/*callvoice*/' not in ht:
    print('callstt: pehle 46_callvoice laga hona chahiye')
elif '/*callstt*/' in ht and '/v1/stt' in sv:
    print('callstt: pehle se laga hai')
else:
    bad=[]
    if sv.count('@app.post("/v1/tts")')!=1: bad.append('server /v1/tts')
    if '/v1/stt' in sv: bad.append('server pehle se /v1/stt hai')
    for a,_ in EDITS:
        if ht.count(a)!=1: bad.append(a[:45])
    if bad:
        print('callstt: jagah nahi mili ->',bad)
    else:
        sv=sv.replace('@app.post("/v1/tts")',SERVER+'@app.post("/v1/tts")',1)
        for a,b in EDITS:
            ht=ht.replace(a,b,1)
        open(SP,'w',encoding='utf-8').write(sv)
        open(HP,'w',encoding='utf-8').write(ht)
        print('callstt: laga diya')
