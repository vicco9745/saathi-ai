(function(){
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function inl(s){return s.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/`([^`\n]+)`/g,'<code>$1</code>');}
function fmt(t){
var out=[],list=null;
function close(){if(list){out.push('</'+list+'>');list=null;}}
t.split('\n').forEach(function(raw){
var l=esc(raw),m;
if(/^\s*(-{3,}|\*{3,})\s*$/.test(raw)){close();out.push('<hr class="fmt-hr">');}
else if((m=/^\s*#{1,6}\s+(.*)$/.exec(l))){close();out.push('<div class="fmt-h">'+inl(m[1])+'</div>');}
else if((m=/^\s*[-*\u2022]\s+(.*)$/.exec(l))){if(list!=='ul'){close();out.push('<ul class="fmt-l">');list='ul';}out.push('<li>'+inl(m[1])+'</li>');}
else if((m=/^\s*\d+[.)]\s+(.*)$/.exec(l))){if(list!=='ol'){close();out.push('<ol class="fmt-l">');list='ol';}out.push('<li>'+inl(m[1])+'</li>');}
else if(raw.trim()===''){close();out.push('<div class="fmt-sp"></div>');}
else{close();out.push('<div>'+inl(l)+'</div>');}
});
close();return out.join('');
}
var st=document.createElement('style');
st.textContent='.fmt-h{font-weight:700;font-size:1.1em;margin:12px 0 4px}.fmt-sp{height:8px}.fmt-hr{border:0;border-top:1px solid rgba(128,128,128,.3);margin:10px 0}.fmt-l{margin:4px 0;padding-left:22px}.fmt-done{white-space:normal!important}.fmt-done code{background:rgba(128,128,128,.15);padding:1px 5px;border-radius:4px}';
document.head.appendChild(st);
var re=/\*\*|^\s*#{1,6}\s|^\s*(-{3,}|\*{3,})\s*$/m;
function scan(){
var root=document.querySelector('.messages-list')||document.querySelector('.messages');
if(!root)return;
root.querySelectorAll('*').forEach(function(el){
if(el.children.length||el.classList.contains('fmt-done'))return;
if(/^(SCRIPT|STYLE|TEXTAREA|INPUT|CODE|PRE)$/.test(el.tagName))return;
var t=el.textContent;
if(t&&re.test(t)){el.innerHTML=fmt(t);el.classList.add('fmt-done');}
});
}
var timer=null;
new MutationObserver(function(){clearTimeout(timer);timer=setTimeout(scan,400);}).observe(document.body,{childList:true,subtree:true,characterData:true});
setTimeout(scan,800);
})();
