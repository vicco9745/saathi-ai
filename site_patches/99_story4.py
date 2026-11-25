p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""/*story-anim*/function __buildStoryCard2(m,row){
const el=__buildStoryCard(m);row.appendChild(el);
const sg=function(t){try{return Array.from(new Intl.Segmenter('hi',{granularity:'grapheme'}).segment(t),function(x){return x.segment;});}catch(_){return Array.from(t);}};
const titleEl=el.querySelector('.story-title');
const sceneEls=Array.from(el.querySelectorAll('.st-scene'));
const acts=el.querySelector('.story-actions');
let nb=null;if(m.text){nb=document.createElement('div');nb.className='bubble';row.appendChild(nb);}
const parts=[];let off=0;
function add(node,txt,wrap){const g=sg(txt);parts.push({node:node,g:g,off:off,wrap:wrap,k:-1,shown:null});off+=g.length;}
add(titleEl,titleEl.textContent,[]);
sceneEls.forEach(function(sc){const p=sc.querySelector('p');const dv=sc.previousElementSibling;const w=[sc];if(dv&&dv.classList.contains('st-div'))w.unshift(dv);add(p,p.textContent,w);});
if(nb)add(nb,String(m.text),[nb]);
const total=off;
const noteOff=nb?parts[parts.length-1].off:total;
let live=false;
function render(c){
parts.forEach(function(pt){
const k=Math.max(0,Math.min(pt.g.length,c-pt.off));
if(k!==pt.k){pt.k=k;pt.node.textContent=k?pt.g.slice(0,k).join(''):'';}
const vis=pt.wrap.length===0||c>pt.off;
if(vis!==pt.shown){pt.shown=vis;pt.wrap.forEach(function(w){w.style.display=vis?'':'none';});
if(vis&&live&&pt.wrap.length){try{pt.wrap[pt.wrap.length-1].scrollIntoView({block:'nearest',behavior:'smooth'});}catch(_){}}}
});
acts.style.display=c>=noteOff?'':'none';}
function fin(){if(nb)nb.innerHTML=linkifyText(String(m.text));}
let c=(typeof m.__sc==='number'&&!m.__sdone)?m.__sc:total;
render(c);
if(c>=total){fin();}else{
window.__stTm=window.__stTm||new Map();
const old=window.__stTm.get(m);if(old)clearInterval(old);
live=true;
const id=setInterval(function(){
if(!el.isConnected){clearInterval(id);return;}
c=Math.min(total,c+3);m.__sc=c;render(c);
if(c>=total){clearInterval(id);m.__sdone=true;fin();try{saveChats();}catch(_){}}
},28);
window.__stTm.set(m,id);}
return el;}
"""
a1 = 'function renderMessages(){'
R = [
(r"""row.appendChild(__buildStoryCard(m));if(m.text){const _sb=document.createElement('div');_sb.className='bubble';_sb.innerHTML=linkifyText(m.text);row.appendChild(_sb);}""",
 r"""__buildStoryCard2(m,row);"""),
(r"""m.story=d.story;""", r"""m.story=d.story;m.__sc=0;"""),
]
if '/*story-anim*/' in s:
    print('story4: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad or s.count(a1) != 1:
        print('story4: jagah nahi mili', bad, s.count(a1))
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        s = s.replace(a1, FN + a1, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story4: laga diya')
