p='index.html'
s=open(p,encoding='utf-8').read()
old="if(callMuted||callBusy||window.__cvMic===false){if(__cvRec)__cvRecDrop();return;}"
new=r"""if(callMuted||window.__cvMic===false){if(__cvRec)__cvRecDrop();return;}/*bargein59*/
  if(callBusy){
    if(window.__saathiSpeaking&&__cvStream&&__cvAn){
      __cvAn.getByteTimeDomainData(__cvBuf);var s2=0;for(var j=0;j<__cvBuf.length;j++){var v2=(__cvBuf[j]-128)/128;s2+=v2*v2;}
      if(Math.sqrt(s2/__cvBuf.length)>(window.__cvBIth||0.07)){window.__cvBI=(window.__cvBI||0)+60;}else{window.__cvBI=0;}
      if(window.__cvBI>=300){window.__cvBI=0;try{__cvStop();}catch(_){}try{__cvCapHide();}catch(_){}callBusy=false;if(__cvRec)__cvRecDrop();__cvRecStart();if(__cvRec){__cvSpeech=1;__cvVoiced=300;__cvSil=0;}}
    }else{window.__cvBI=0;if(__cvRec)__cvRecDrop();}
    return;
  }"""
if 'bargein59' in s:
    print('bargein: pehle se laga hai')
elif s.count(old)==1:
    open(p,'w',encoding='utf-8').write(s.replace(old,new,1))
    print('bargein: laga diya')
else:
    print('bargein: jagah nahi mili',s.count(old))
