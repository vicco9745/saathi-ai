p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __imgWait(url){return new Promise(function(resolve,reject){var tries=0;function go(){tries++;var u=tries===1?url:url+(url.indexOf('?')>-1?'&':'?')+'seed='+Math.floor(Math.random()*1e9);var im=new Image(),done=false;var to=setTimeout(function(){if(done)return;done=true;im.onload=im.onerror=null;reject(new Error('timeout'));},300000);im.onload=function(){if(done)return;done=true;clearTimeout(to);resolve(u);};im.onerror=function(){if(done)return;done=true;clearTimeout(to);if(tries<3)setTimeout(go,2500);else reject(new Error('fail'));};im.src=u;}go();});}
"""
a1 = 'function linkifyText(text){'
old = ".then(data=>{const imgSrc=data.image_url||(data.image_base64?('data:image/png;base64,'+data.image_base64):null);pendingReply.generating=false;"
new = ".then(async data=>{let imgSrc=data.image_url||(data.image_base64?('data:image/png;base64,'+data.image_base64):null);if(imgSrc&&imgSrc.indexOf('http')===0){try{imgSrc=await __imgWait(imgSrc);}catch(_){imgSrc=null;}}pendingReply.generating=false;"
if '__imgWait' in s:
    print('imgwait: pehle se laga hai')
elif s.count(a1) == 1 and s.count(old) == 1:
    s = s.replace(a1, FN + a1, 1)
    s = s.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('imgwait: laga diya')
else:
    print('imgwait: jagah nahi mili', s.count(a1), s.count(old))
