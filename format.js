(function(){
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function inl(s){return s.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/\*([^*\n]+)\*/g,'<em>$1</em>').replace(/`([^`\n]+)`/g,'<code>$1</code>').replace(/\*/g,'');}
function odd(r){var c=(r.match(/\*\*/g)||[]).length;return c%2?r+'**':r;}
function fmt(t){
var out=[],list=null;
function close(){if(list){out.push('</'+list+'>');list=null;}}
t.split('\n').forEach(function(raw){
raw=odd(raw);
var l=esc(raw),m;
if(/^\s*(-{3,}|\*{3,})\s*$/.test(raw)){close();out.push('<hr class="fmt-hr">');}
else if(/^\s*#{1,6}\s*$/.test(raw)){close();}
else if((m=/^\s*#{1,6}\s+(.*)$/.exec(l))){close();out.push('<div class="fmt-h">'+inl(m[1])+'</div>');}
else if((m=/^\s*&gt;\s?(.*)$/.exec(l))){close();out.push('<div class="fmt-q">'+inl(m[1])+'</div>');}
else if((m=/^\s*[-*\u2022]\s+(.*)$/.exec(l))){if(list!=='ul'){close();out.push('<ul class="fmt-l">');list='ul';}out.push('<li>'+inl(m[1])+'</li>');}
else if((m=/^\s*\d+[.)]\s+(.*)$/.exec(l))){if(list!=='ol'){close();out.push('<ol class="fmt-l">');list='ol';}out.push('<li>'+inl(m[1])+'</li>');}
else if(raw.trim()===''){close();out.push('<div class="fmt-sp"></div>');}
else{close();out.push('<div>'+inl(l)+'</div>');}
});
close();return out.join('');
}
var st=document.createElement('style');
st.textContent='.fmt-h{font-weight:700;font-size:1.1em;margin:12px 0 4px}.fmt-sp{height:8px}.fmt-hr{border:0;border-top:1px solid rgba(128,128,128,.3);margin:10px 0}.fmt-l{margin:4px 0;padding-left:22px}.fmt-q{border-left:3px solid rgba(128,128,128,.4);padding-left:10px;margin:6px 0}.fmt-view{white-space:normal!important}.fmt-view code{background:rgba(128,128,128,.15);padding:1px 5px;border-radius:4px}';
document.head.appendChild(st);
var re=/\*|^\s*#{1,6}(\s|$)|^\s*-{3,}\s*$|^\s*>/m;
function scan(){
var root=document.querySelector('.messages-list')||document.querySelector('.messages');
if(!root)return;
root.querySelectorAll('*').forEach(function(el){
if(el.children.length)return;
if(el.classList.contains('fmt-view'))return;
if(/^(SCRIPT|STYLE|TEXTAREA|INPUT|CODE|PRE|BUTTON|SVG|PATH)$/i.test(el.tagName))return;
var sib=el.nextElementSibling;
if(sib&&!sib.classList.contains('fmt-view'))sib=null;
var t=el.textContent;
if(!sib&&!(t&&re.test(t)))return;
if(!sib){
sib=document.createElement('div');
sib.className=(el.className+' fmt-view').trim();
el.parentNode.insertBefore(sib,el.nextSibling);
el.style.display='none';
}
var h=fmt(t||'');
if(sib.getAttribute('data-h')!==h){sib.innerHTML=h;sib.setAttribute('data-h',h);}
});
}
var wait=false;
new MutationObserver(function(){if(wait)return;wait=true;setTimeout(function(){wait=false;scan();},40);}).observe(document.body,{childList:true,subtree:true,characterData:true});
setTimeout(scan,300);
})();
(function(){var o=window.setTimeout,c=0,last=0;window.setTimeout=function(f,m){if(typeof f==='function'&&f.name==='typeNext'&&m===35){if(++c%10){last=0;f();return last;}last=o(f,16);return last;}return o.apply(window,arguments);};})();
(function(){
function clean(t){return String(t).replace(/^\s*(-{3,}|\*{3,})\s*$/gm,'').replace(/^\s*#{1,6}\s*/gm,'').replace(/^\s*>\s?/gm,'').replace(/^\s*[-*]\s+/gm,'\u2022 ').replace(/\*\*(.+?)\*\*/g,'$1').replace(/\*([^*\n]+)\*/g,'$1').replace(/\*/g,'').replace(/`([^`\n]+)`/g,'$1').replace(/[ \t]+$/gm,'').replace(/\n{3,}/g,'\n\n').trim();}
var bad=/\*|^\s*#{1,6}\s|^\s*-{3,}\s*$|^\s*>/m;
try{if(window.Clipboard&&Clipboard.prototype.writeText){var w=Clipboard.prototype.writeText;Clipboard.prototype.writeText=function(t){return w.call(this,typeof t==='string'&&bad.test(t)?clean(t):t);};}}catch(e){}
document.addEventListener('copy',function(e){
try{var s='',a=document.activeElement;
if(a&&a.value!==undefined&&a.selectionStart!=null&&a.selectionEnd>a.selectionStart)s=a.value.slice(a.selectionStart,a.selectionEnd);
else s=String(window.getSelection());
if(s&&bad.test(s)&&e.clipboardData){e.clipboardData.setData('text/plain',clean(s));e.preventDefault();}}catch(x){}
},true);
})();
(function(){
function sc(t){return String(t).replace(/^\s*(-{3,}|\*{3,})\s*$/gm,' ').replace(/^\s*#{1,6}\s*/gm,'').replace(/^\s*>\s?/gm,'').replace(/^\s*[-*]\s+/gm,'').replace(/\*+/g,'').replace(/#+/g,' ').replace(/`/g,'').replace(/_{2,}/g,' ').replace(/\s{2,}/g,' ').trim();}
try{
var ss=window.speechSynthesis;
if(ss&&ss.speak){
var sp=ss.speak.bind(ss);
ss.speak=function(u){try{if(u&&typeof u.text==='string')u.text=sc(u.text);}catch(e){}return sp(u);};
}
}catch(e){}
})();
(function(){
var snap=[],seen=0;
function grab(){
var a=[];
try{if(typeof pendingAttachments!=='undefined'&&pendingAttachments.length){pendingAttachments.forEach(function(p){if(p&&p.kind==='photo'&&p.dataUrl)a.push({kind:'photo',dataUrl:p.dataUrl,name:p.name||'photo.jpg'});});}}catch(e){}
if(!a.length){try{document.querySelectorAll('#pendingAttachmentsWrap img').forEach(function(im,i){if(/^data:image/.test(im.src))a.push({kind:'photo',dataUrl:im.src,name:'photo'+i+'.jpg'});});}catch(e){}}
return a;
}
setInterval(function(){var a=grab();if(a.length){snap=a;seen=Date.now();}else if(Date.now()-seen>5000){snap=[];}},150);
var of=window.fetch;
window.fetch=function(u,o){
try{if(snap.length&&typeof u==='string'&&/\/v1\/chat$/.test(u.split('?')[0])&&o&&typeof o.body==='string'){var b=JSON.parse(o.body);if(!b.attachments||!b.attachments.length){b.attachments=snap;o=Object.assign({},o,{body:JSON.stringify(b)});}snap=[];seen=0;}}catch(e){}
return of.call(this,u,o);
};
})();
(function(){
var busy={},done={};
function isFileName(t){return /\.(png|jpe?g|webp|gif|heic)$/i.test(String(t||'').trim());}
function photoOf(c){
var ms=(c&&c.messages)||[];
for(var i=0;i<ms.length;i++){
var at=ms[i].attachments||[];
for(var j=0;j<at.length;j++){if(at[j]&&at[j].kind==='photo'&&at[j].dataUrl&&String(at[j].dataUrl).indexOf('data:image')===0)return at[j].dataUrl;}
}
return null;
}
function tick(){
try{
if(typeof chats==='undefined'||!Array.isArray(chats)||typeof SAATHI_API_BASE==='undefined'||typeof SAATHI_KEY==='undefined')return;
var key=localStorage.getItem(typeof SAATHI_KEY_STORE!=='undefined'?SAATHI_KEY_STORE:'')||'';
chats.forEach(function(c){
if(!c||!c.id||busy[c.id]||done[c.id]||!isFileName(c.title))return;
var img=photoOf(c);if(!img)return;
busy[c.id]=true;
fetch(SAATHI_API_BASE+'/v1/title',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({message:'',image:img})})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){
busy[c.id]=false;done[c.id]=true;
var t=d&&d.title?String(d.title).trim():'';
if(t&&t!=='Photo message'&&!isFileName(t)){c.title=t;try{saveChats();}catch(e){}try{renderChatList();}catch(e){}}
})
.catch(function(){busy[c.id]=false;done[c.id]=true;});
});
}catch(e){}
}
setInterval(tick,2000);
})();
(function(){
var last='';
function say(m){if(m!==last){last=m;try{console.log('[title] '+m);}catch(e){}}}
window.__titleDebug=function(){
var r={};
try{r.chats=(typeof chats!=='undefined')?chats.length:'undefined';}catch(e){r.chats='err';}
try{r.api=(typeof SAATHI_API_BASE!=='undefined')?'ok':'undefined';}catch(e){r.api='err';}
try{r.key=(typeof SAATHI_KEY!=='undefined'&&SAATHI_KEY)?'ok':'missing';}catch(e){r.key='err';}
try{r.fileTitles=chats.filter(function(c){return /\.(png|jpe?g|webp|gif|heic)$/i.test(String(c.title||''));}).length;}catch(e){r.fileTitles='err';}
try{r.withPhoto=chats.filter(function(c){return (c.messages||[]).some(function(m){return (m.attachments||[]).some(function(a){return a&&a.kind==='photo'&&a.dataUrl;});});}).length;}catch(e){r.withPhoto='err';}
alert(JSON.stringify(r));
};
})();
(function(){
var busy={},done={};
function isFile(t){return /\.(png|jpe?g|webp|gif|heic)$/i.test(String(t||'').trim());}
function photoOf(c){var ms=(c&&c.messages)||[];for(var i=0;i<ms.length;i++){var at=ms[i].attachments||[];for(var j=0;j<at.length;j++){if(at[j]&&at[j].kind==='photo'&&at[j].dataUrl&&String(at[j].dataUrl).indexOf('data:image')===0)return at[j].dataUrl;}}return null;}
function tick(){
try{
var S=window.__sc;if(!S)return;
var chats=S.chats(),key=S.key(),api=S.api();
if(!Array.isArray(chats)||!key||!api)return;
chats.forEach(function(c){
if(!c||!c.id||busy[c.id]||done[c.id]||!isFile(c.title))return;
var img=photoOf(c);if(!img)return;
busy[c.id]=true;
fetch(api+'/v1/title',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':key},body:JSON.stringify({message:'',image:img})})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){busy[c.id]=false;done[c.id]=true;var t=d&&d.title?String(d.title).trim():'';if(t&&t!=='Photo message'&&!isFile(t)){c.title=t;try{S.save();}catch(e){}try{S.render();}catch(e){}}})
.catch(function(){busy[c.id]=false;});
});
}catch(e){}
}
setInterval(tick,2000);
window.__titleDebug=function(){
var r={};
try{var S=window.__sc;r.khidki=S?'ok':'missing';var ch=S?S.chats():[];r.chats=ch.length;r.key=S&&S.key()?'ok':'missing';r.fileTitles=ch.filter(function(c){return isFile(c.title);}).length;r.withPhoto=ch.filter(function(c){return !!photoOf(c);}).length;}catch(e){r.err=String(e.message);}
alert(JSON.stringify(r));
};
})();
(function(){
var PH='Naam ban raha hai…';
var busy={},done={};
function isFile(t){return /\.(png|jpe?g|webp|gif|heic)$/i.test(String(t||'').trim());}
function needs(t){return isFile(t)||String(t||'')===PH;}
function photoOf(c){var ms=(c&&c.messages)||[];for(var i=0;i<ms.length;i++){var at=ms[i].attachments||[];for(var j=0;j<at.length;j++){if(at[j]&&at[j].kind==='photo'&&at[j].dataUrl&&String(at[j].dataUrl).indexOf('data:image')===0)return at[j].dataUrl;}}return null;}
function tick(){
try{
var S=window.__sc;if(!S)return;
var chats=S.chats();if(!Array.isArray(chats))return;
var key=S.key(),api=S.api();
chats.forEach(function(c){
if(!c||!c.id||done[c.id]||!needs(c.title))return;
var img=photoOf(c);if(!img)return;
function setT(t){c.title=t;try{S.save();}catch(e){}try{S.render();}catch(e){}}
if(c.title!==PH)setT(PH);
if(busy[c.id]||!key||!api)return;
busy[c.id]=true;
fetch(api+'/v1/title',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':key},body:JSON.stringify({message:'',image:img})})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){busy[c.id]=false;done[c.id]=true;var t=d&&d.title?String(d.title).trim():'';if(!t||t==='Photo message'||isFile(t))t='Photo chat';setT(t);})
.catch(function(){busy[c.id]=false;done[c.id]=true;setT('Photo chat');});
});
}catch(e){}
}
setInterval(tick,300);
})();
