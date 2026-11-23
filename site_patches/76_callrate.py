p='index.html'
s=open(p,encoding='utf-8').read()
fb=r"""/*callrate76*/function __callRate(){try{var old=document.getElementById('callRateBox');if(old)old.remove();var comp=document.querySelector('.composer');var b=document.createElement('div');b.id='callRateBox';var ic=function(p){return '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+p+'</svg>';};b.innerHTML='<span>How was this conversation?</span><button type="button" data-r="up" aria-label="Good">'+ic(THUMB_UP)+'</button><button type="button" data-r="down" aria-label="Bad">'+ic(THUMB_DOWN)+'</button>';b.style.cssText='position:fixed;left:12px;right:12px;z-index:60;display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:20px;background:var(--icon-hover,#f0f0f2);color:var(--text,#1a1c2e);font-size:15px;transition:opacity .3s;opacity:0';var r=comp?comp.getBoundingClientRect():null;b.style.bottom=(r?Math.max(10,window.innerHeight-r.top+10):90)+'px';b.querySelector('span').style.cssText='flex:1';b.querySelectorAll('button').forEach(function(x){x.style.cssText='border:none;background:transparent;color:inherit;padding:6px;cursor:pointer;display:flex';});document.body.appendChild(b);requestAnimationFrame(function(){b.style.opacity='1';});var gone=function(){b.style.opacity='0';setTimeout(function(){b.remove();},300);};var t=setTimeout(gone,7000);b.addEventListener('click',function(e){var x=e.target.closest('button');if(!x)return;clearTimeout(t);try{var up=x.getAttribute('data-r')==='up',key=(up?THUMB_UP:THUMB_DOWN).slice(0,24);var rows=document.querySelectorAll('.msg-row.ai .msg-actions');var last=rows[rows.length-1];var bt=last?last.querySelectorAll('.msg-action-btn'):[];for(var i=0;i<bt.length;i++){if(bt[i].innerHTML.indexOf(key)>-1){bt[i].click();break;}}}catch(_){}gone();});}catch(_){}}
"""
pairs=[
("function startCall(){__snd('open');", fb+"function startCall(){__snd('open');"),
("if(callActive)__snd('end');", "if(callActive){__snd('end');setTimeout(__callRate,500);}"),
]
if 'callrate76' in s:
    print('callrate: pehle se laga hai')
else:
    cnt=[s.count(a) for a,b in pairs]
    if cnt==[1,1]:
        for a,b in pairs:
            s=s.replace(a,b,1)
        open(p,'w',encoding='utf-8').write(s)
        print('callrate: laga diya')
    else:
        print('callrate: jagah nahi mili',cnt)
