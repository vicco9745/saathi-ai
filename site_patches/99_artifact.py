p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __buildArtifactCard(m){
if(!document.getElementById('af-css')){const c=document.createElement('style');c.id='af-css';c.textContent=`
.af-card{background:var(--panel-bg);border:1px solid var(--border);border-radius:22px;margin:12px 0;padding:12px;width:100%;white-space:normal;text-align:left;animation:afin .5s ease}
@keyframes afin{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.af-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px}
.af-t{font-size:16px;font-weight:700;color:var(--text);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.af-b{display:flex;gap:4px;flex:none}
.af-btn{width:38px;height:38px;border:none;background:transparent;color:var(--text-soft);display:flex;align-items:center;justify-content:center;border-radius:10px;cursor:pointer;padding:0}
.af-btn svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.af-fr{width:100%;height:440px;border:1px solid var(--border);border-radius:14px;background:#fff;display:block}
.af-full{position:fixed;inset:0;z-index:99999;background:var(--page-bg);display:flex;flex-direction:column;padding:10px}
.af-full .af-fr{flex:1;height:auto}
`;document.head.appendChild(c);}
const a=m.artifact||{};
const esc=function(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
const ic={full:'<svg viewBox="0 0 24 24"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>',copy:'<svg viewBox="0 0 24 24"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>',dl:'<svg viewBox="0 0 24 24"><path d="M12 3v12m0 0 4-4m-4 4-4-4M5 21h14"/></svg>',x:'<svg viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>'};
const el=document.createElement('div');el.className='af-card';
el.innerHTML='<div class="af-head"><span class="af-t">'+esc(a.title||'')+'</span><span class="af-b"><button class="af-btn" data-k="full">'+ic.full+'</button><button class="af-btn" data-k="copy">'+ic.copy+'</button><button class="af-btn" data-k="dl">'+ic.dl+'</button></span></div><iframe class="af-fr" sandbox="allow-scripts allow-forms" referrerpolicy="no-referrer"></iframe>';
el.querySelector('iframe').srcdoc=String(a.html||'');
el.querySelector('[data-k="full"]').onclick=function(){const o=document.createElement('div');o.className='af-full';o.innerHTML='<div class="af-head"><span class="af-t">'+esc(a.title||'')+'</span><button class="af-btn" data-k="x">'+ic.x+'</button></div><iframe class="af-fr" sandbox="allow-scripts allow-forms" referrerpolicy="no-referrer"></iframe>';o.querySelector('iframe').srcdoc=String(a.html||'');o.querySelector('[data-k="x"]').onclick=function(){o.remove();};document.body.appendChild(o);};
el.querySelector('[data-k="copy"]').onclick=function(){try{navigator.clipboard.writeText(String(a.html||''));}catch(_){}};
el.querySelector('[data-k="dl"]').onclick=function(){try{const b=new Blob([String(a.html||'')],{type:'text/html'});const u=URL.createObjectURL(b);const l=document.createElement('a');l.href=u;l.download=(String(a.title||'saathi').replace(/[^\w\u00C0-\uFFFF ]+/g,'').trim().slice(0,40)||'saathi')+'.html';document.body.appendChild(l);l.click();l.remove();setTimeout(function(){URL.revokeObjectURL(u);},4000);}catch(_){}};
return el;}
"""
a1 = 'function renderMessages(){'
R = [
(r"""if(m.role==='ai'&&m.budget&&!m.typing){""",
 r"""if(m.role==='ai'&&m.artifact&&!m.typing){row.appendChild(__buildArtifactCard(m));if(m.text){const _ab=document.createElement('div');_ab.className='bubble';_ab.innerHTML=linkifyText(m.text);row.appendChild(_ab);}row.appendChild(buildMessageActions(m,idx,chat,idx===lastAiIdx));messagesList.appendChild(row);return;}if(m.role==='ai'&&m.budget&&!m.typing){"""),
(r"""if(d.kind==='image'&&d.image_url){""",
 r"""if(d.kind==='artifact'&&d.html){m.typing=false;m.processing=null;m.text=String(d.reply||'');m.artifact={title:String(d.title||''),html:String(d.html)};try{saveChats();renderMessages();clearTypingState();updateActionButton();}catch(_){}return true;}if(d.kind==='image'&&d.image_url){"""),
]
if 'function __buildArtifactCard' in s:
    print('artifact: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad or s.count(a1) != 1:
        print('artifact: jagah nahi mili', bad, s.count(a1))
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        s = s.replace(a1, FN + a1, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('artifact: laga diya')
