p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""/*budget*/const __BK='saathi_budgets_v1';
const __BCATS=['खाना','किराया','बिजली / बिल','यात्रा','दवाई','पढ़ाई','मनोरंजन','खरीदारी'];
function __bLoad(){try{const a=JSON.parse(localStorage.getItem(__BK)||'[]');return Array.isArray(a)?a:[];}catch(_){return [];}}
function __bSave(a){try{localStorage.setItem(__BK,JSON.stringify(a));}catch(_){}}
function __bNum(v){const n=parseFloat(String(v==null?'':v).replace(/[^0-9.]/g,''));return isFinite(n)?n:0;}
function __bFmt(n){return '₹'+Math.round(n).toLocaleString('en-IN');}
function __bEsc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function __bDate(ts){try{return new Date(ts).toLocaleDateString('hi-IN',{day:'numeric',month:'long',year:'numeric'});}catch(_){return '';}}
function __bSv(n){return (n<0?'−':'')+__bFmt(Math.abs(n));}
function __bK(b){return '<div class="bd-kpis"><div><span>बजट</span><b>'+__bFmt(b.total)+'</b></div><div><span>खर्च</span><b>'+__bFmt(b.spent)+'</b></div><div><span>बचत</span><b class="'+(b.saved<0?'bd-neg':'')+'">'+__bSv(b.saved)+'</b></div></div>';}
function __bItems(b){return (b.items||[]).map(function(it){return '<div class="bd-li"><span>'+__bEsc(it.n)+'</span><span>'+__bFmt(it.amt)+'</span></div>';}).join('');}
function __bTot(list){return list.reduce(function(a,b){return {total:a.total+b.total,spent:a.spent+b.spent,saved:a.saved+b.saved};},{total:0,spent:0,saved:0});}
const __bPdfIcon='<svg viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/></svg>';
function __bCss(){if(document.getElementById('bd-css'))return;const c=document.createElement('style');c.id='bd-css';c.textContent=`
.bd-card{background:var(--panel-bg);border:1px solid var(--border);border-radius:22px;margin:12px 0;padding:18px;white-space:normal;text-align:left;width:100%;color:var(--text)}
.bd-card svg,.bd-pg svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
.bd-title{font-size:20px;font-weight:700;margin-bottom:14px}
.bd-lbl{display:block;font-size:14px;color:var(--text-muted);margin:12px 0 6px}
.bd-in{width:100%;padding:10px 12px;border:1px solid var(--border);border-radius:12px;background:var(--bg);color:var(--text);font-family:inherit;font-size:16px;outline:none}
.bd-in:focus{border-color:var(--accent)}
.bd-row{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.bd-chk{display:flex;align-items:center;gap:8px;flex:1;font-size:16px}
.bd-chk input{width:20px;height:20px;accent-color:var(--accent)}
.bd-amt{width:120px;flex:none}
.bd-add{display:flex;gap:8px;margin-top:6px}
.bd-sum{display:flex;justify-content:space-between;margin:12px 0 0;font-size:15px}
.bd-err{color:var(--danger);font-size:14px;min-height:20px;margin-top:6px}
.bd-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--panel-bg);color:var(--text);border:1px solid var(--border);border-radius:12px;padding:10px 16px;font-size:15px;font-family:inherit;cursor:pointer}
.bd-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;width:100%;margin-top:10px;padding:12px}
.bd-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.bd-kpis div{background:var(--accent-soft);border-radius:14px;padding:10px;text-align:center}
.bd-kpis span{display:block;font-size:12px;color:var(--text-muted)}
.bd-kpis b{font-size:16px}
.bd-li{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:15px}
.bd-acts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.bd-pg{position:fixed;inset:0;z-index:99999;background:var(--page-bg);overflow:auto;padding:16px;color:var(--text)}
.bd-pg-in{max-width:640px;margin:0 auto}
.bd-pg-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.bd-neg{color:var(--danger)}
`;document.head.appendChild(c);}
function __budgetPdf(list){
const tt=__bTot(list);
const css='body{font-family:"Noto Sans Devanagari",sans-serif;color:#111;padding:24px}h1{font-size:22px}h2{font-size:18px;margin:22px 0 4px}table{width:100%;border-collapse:collapse;margin-top:8px}td,th{border:1px solid #ccc;padding:6px 8px;text-align:left;font-size:14px}.k{display:flex;gap:18px;margin:6px 0;font-size:15px}.b{page-break-inside:avoid}';
let h='<!DOCTYPE html><html lang="hi"><head><meta charset="utf-8"><title>Saathi बजट रिपोर्ट</title><style>'+css+'</style></head><body><h1>Saathi — बजट रिपोर्ट</h1>';
if(list.length>1)h+='<div class="k"><b>कुल बजट: '+__bFmt(tt.total)+'</b><b>कुल खर्च: '+__bFmt(tt.spent)+'</b><b>कुल बचत: '+__bSv(tt.saved)+'</b></div>';
list.forEach(function(b){h+='<div class="b"><h2>'+__bEsc(b.name)+'</h2><div>'+__bDate(b.ts)+'</div><div class="k"><span>बजट: '+__bFmt(b.total)+'</span><span>खर्च: '+__bFmt(b.spent)+'</span><span>बचत: '+__bSv(b.saved)+'</span></div><table><tr><th>खर्च</th><th>रकम</th></tr>'+(b.items||[]).map(function(it){return '<tr><td>'+__bEsc(it.n)+'</td><td>'+__bFmt(it.amt)+'</td></tr>';}).join('')+'</table></div>';});
h+='</body></html>';
const f=document.createElement('iframe');f.style.cssText='position:fixed;right:0;bottom:0;width:0;height:0;border:0';document.body.appendChild(f);
const d=f.contentWindow.document;d.open();d.write(h);d.close();
setTimeout(function(){try{f.contentWindow.focus();f.contentWindow.print();}catch(_){}setTimeout(function(){try{f.remove();}catch(_){}},60000);},500);}
function __budgetPage(){__bCss();const old=document.getElementById('bd-pg');if(old)old.remove();
const list=__bLoad();const pg=document.createElement('div');pg.className='bd-pg';pg.id='bd-pg';
const x='<svg viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>';
pg.innerHTML='<div class="bd-pg-in"><div class="bd-pg-top"><div class="bd-title" style="margin:0">मेरे बजट</div><button class="bd-btn" id="bd-x">'+x+'</button></div>'
+(list.length?__bK(__bTot(list))+list.slice().reverse().map(function(b){return '<div class="bd-card"><div class="bd-title">'+__bEsc(b.name)+'</div><div style="font-size:13px;color:var(--text-muted);margin:-8px 0 12px">'+__bDate(b.ts)+'</div>'+__bK(b)+__bItems(b)+'</div>';}).join('')+'<button class="bd-btn primary" id="bd-pdf">'+__bPdfIcon+'PDF</button>':'<div class="bd-card">अभी कोई बजट सेव नहीं है।</div>')+'</div>';
document.body.appendChild(pg);
pg.querySelector('#bd-x').onclick=function(){pg.remove();};
const pb=pg.querySelector('#bd-pdf');if(pb)pb.onclick=function(){__budgetPdf(list);};}
function __buildBudgetCard(m){__bCss();
const el=document.createElement('div');el.className='bd-card';
const bd=m.budget||{};
function drawForm(){
const d=bd.draft=bd.draft||{};d.items=d.items||__BCATS.map(function(n){return {n:n,on:false,amt:''};});
el.innerHTML='<div class="bd-title">नया बजट</div>'
+'<label class="bd-lbl">नाम</label><input class="bd-in" id="bn" placeholder="जैसे: घर का बजट" value="'+__bEsc(d.name||'')+'">'
+'<label class="bd-lbl">कुल बजट (₹)</label><input class="bd-in" id="bt" type="number" inputmode="decimal" value="'+__bEsc(d.total||'')+'">'
+'<label class="bd-lbl">खर्च — टिक लगाओ और रकम भरो</label>'
+d.items.map(function(it,i){return '<div class="bd-row"><label class="bd-chk"><input type="checkbox" data-i="'+i+'"'+(it.on?' checked':'')+'><span>'+__bEsc(it.n)+'</span></label><input class="bd-in bd-amt" type="number" inputmode="decimal" data-a="'+i+'" placeholder="₹" value="'+__bEsc(it.amt||'')+'"'+(it.on?'':' disabled')+'></div>';}).join('')
+'<div class="bd-add"><input class="bd-in" id="bc" placeholder="अपना खर्च जोड़ें"><button class="bd-btn" id="ba">+</button></div>'
+'<div class="bd-sum"><span>कुल खर्च</span><b id="bs">₹0</b></div><div class="bd-sum"><span>बचत</span><b id="bv">₹0</b></div>'
+'<div class="bd-err" id="be"></div><button class="bd-btn primary" id="bsub">सबमिट</button>';
function calc(){const tot=__bNum(d.total);let sp=0;d.items.forEach(function(it){if(it.on)sp+=__bNum(it.amt);});el.querySelector('#bs').textContent=__bFmt(sp);const sv=tot-sp;const v=el.querySelector('#bv');v.textContent=__bSv(sv);v.className=sv<0?'bd-neg':'';}
el.querySelector('#bn').oninput=function(e){d.name=e.target.value;};
el.querySelector('#bt').oninput=function(e){d.total=e.target.value;calc();};
el.querySelectorAll('input[data-i]').forEach(function(c){c.onchange=function(){const i=+c.dataset.i;d.items[i].on=c.checked;const a=el.querySelector('input[data-a="'+i+'"]');a.disabled=!c.checked;if(c.checked)a.focus();calc();try{saveChats();}catch(_){}};});
el.querySelectorAll('input[data-a]').forEach(function(a){a.oninput=function(){d.items[+a.dataset.a].amt=a.value;calc();};});
el.querySelector('#ba').onclick=function(){const n=el.querySelector('#bc').value.trim();if(!n)return;d.items.push({n:n,on:true,amt:''});drawForm();};
el.querySelector('#bsub').onclick=function(){
const name=String(d.name||'').trim();const tot=__bNum(d.total);const err=el.querySelector('#be');
if(!name){err.textContent='नाम लिखो';return;}
if(!(tot>0)){err.textContent='कुल बजट लिखो';return;}
const items=d.items.filter(function(it){return it.on&&__bNum(it.amt)>0;}).map(function(it){return {n:it.n,amt:__bNum(it.amt)};});
const sp=items.reduce(function(a,it){return a+it.amt;},0);
const rec={id:'b'+Date.now(),name:name,total:tot,items:items,spent:sp,saved:tot-sp,ts:Date.now()};
const list=__bLoad();list.push(rec);__bSave(list);
m.budget={mode:'saved',id:rec.id};try{saveChats();}catch(_){}
el.replaceWith(__buildBudgetCard(m));};
calc();}
function drawSaved(){const b=__bLoad().find(function(x){return x.id===bd.id;});
if(!b){el.innerHTML='<div class="bd-title">यह बजट अब नहीं मिला</div>';return;}
el.innerHTML='<div class="bd-title">'+__bEsc(b.name)+'</div>'+__bK(b)+__bItems(b)+'<div class="bd-acts"><button class="bd-btn" id="bp">'+__bPdfIcon+'PDF</button><button class="bd-btn" id="bo">सारे बजट</button></div>';
el.querySelector('#bp').onclick=function(){__budgetPdf([b]);};el.querySelector('#bo').onclick=function(){__budgetPage();};}
function drawAll(){const list=__bLoad();
if(!list.length){el.innerHTML='<div class="bd-title">अभी कोई बजट सेव नहीं है</div><button class="bd-btn primary" id="bn2">नया बजट बनाएँ</button>';el.querySelector('#bn2').onclick=function(){m.budget={mode:'form',draft:{}};try{saveChats();}catch(_){}el.replaceWith(__buildBudgetCard(m));};return;}
el.innerHTML='<div class="bd-title">मेरे बजट</div>'+__bK(__bTot(list))+list.slice(-5).reverse().map(function(b){return '<div class="bd-li"><span>'+__bEsc(b.name)+'</span><b class="'+(b.saved<0?'bd-neg':'')+'">बचत '+__bSv(b.saved)+'</b></div>';}).join('')+'<div class="bd-acts"><button class="bd-btn" id="bp">'+__bPdfIcon+'PDF</button><button class="bd-btn" id="bo">सब देखें</button></div>';
el.querySelector('#bp').onclick=function(){__budgetPdf(list);};el.querySelector('#bo').onclick=function(){__budgetPage();};}
if(bd.mode==='form')drawForm();else if(bd.mode==='saved')drawSaved();else drawAll();
return el;}
function __budgetHandle(m,text){try{
const t=String(text||'').trim();
if(!t||t.length>200||t.indexOf('=== file:')>-1||t.indexOf('```')>-1||t.charAt(0)==='/')return false;
if(/kaise|कैसे|how |what is|क्या होता|मतलब|tips|सलाह/i.test(t))return false;
const list=__bLoad();const hasB=/budget|बजट|bajat/i.test(t);const low=t.toLowerCase();
let hit=null;
for(let i=0;i<list.length;i++){const n=String(list[i].name||'').trim().toLowerCase();if(!n)continue;if(low===n||(hasB&&low.indexOf(n)>-1)){hit=list[i];break;}}
let mode=null;
if(hit)mode='one';
else if(hasB){if(/bana|बना|create|make|new|naya|नया|शुरू|shuru|start|setup|set up/i.test(t))mode='form';else if(/batao|बताओ|बताइए|dikha|दिखा|show|mera|मेरा|my|dekh|देख|kitna|कितना|bachat|बचत|saved|saving|report|pdf|list|history/i.test(t))mode='all';}
if(!mode)return false;
m.typing=false;m.processing=null;m.text='';
m.budget=mode==='form'?{mode:'form',draft:{}}:(mode==='one'?{mode:'saved',id:hit.id}:{mode:'all'});
try{const c=getCurrentChat();if(c&&c.title==='New chat'){c.title='बजट';c.__autoTitle=false;}}catch(_){}
try{saveChats();renderMessages();}catch(_){}
try{clearTypingState();updateActionButton();}catch(_){}
return true;}catch(_){return false;}}
"""
a1 = 'function renderMessages(){'
R = [
(r"""if(m.role==='ai'&&m.story&&!m.typing){""",
 r"""if(m.role==='ai'&&m.budget&&!m.typing){row.appendChild(__buildBudgetCard(m));messagesList.appendChild(row);return;}if(m.role==='ai'&&m.story&&!m.typing){"""),
(r"""/*img-nat*/const imageMatch=(function(){""",
 r"""if(__budgetHandle(pendingReply,combinedText)){return;}/*img-nat*/const imageMatch=(function(){"""),
]
if 'function __budgetHandle' in s:
    print('budget: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad or s.count(a1) != 1:
        print('budget: jagah nahi mili', bad, s.count(a1))
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        s = s.replace(a1, FN + a1, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget: laga diya')
