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
