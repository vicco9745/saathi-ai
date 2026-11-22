import re
p='index.html'
s=open(p,encoding='utf-8').read()
new=r"""/*ttsfast57*/
    var __ps=(function(t){var out=[],s=String(t);while(s.length>0&&out.length<30){if(s.length<=150){out.push(s);break;}var cut=-1,m,re=/[\u0964.!?]\s/g,head=s.slice(0,150);while((m=re.exec(head))!==null)cut=m.index+1;if(cut<40)cut=s.lastIndexOf(' ',150);if(cut<1)cut=150;out.push(s.slice(0,cut).trim());s=s.slice(cut).trim();}return out;})(text),__jb=[];
    var __ld=function(i){if(i<__ps.length&&!__jb[i])__jb[i]=fetch(SAATHI_API_BASE+'/v1/tts',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':localStorage.getItem('saathi_api_key')},body:JSON.stringify({text:__ps[i],lang:lang})}).then(function(r){if(!r.ok)throw new Error('tts');return r.blob();});return __jb[i];};
    var __fail=function(i){if(my!==srvTok)return;srvAudio=null;setVoiceBtnState(btnEl,false);if(i===0)fb();else if(onEnd)onEnd();};
    var __pl=function(i){
      if(my!==srvTok)return;
      if(i>=__ps.length){srvAudio=null;setVoiceBtnState(btnEl,false);if(onEnd)onEnd();return;}
      __ld(i).then(function(b){
        if(my!==srvTok)return;
        __ld(i+1);
        const a=new Audio(URL.createObjectURL(b));srvAudio=a;
        a.onended=function(){if(my!==srvTok)return;__pl(i+1);};
        a.onerror=function(){__fail(i);};
        const pr=a.play();
        if(pr&&pr.catch)pr.catch(function(){__fail(i);});
      }).catch(function(){__fail(i);});
    };
    __ld(0);__ld(1);__pl(0);
"""
pat=re.compile(r"    fetch\(SAATHI_API_BASE\+'/v1/tts'.*?\.catch\(function\(\)\{if\(my!==srvTok\)return;setVoiceBtnState\(btnEl,false\);fb\(\);\}\);\n(?=    return true;)",re.S)
n=len(pat.findall(s))
if 'ttsfast57' in s:
    print('ttsfast: pehle se laga hai')
elif n==1:
    open(p,'w',encoding='utf-8').write(pat.sub(lambda m:new,s,count=1))
    print('ttsfast: laga diya')
else:
    print('ttsfast: jagah nahi mili',n)
