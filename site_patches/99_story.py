p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""/*story*/function __buildStoryCard(m){
const st=m.story||{};const sc=Array.isArray(st.scenes)?st.scenes:[];
const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
if(!document.getElementById('story-css')){const css=document.createElement('style');css.id='story-css';css.textContent=`
.story-card{background:var(--panel-bg);border:1px solid var(--border);border-radius:22px;margin:12px 0;padding:18px;white-space:normal;text-align:left;width:100%}
.story-meta{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.story-tag{display:inline-flex;align-items:center;gap:6px;background:var(--accent-soft);color:var(--accent);font-size:13px;font-weight:600;padding:4px 12px;border-radius:999px}
.story-time{display:inline-flex;align-items:center;gap:5px;color:var(--text-muted);font-size:13px}
.story-card svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
.story-meta svg{width:15px;height:15px}
.story-title{font-size:24px;line-height:1.35;font-weight:700;color:var(--text);margin-bottom:18px}
.st-scene{margin-bottom:22px}
.st-pic{width:100%;aspect-ratio:16/10;background:var(--page-bg);border:1px dashed var(--border);border-radius:16px;margin-bottom:12px}
.st-scene p{font-size:17px;line-height:1.8;color:var(--text)}
.story-actions{display:flex;gap:10px;flex-wrap:wrap;border-top:1px solid var(--border);padding-top:16px}
.story-btn{display:inline-flex;align-items:center;gap:8px;background:var(--panel-bg);color:var(--text);border:1px solid var(--border);border-radius:12px;padding:10px 16px;font-size:15px;font-family:inherit;cursor:pointer}
.story-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
`;document.head.appendChild(css);}
const full=(st.title?st.title+'\n\n':'')+sc.map(x=>x.text).join('\n\n');
const mins=st.minutes||Math.max(1,Math.round(full.length/900));
const el=document.createElement('div');el.className='story-card';
el.innerHTML=`<div class="story-meta"><span class="story-tag"><svg viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/></svg>कहानी</span><span class="story-time"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>${mins} मिनट पढ़ने में</span></div>
<div class="story-title">${esc(st.title)}</div>
${sc.map(x=>`<div class="st-scene"><div class="st-pic"></div><p>${esc(x.text)}</p></div>`).join('')}
<div class="story-actions">
<button class="story-btn primary st-listen"><svg viewBox="0 0 24 24"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>सुनो</button>
<button class="story-btn st-again"><svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/></svg>फिर से</button>
<button class="story-btn st-copy"><svg viewBox="0 0 24 24"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>कॉपी</button>
<button class="story-btn st-share"><svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>शेयर</button>
</div>`;
el.querySelector('.st-listen').onclick=()=>{try{if(typeof speakText==='function'){speakText(full);}else{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(full);u.lang='hi-IN';speechSynthesis.speak(u);}}catch(_){}};
el.querySelector('.st-copy').onclick=()=>{try{navigator.clipboard.writeText(full);}catch(_){}};
el.querySelector('.st-share').onclick=()=>{try{if(navigator.share)navigator.share({title:st.title||'कहानी',text:full});}catch(_){}};
return el;}
/*storytest*/setTimeout(function(){try{if(location.hash!=='#storytest')return;const c=getCurrentChat();if(!c)return;c.messages.push({role:'ai',story:{title:'पुराने स्टेशन की घड़ी',scenes:[{text:'गाँव के छोटे स्टेशन पर एक पुरानी घड़ी लगी थी। उसकी सुइयाँ बरसों से सात बजकर दस मिनट पर रुकी थीं।'},{text:'एक दिन शहर से एक लड़की आई, नाम था अनु। उसने घड़ी को देर तक देखा, फिर सीढ़ी माँगी।'},{text:'शाम तक अनु ने ज़ंग लगे पुर्ज़े साफ़ किए और चाबी घुमाई। टिक। फिर टिक, टिक। सुइयाँ चल पड़ीं।'}]}});renderMessages();}catch(_){}},1500);
"""
a1 = 'function renderMessages(){'
a2 = "if(attachments.length>0)row.appendChild(buildAttachmentsBlock(attachments));"
a3 = "if(d.kind==='image'&&d.image_url){"
n2 = "if(m.role==='ai'&&m.story&&!m.typing){row.appendChild(__buildStoryCard(m));messagesList.appendChild(row);return;}" + a2
n3 = "if(d.kind==='story'&&d.story){m.typing=false;m.processing=null;m.text='';m.story=d.story;try{saveChats();renderMessages();clearTypingState();updateActionButton();}catch(_){}return true;}" + a3
if '/*story*/' in s:
    print('story: pehle se laga hai')
elif s.count(a1) == 1 and s.count(a2) == 1 and s.count(a3) == 1:
    s = s.replace(a1, FN + a1, 1).replace(a2, n2, 1).replace(a3, n3, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('story: laga diya')
else:
    print('story: jagah nahi mili', s.count(a1), s.count(a2), s.count(a3))
