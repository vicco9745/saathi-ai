import os
SP='app/main.py'
HP='index.html'
sv=open(SP,encoding='utf-8').read()
ht=open(HP,encoding='utf-8').read()

SERVER=r'''class PreviewRequest(BaseModel):
    url: str

_PREV_CACHE = {}

def _host_ok(host):
    import socket, ipaddress
    try:
        infos = socket.getaddrinfo(host, None)
    except Exception:
        return False
    for inf in infos:
        try:
            ip = ipaddress.ip_address(inf[4][0])
        except Exception:
            return False
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            return False
    return True

@app.post("/v1/preview")
def preview(body: PreviewRequest, key=Depends(require_api_key)):
    import re, requests
    from urllib.parse import urlparse, urljoin
    url = (body.url or "").strip()
    if url in _PREV_CACHE:
        return {"image": _PREV_CACHE[url]}
    img = ""
    try:
        cur = url
        for _ in range(4):
            pu = urlparse(cur)
            if pu.scheme not in ("http", "https") or not pu.hostname or not _host_ok(pu.hostname):
                raise ValueError("blocked")
            r = requests.get(cur, headers={"User-Agent": "Mozilla/5.0 (compatible; SaathiBot/1.0)", "Accept": "text/html"}, timeout=4, stream=True, allow_redirects=False)
            if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("Location"):
                cur = urljoin(cur, r.headers["Location"])
                r.close()
                continue
            if r.status_code != 200 or "html" not in (r.headers.get("Content-Type") or "").lower():
                r.close()
                break
            raw = b""
            for chunk in r.iter_content(8192):
                raw += chunk
                if len(raw) > 250000:
                    break
            r.close()
            html = raw.decode("utf-8", "ignore")
            m = (re.search(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
                 or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\'](?:og:image|twitter:image)["\']', html, re.I))
            if m:
                img = urljoin(cur, m.group(1).replace("&amp;", "&"))
                if not img.lower().startswith(("http://", "https://")):
                    img = ""
            break
    except Exception as e:
        print("PREVIEW error", repr(e)[:120])
    if img:
        if len(_PREV_CACHE) > 500:
            _PREV_CACHE.clear()
        _PREV_CACHE[url] = img
    return {"image": img}

'''

BLOCK=r"""/*callfocus*/function __cvEnrich(list){
  var KEY=localStorage.getItem('saathi_api_key');if(!KEY)return;
  var tok=window.__cvSrcTok=(window.__cvSrcTok||0)+1;
  list.slice(0,6).forEach(function(s,idx){
    if(s.image||s.thumbnail)return;
    fetch(SAATHI_API_BASE+'/v1/preview',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({url:s.url})})
    .then(function(r){return r.ok?r.json():null;})
    .then(function(d){
      if(!d||!d.image||tok!==window.__cvSrcTok)return;
      var a=document.querySelectorAll('#callSrcCard .cvs-item')[idx];
      if(!a||a.querySelector('.cvs-th'))return;
      var tm=document.createElement('img');tm.className='cvs-th';tm.alt='';tm.referrerPolicy='no-referrer';
      tm.onerror=function(){tm.style.display='none';};tm.src=d.image;a.appendChild(tm);
    }).catch(function(){});
  });
}
function __cvFocus(i,text){
  try{
    var row=document.querySelector('#callSrcCard .cvs-row');if(!row)return;
    var items=row.querySelectorAll('.cvs-item');if(!items.length)return;
    var low=String(text||'').toLowerCase(),best=-1,sc=0;
    for(var k=0;k<items.length;k++){
      var words=String((items[k].querySelector('.cvs-title')||{}).textContent||'').toLowerCase().split(/[^a-z0-9\u0900-\u097f]+/),n=0;
      words.forEach(function(w){if(w.length>3&&low.indexOf(w)>-1)n++;});
      if(n>sc){sc=n;best=k;}
    }
    if(best<0)best=i%items.length;
    for(var j=0;j<items.length;j++)items[j].classList.toggle('act',j===best);
    row.scrollTo({left:items[best].offsetLeft-row.offsetLeft,behavior:'smooth'});
  }catch(_){}
}
"""

EDITS=[
 ("function startCall(){callActive=true;callMuted=false;",
  BLOCK+"function startCall(){callActive=true;callMuted=false;"),
 ("c.style.top=top+'px';c.classList.add('on');",
  "c.style.top=top+'px';c.classList.add('on');__cvEnrich(list);"),
 ("var a=new Audio(URL.createObjectURL(b));__cvAudio=a;window.__saathiAudio=a;",
  "__cvFocus(i,parts[i]);var a=new Audio(URL.createObjectURL(b));__cvAudio=a;window.__saathiAudio=a;"),
 ("out.length<12){if(s.length<=260){out.push(s);break;}",
  "out.length<16){if(s.length<=200){out.push(s);break;}"),
 ("head=s.slice(0,260)","head=s.slice(0,200)"),
 ("if(cut<80)cut=s.lastIndexOf(' ',260);if(cut<1)cut=260;",
  "if(cut<60)cut=s.lastIndexOf(' ',200);if(cut<1)cut=200;"),
 (".cvs-th{width:78px;height:60px;object-fit:cover;border-radius:10px;flex-shrink:0}",
  ".cvs-th{width:104px;height:88px;object-fit:cover;border-radius:14px;flex-shrink:0}\n.cvs-item{transition:box-shadow .3s}\n.cvs-item.act{box-shadow:0 0 0 2px rgba(91,100,230,.4)}"),
]

if '/*callsrc*/' not in ht:
    print('callfocus: pehle 49_callsrc laga hona chahiye')
elif '/*callfocus*/' in ht and '/v1/preview' in sv:
    print('callfocus: pehle se laga hai')
else:
    bad=[]
    if sv.count('@app.post("/v1/tts")')!=1: bad.append('server /v1/tts')
    if '/v1/preview' in sv: bad.append('server pehle se /v1/preview hai')
    for a,_ in EDITS:
        if ht.count(a)!=1: bad.append(a[:45])
    if bad:
        print('callfocus: jagah nahi mili ->',bad)
    else:
        sv=sv.replace('@app.post("/v1/tts")',SERVER+'@app.post("/v1/tts")',1)
        for a,b in EDITS: ht=ht.replace(a,b,1)
        open(SP,'w',encoding='utf-8').write(sv)
        open(HP,'w',encoding='utf-8').write(ht)
        print('callfocus laga diya')
