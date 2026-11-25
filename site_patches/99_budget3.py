p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""/*budget3*/const __BK='saathi_budgets_v1';
const __BHI={newBudget:'नया बजट',name:'नाम',nameHint:'जैसे: घर का बजट',total:'कुल बजट',totalHint:'रकम लिखो',expTitle:'खर्च — टिक लगाओ और रकम भरो',addOwn:'अपना खर्च जोड़ें',totalSpent:'कुल खर्च',saving:'बचत',submit:'सबमिट',needName:'नाम लिखो',needTotal:'कुल बजट लिखो',budget:'बजट',spent:'खर्च',myBudgets:'मेरे बजट',seeAll:'सारे बजट',noBudget:'अभी कोई बजट सेव नहीं है',createNew:'नया बजट बनाएँ',notFound:'यह बजट अब नहीं मिला',report:'बजट रिपोर्ट',expense:'खर्च',amount:'रकम',allTotalBudget:'कुल बजट',allTotalSpent:'कुल खर्च',allTotalSaving:'कुल बचत',c0:'खाना',c1:'किराया',c2:'बिजली / बिल',c3:'यात्रा',c4:'दवाई',c5:'पढ़ाई',c6:'मनोरंजन',c7:'खरीदारी'};
const __BEN={newBudget:'New Budget',name:'Name',nameHint:'e.g. Home budget',total:'Total budget',totalHint:'Enter amount',expTitle:'Expenses — tick and enter amount',addOwn:'Add your own expense',totalSpent:'Total spent',saving:'Savings',submit:'Submit',needName:'Enter a name',needTotal:'Enter the total budget',budget:'Budget',spent:'Spent',myBudgets:'My budgets',seeAll:'All budgets',noBudget:'No budget saved yet',createNew:'Create a new budget',notFound:'This budget was not found',report:'Budget Report',expense:'Expense',amount:'Amount',allTotalBudget:'Total budget',allTotalSpent:'Total spent',allTotalSaving:'Total savings',c0:'Food',c1:'Rent',c2:'Electricity / Bills',c3:'Travel',c4:'Medicine',c5:'Education',c6:'Entertainment',c7:'Shopping'};
const __bWordRe=/budget|बजट|bajat|presupuesto|orçamento|orcamento|budjet|bütçe|butce|anggaran|ngân sách|งบประมาณ|预算|預算|予算|예산|ميزانية|ميزانيه|بجٹ|بودجه|বাজেট|பட்ஜெட்|బడ్జెట్|ബജറ്റ്|ಬಜೆಟ್|બજેટ|ਬਜਟ|बजेट|бюджет|προϋπολογισμός|תקציב|begroting|budžet|rozpočet|költségvetés|buget|haushaltsplan/i;
const __bI={plus:'<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',user:'<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',rupee:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9 8h6M9 11h6M9 8c4 0 4 5 0 5l4 3"/></svg>',list:'<svg viewBox="0 0 24 24"><path d="M9 6h11M9 12h11M9 18h11"/><path d="m3.5 6 1.5 1.5L7.5 5M3.5 12l1.5 1.5L7.5 11M3.5 18l1.5 1.5L7.5 17"/></svg>',save:'<svg viewBox="0 0 24 24"><path d="M5 3h11l4 4v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M8 3v5h7V3M8 21v-7h8v7"/></svg>',pdf:'<svg viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/></svg>',x:'<svg viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>'};
function __bLoad(){try{const a=JSON.parse(localStorage.getItem(__BK)||'[]');return Array.isArray(a)?a:[];}catch(_){return [];}}
function __bSave(a){try{localStorage.setItem(__BK,JSON.stringify(a));}catch(_){}}
function __bNum(v){const n=parseFloat(String(v==null?'':v).replace(/[^0-9.]/g,''));return isFinite(n)?n:0;}
function __bEsc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function __bU(ui){const lang=(ui&&ui.lang)||'hi';const base=lang==='hi'?__BHI:__BEN;const L=Object.assign({},base,(ui&&ui.labels)||{});return {L:L,cur:(ui&&ui.cur)||'₹',lang:lang,loc:lang==='hi'?'hi-IN':(lang==='en'?'en-IN':lang)};}
function __bDir(el,u){if(/^(ar|he|iw|fa|ur|ps|sd|yi|ckb)/i.test(u.lang)){el.dir='rtl';el.style.textAlign='right';}else{el.dir='ltr';el.style.textAlign='left';}}
function __bFmt(n,u){const x=Math.round(n);let t;try{t=x.toLocaleString(u.loc);}catch(_){t=String(x);}return u.cur+t;}
function __bSv(n,u){return (n<0?'−':'')+__bFmt(Math.abs(n),u);}
function __bDate(ts,u){try{return new Date(ts).toLocaleDateString(u.loc,{day:'numeric',month:'long',year:'numeric'});}catch(_){return '';}}
function __bK(b,u,tot){const L=u.L;const a=tot?[L.allTotalBudget,L.allTotalSpent,L.allTotalSaving]:[L.budget,L.spent,L.saving];return '<div class="bd-kpis"><div><span>'+__bEsc(a[0])+'</span><b>'+__bFmt(b.total,u)+'</b></div><div><span>'+__bEsc(a[1])+'</span><b>'+__bFmt(b.spent,u)+'</b></div><div><span>'+__bEsc(a[2])+'</span><b class="'+(b.saved<0?'bd-neg':'')+'">'+__bSv(b.saved,u)+'</b></div></div>';}
function __bItems(b,u){return (b.items||[]).map(function(it){return '<div class="bd-li"><span>'+__bEsc(it.n)+'</span><span>'+__bFmt(it.amt,u)+'</span></div>';}).join('');}
function __bTot(list){return list.reduce(function(a,b){return {total:a.total+b.total,spent:a.spent+b.spent,saved:a.saved+b.saved};},{total:0,spent:0,saved:0});}
function __bCss(){if(document.getElementById('bd-css'))return;const c=document.createElement('style');c.id='bd-css';c.textContent=`
.bd-card,.bd-pg{--bd-p:#5b35e8;--bd-p2:#7a4cf5;--bd-soft:#ece8ff;--bd-ink:#1b1464;--bd-bd:#cfc8f3;--bd-bg:#ffffff;--bd-mut:#8a86b0}
[data-theme="dark"] .bd-card,[data-theme="dark"] .bd-pg{--bd-soft:#2a2550;--bd-ink:#ece9ff;--bd-bd:#4a4290;--bd-bg:#1c1a33;--bd-mut:#9a96c8}
.bd-card{background:linear-gradient(180deg,var(--bd-soft),var(--panel-bg) 55%);border:1px solid var(--bd-bd);border-radius:22px;margin:12px 0;padding:18px;white-space:normal;text-align:left;width:100%;color:var(--text);box-shadow:0 6px 20px rgba(91,53,232,.10)}
.bd-card svg,.bd-pg svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
.bd-head{display:inline-flex;align-items:center;gap:12px;background:var(--bd-soft);border-radius:18px;padding:6px 18px 6px 6px;margin-bottom:16px}
.bd-plus{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,var(--bd-p2),var(--bd-p));color:#fff;display:flex;align-items:center;justify-content:center}
.bd-plus svg{width:24px;height:24px;stroke-width:2.6}
.bd-htxt{font-size:19px;font-weight:700;color:var(--bd-ink)}
.bd-title{font-size:20px;font-weight:700;margin-bottom:14px;color:var(--bd-ink)}
.bd-fld{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px}
.bd-ic{width:42px;height:42px;border-radius:50%;background:var(--bd-soft);color:var(--bd-p);display:flex;align-items:center;justify-content:center;flex:none;margin-top:2px}
.bd-ic svg{width:22px;height:22px}
.bd-fb{flex:1;min-width:0}
.bd-lbl{display:block;font-size:16px;font-weight:700;color:var(--bd-ink);margin:0 0 6px}
.bd-lbl i{color:#e5484d;font-style:normal}
.bd-in{width:100%;padding:12px 14px;border:1.5px solid var(--bd-bd);border-radius:14px;background:var(--bd-bg);color:var(--bd-ink);font-family:inherit;font-size:16px;outline:none}
.bd-in::placeholder{color:var(--bd-mut)}
.bd-in:focus{border-color:var(--bd-p);box-shadow:0 0 0 3px rgba(91,53,232,.15)}
.bd-row{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.bd-chk{display:flex;align-items:center;gap:8px;flex:1;font-size:16px;color:var(--bd-ink)}
.bd-chk input{width:20px;height:20px;accent-color:var(--bd-p)}
.bd-amt{width:120px;flex:none}
.bd-add{display:flex;gap:8px;margin-top:6px}
.bd-sum{display:flex;justify-content:space-between;margin:12px 0 0;font-size:15px}
.bd-sum b,.bd-kpis b{color:var(--bd-ink)}
.bd-err{color:var(--danger);font-size:14px;min-height:20px;margin-top:6px}
.bd-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--panel-bg);color:var(--bd-ink);border:1px solid var(--bd-bd);border-radius:12px;padding:10px 16px;font-size:15px;font-family:inherit;cursor:pointer}
.bd-btn.primary{background:linear-gradient(135deg,var(--bd-p2),var(--bd-p));border:0;color:#fff;width:100%;margin-top:10px;padding:15px;border-radius:16px;font-size:18px;font-weight:700;box-shadow:0 8px 18px rgba(91,53,232,.30)}
.bd-btn.primary svg{width:22px;height:22px}
.bd-kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.bd-kpis div{background:var(--bd-soft);border-radius:14px;padding:10px;text-align:center}
.bd-kpis span{display:block;font-size:12px;color:var(--bd-mut)}
.bd-kpis b{font-size:16px}
.bd-li{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--bd-bd);font-size:15px;color:var(--bd-ink)}
.bd-acts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.bd-pg{position:fixed;inset:0;z-index:99999;background:var(--page-bg);overflow:auto;padding:16px;color:var(--text)}
.bd-pg-in{max-width:640px;margin:0 auto}
.bd-pg-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.bd-neg,.bd-kpis b.bd-neg,.bd-sum b.bd-neg{color:var(--danger)}
`;document.head.appendChild(c);}
function __budgetPdf(list,u){
const L=u.L;const tt=__bTot(list);
const css='body{font-family:"Noto Sans Devanagari","Noto Sans",sans-serif;color:#111;padding:24px}h1{font-size:22px}h2{font-size:18px;margin:22px 0 4px}table{width:100%;border-collapse:collapse;margin-top:8px}td,th{border:1px solid #ccc;padding:6px 8px;text-align:start;font-size:14px}.k{display:flex;gap:18px;margin:6px 0;font-size:15px;flex-wrap:wrap}.b{page-break-inside:avoid}';
const rtl=/^(ar|he|iw|fa|ur|ps|sd|yi|ckb)/i.test(u.lang);
let h='<!DOCTYPE html><html lang="'+__bEsc(u.lang)+'" dir="'+(rtl?'rtl':'ltr')+'"><head><meta charset="utf-8"><title>Saathi '+__bEsc(L.report)+'</title><style>'+css+'</style></head><body><h1>Saathi — '+__bEsc(L.report)+'</h1>';
if(list.length>1)h+='<div class="k"><b>'+__bEsc(L.allTotalBudget)+': '+__bFmt(tt.total,u)+'</b><b>'+__bEsc(L.allTotalSpent)+': '+__bFmt(tt.spent,u)+'</b><b>'+__bEsc(L.allTotalSaving)+': '+__bSv(tt.saved,u)+'</b></div>';
list.forEach(function(b){h+='<div class="b"><h2>'+__bEsc(b.name)+'</h2><div>'+__bDate(b.ts,u)+'</div><div class="k"><span>'+__bEsc(L.budget)+': '+__bFmt(b.total,u)+'</span><span>'+__bEsc(L.spent)+': '+__bFmt(b.spent,u)+'</span><span>'+__bEsc(L.saving)+': '+__bSv(b.saved,u)+'</span></div><table><tr><th>'+__bEsc(L.expense)+'</th><th>'+__bEsc(L.amount)+'</th></tr>'+(b.items||[]).map(function(it){return '<tr><td>'+__bEsc(it.n)+'</td><td>'+__bFmt(it.amt,u)+'</td></tr>';}).join('')+'</table></div>';});
h+='</body></html>';
const f=document.createElement('iframe');f.style.cssText='position:fixed;right:0;bottom:0;width:0;height:0;border:0';document.body.appendChild(f);
const d=f.contentWindow.document;d.open();d.write(h);d.close();
setTimeout(function(){try{f.contentWindow.focus();f.contentWindow.print();}catch(_){}setTimeout(function(){try{f.remove();}catch(_){}},60000);},500);}
function __budgetPage(u){__bCss();const L=u.L;const old=document.getElementById('bd-pg');if(old)old.remove();
const list=__bLoad();const pg=document.createElement('div');pg.className='bd-pg';pg.id='bd-pg';__bDir(pg,u);
pg.innerHTML='<div class="bd-pg-in"><div class="bd-pg-top"><div class="bd-title" style="margin:0">'+__bEsc(L.myBudgets)+'</div><button class="bd-btn" id="bd-x">'+__bI.x+'</button></div>'
+(list.length?__bK(__bTot(list),u,true)+list.slice().reverse().map(function(b){return '<div class="bd-card"><div class="bd-title">'+__bEsc(b.name)+'</div><div style="font-size:13px;color:var(--bd-mut);margin:-8px 0 12px">'+__bDate(b.ts,u)+'</div>'+__bK(b,u)+__bItems(b,u)+'</div>';}).join('')+'<button class="bd-btn primary" id="bd-pdf">'+__bI.pdf+'PDF</button>':'<div class="bd-card">'+__bEsc(L.noBudget)+'</div>')+'</div>';
document.body.appendChild(pg);
pg.querySelector('#bd-x').onclick=function(){pg.remove();};
const pb=pg.querySelector('#bd-pdf');if(pb)pb.onclick=function(){__budgetPdf(list,u);};}
function __buildBudgetCard(m){__bCss();
const el=document.createElement('div');el.className='bd-card';
const bd=m.budget||{};
function drawForm(){
const u=__bU(bd.ui),L=u.L;__bDir(el,u);
const d=bd.draft=bd.draft||{};d.items=d.items||[0,1,2,3,4,5,6,7].map(function(i){return {n:L['c'+i],on:false,amt:''};});
el.innerHTML='<div class="bd-head"><span class="bd-plus">'+__bI.plus+'</span><span class="bd-htxt">'+__bEsc(L.newBudget)+'</span></div>'
+'<div class="bd-fld"><span class="bd-ic">'+__bI.user+'</span><div class="bd-fb"><label class="bd-lbl">'+__bEsc(L.name)+' <i>*</i></label><input class="bd-in" id="bn" placeholder="'+__bEsc(L.nameHint)+'" value="'+__bEsc(d.name||'')+'"></div></div>'
+'<div class="bd-fld"><span class="bd-ic">'+__bI.rupee+'</span><div class="bd-fb"><label class="bd-lbl">'+__bEsc(L.total)+' ('+__bEsc(u.cur)+') <i>*</i></label><input class="bd-in" id="bt" type="number" inputmode="decimal" placeholder="'+__bEsc(L.totalHint)+'" value="'+__bEsc(d.total||'')+'"></div></div>'
+'<div class="bd-fld" style="margin-bottom:8px"><span class="bd-ic">'+__bI.list+'</span><div class="bd-fb"><label class="bd-lbl" style="margin:10px 0 0">'+__bEsc(L.expTitle)+'</label></div></div>'
+d.items.map(function(it,i){return '<div class="bd-row"><label class="bd-chk"><input type="checkbox" data-i="'+i+'"'+(it.on?' checked':'')+'><span>'+__bEsc(it.n)+'</span></label><input class="bd-in bd-amt" type="number" inputmode="decimal" data-a="'+i+'" placeholder="'+__bEsc(u.cur)+'" value="'+__bEsc(it.amt||'')+'"'+(it.on?'':' disabled')+'></div>';}).join('')
+'<div class="bd-add"><input class="bd-in" id="bc" placeholder="'+__bEsc(L.addOwn)+'"><button class="bd-btn" id="ba">+</button></div>'
+'<div class="bd-sum"><span>'+__bEsc(L.totalSpent)+'</span><b id="bs"></b></div><div class="bd-sum"><span>'+__bEsc(L.saving)+'</span><b id="bv"></b></div>'
+'<div class="bd-err" id="be"></div><button class="bd-btn primary" id="bsub">'+__bI.save+__bEsc(L.submit)+'</button>';
function calc(){const tot=__bNum(d.total);let sp=0;d.items.forEach(function(it){if(it.on)sp+=__bNum(it.amt);});el.querySelector('#bs').textContent=__bFmt(sp,u);const sv=tot-sp;const v=el.querySelector('#bv');v.textContent=__bSv(sv,u);v.className=sv<0?'bd-neg':'';}
el.querySelector('#bn').oninput=function(e){d.name=e.target.value;};
el.querySelector('#bt').oninput=function(e){d.total=e.target.value;calc();};
el.querySelectorAll('input[data-i]').forEach(function(c){c.onchange=function(){const i=+c.dataset.i;d.items[i].on=c.checked;const a=el.querySelector('input[data-a="'+i+'"]');a.disabled=!c.checked;if(c.checked)a.focus();calc();try{saveChats();}catch(_){}};});
el.querySelectorAll('input[data-a]').forEach(function(a){a.oninput=function(){d.items[+a.dataset.a].amt=a.value;calc();};});
el.querySelector('#ba').onclick=function(){const n=el.querySelector('#bc').value.trim();if(!n)return;d.items.push({n:n,on:true,amt:''});drawForm();};
el.querySelector('#bsub').onclick=function(){
const name=String(d.name||'').trim();const tot=__bNum(d.total);const err=el.querySelector('#be');
if(!name){err.textContent=L.needName;return;}
if(!(tot>0)){err.textContent=L.needTotal;return;}
const items=d.items.filter(function(it){return it.on&&__bNum(it.amt)>0;}).map(function(it){return {n:it.n,amt:__bNum(it.amt)};});
const sp=items.reduce(function(a,it){return a+it.amt;},0);
const rec={id:'b'+Date.now(),name:name,total:tot,items:items,spent:sp,saved:tot-sp,ts:Date.now(),ui:bd.ui||null};
const list=__bLoad();list.push(rec);__bSave(list);
m.budget={mode:'saved',id:rec.id,ui:bd.ui||null};try{saveChats();}catch(_){}
el.replaceWith(__buildBudgetCard(m));};
calc();}
function drawSaved(){const b=__bLoad().find(function(x){return x.id===bd.id;});
const u=__bU((b&&b.ui)||bd.ui),L=u.L;__bDir(el,u);
if(!b){el.innerHTML='<div class="bd-title">'+__bEsc(L.notFound)+'</div>';return;}
el.innerHTML='<div class="bd-title">'+__bEsc(b.name)+'</div>'+__bK(b,u)+__bItems(b,u)+'<div class="bd-acts"><button class="bd-btn" id="bp">'+__bI.pdf+'PDF</button><button class="bd-btn" id="bo">'+__bEsc(L.seeAll)+'</button></div>';
el.querySelector('#bp').onclick=function(){__budgetPdf([b],u);};el.querySelector('#bo').onclick=function(){__budgetPage(u);};}
function drawAll(){const list=__bLoad();const u=__bU(bd.ui),L=u.L;__bDir(el,u);
if(!list.length){el.innerHTML='<div class="bd-title">'+__bEsc(L.noBudget)+'</div><button class="bd-btn primary" id="bn2">'+__bEsc(L.createNew)+'</button>';el.querySelector('#bn2').onclick=function(){m.budget={mode:'form',draft:{},ui:bd.ui||null};try{saveChats();}catch(_){}el.replaceWith(__buildBudgetCard(m));};return;}
el.innerHTML='<div class="bd-title">'+__bEsc(L.myBudgets)+'</div>'+__bK(__bTot(list),u,true)+list.slice(-5).reverse().map(function(b){return '<div class="bd-li"><span>'+__bEsc(b.name)+'</span><b class="'+(b.saved<0?'bd-neg':'')+'">'+__bEsc(L.saving)+' '+__bSv(b.saved,u)+'</b></div>';}).join('')+'<div class="bd-acts"><button class="bd-btn" id="bp">'+__bI.pdf+'PDF</button><button class="bd-btn" id="bo">'+__bEsc(L.seeAll)+'</button></div>';
el.querySelector('#bp').onclick=function(){__budgetPdf(list,u);};el.querySelector('#bo').onclick=function(){__budgetPage(u);};}
if(bd.mode==='form')drawForm();else if(bd.mode==='saved')drawSaved();else drawAll();
return el;}
function __bFinish(m,b){m.typing=false;m.processing=null;m.text='';m.budget=b;
try{const c=getCurrentChat();if(c&&c.title==='New chat'){c.title=__bU(b.ui).L.budget;c.__autoTitle=false;}}catch(_){}
try{saveChats();renderMessages();}catch(_){}
try{clearTypingState();updateActionButton();}catch(_){}}
function __bAsync(m,t){
const done=function(d){const ok=d&&d.labels&&typeof d.labels==='object';const ui=ok?{lang:String(d.lang||'en'),cur:String(d.cur||'₹'),labels:d.labels}:{lang:'en',cur:'₹'};__bFinish(m,{mode:(d&&d.intent==='show')?'all':'form',draft:{},ui:ui});};
try{fetch(SAATHI_API_BASE+'/v1/budget-ui',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({text:t})}).then(function(r){return r.ok?r.json():null;}).then(done).catch(function(){done(null);});}catch(_){done(null);}}
function __budgetHandle(m,text){try{
const t=String(text||'').trim();
if(!t||t.length>200||t.indexOf('=== file:')>-1||t.indexOf('```')>-1||t.charAt(0)==='/')return false;
if(/kaise|कैसे|how |what is|क्या होता|मतलब|tips|सलाह/i.test(t))return false;
const list=__bLoad();const low=t.toLowerCase();
for(let i=0;i<list.length;i++){const n=String(list[i].name||'').trim().toLowerCase();if(!n)continue;if(low===n||(__bWordRe.test(t)&&low.indexOf(n)>-1)){__bFinish(m,{mode:'saved',id:list[i].id,ui:list[i].ui||null});return true;}}
if(!__bWordRe.test(t))return false;
const ascii=!/[^\x00-\x7F]/.test(t);
const hing=/bana|बना|batao|बताओ|बताइए|dikha|दिखा|mera|मेरा|dekh|देख|kitna|कितना|bachat|बचत|naya|नया|shuru|शुरू|[\u0900-\u097F]/i.test(t);
const enCue=/\b(create|make|new|set ?up|start|show|my|list|view|report|saved|saving|savings|history|see|check)\b/i.test(t);
if(hing||(ascii&&enCue&&/budget/i.test(t))){
const createRe=/bana|बना|create|make|new|naya|नया|शुरू|shuru|start|setup|set up/i;
const showRe=/batao|बताओ|बताइए|dikha|दिखा|show|mera|मेरा|my|dekh|देख|kitna|कितना|bachat|बचत|saved|saving|savings|report|pdf|list|history|view|see|check/i;
let mode=null;if(createRe.test(t))mode='form';else if(showRe.test(t))mode='all';
if(!mode)return false;
__bFinish(m,{mode:mode,draft:{},ui:hing?null:{lang:'en',cur:'₹'}});return true;}
const other=__bWordRe.test(t.replace(/budget/ig,''));
if(!ascii||other){if(/[?？؟]/.test(t)||t.length>120)return false;__bAsync(m,t);return true;}
return false;}catch(_){return false;}}
"""
if '/*budget3*/' in s:
    print('budget3: pehle se laga hai')
else:
    a = s.find('/*budget*/const __BK')
    b = s.find('function renderMessages(){')
    if a < 0 or b < 0 or b < a or 'function __budgetHandle' not in s[a:b]:
        print('budget3: purana block nahi mila', a, b)
    else:
        s = s[:a] + FN + s[b:]
        open(p, 'w', encoding='utf-8').write(s)
        print('budget3: laga diya')
