p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __sfCap(){
var P=function(t,m){try{parent.postMessage({__sf:1,t:t,m:String(m).slice(0,300)},'*');}catch(e){}};
window.addEventListener('error',function(e){var x=e.target;if(x&&x!==window&&x.tagName){var src=x.src||x.href||'';var bad=x.tagName!=='IMG'||/unsplash|^$/.test(src);P(bad?'error':'warn','file failed to load: '+x.tagName+' '+src);}else{P('error',(e.message||'Error')+(e.lineno?' (line '+e.lineno+')':''));}},true);
window.addEventListener('unhandledrejection',function(e){P('error','Promise: '+((e.reason&&e.reason.message)||e.reason));});
var ce=console.error;console.error=function(){P('error',[].slice.call(arguments).join(' '));try{ce.apply(console,arguments);}catch(e){}};
window.addEventListener('load',function(){
if(!document.querySelector('meta[name=viewport]'))P('error','viewport meta tag missing');
P('done','');
});
}
function __sfRun(html){return new Promise(function(res){
var logs=[];var fr=document.createElement('iframe');
fr.setAttribute('sandbox','allow-scripts allow-forms');
fr.style.cssText='position:fixed;width:390px;height:700px;left:-9999px;top:0;border:0';
var inj='<scr'+'ipt>('+__sfCap.toString()+')();</scr'+'ipt>';
fr.srcdoc=/<head[^>]*>/i.test(html)?html.replace(/<head[^>]*>/i,function(x){return x+inj;}):inj+html;
var fin=false;
var end=function(){if(fin)return;fin=true;window.removeEventListener('message',h);try{fr.remove();}catch(e){}res(logs);};
var h=function(e){if(e.source!==fr.contentWindow||!e.data||!e.data.__sf)return;if(e.data.t==='done'){setTimeout(end,1200);return;}logs.push({t:e.data.t,m:e.data.m});};
window.addEventListener('message',h);document.body.appendChild(fr);setTimeout(end,5000);
});}
async function __siteFix(html,prompt,m){
var cur=String(html||'');
try{
for(var round=1;round<=4;round++){
var logs=await __sfRun(cur);
var errs=logs.filter(function(l){return l.t==='error';});
if(!errs.length)return cur;
if(round===4)break;
var r=await fetch(SAATHI_API_BASE+'/v1/website-fix',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({html:cur,errors:errs.map(function(l){return l.m;}).join('\n')})});
var d=await r.json();
if(d&&d.html&&d.html!==cur){cur=d.html;}else break;
}
}catch(_){}
return cur;}
"""
a1 = 'function renderMessages(){'
old_call = "return data;}).then(data=>{const html=data.html||data.code;"
new_call = "return data;}).then(async data=>{try{if(data&&(data.html||data.code)){data.html=await __siteFix(data.html||data.code,sitePrompt,pendingReply);}}catch(_){}return data;}).then(data=>{const html=data.html||data.code;"
if 'function __siteCheck' in s:
    i = s.find('function __scCap(){')
    j = s.find('function renderMessages(){')
    if i >= 0 and j > i:
        s = s[:i] + s[j:]
    s = s.replace("try{__siteCheck(d.html);}catch(_){}", "").replace("try{__siteCheck(html);}catch(_){}", "")
    print('sitefix: purana sitecheck hata diya')
if 'function __siteFix' in s:
    print('sitefix: pehle se laga hai')
elif s.count(old_call) != 1 or s.count(a1) != 1:
    print('sitefix: jagah nahi mili', s.count(old_call), s.count(a1))
else:
    s = s.replace(old_call, new_call, 1)
    s = s.replace(a1, FN + a1, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('sitefix: laga diya')
