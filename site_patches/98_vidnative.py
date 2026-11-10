import re

# ---------- 1) format.js: frames ke asli naam + video bhejna ----------
f = "format.js"
t = open(f, encoding="utf-8").read()
old = "try{if(typeof pendingAttachments!=='undefined'&&pendingAttachments.length){pendingAttachments.forEach(function(p){if(p&&p.kind==='photo'&&p.dataUrl)a.push({kind:'photo',dataUrl:p.dataUrl,name:p.name||'photo.jpg'});});}}catch(e){}"
new = "try{var PA=(window.__vidApi&&window.__vidApi.get())||(typeof pendingAttachments!=='undefined'?pendingAttachments:null);if(PA&&PA.length){PA.forEach(function(p){if(p&&p.kind==='photo'&&p.dataUrl)a.push({kind:'photo',dataUrl:p.dataUrl,name:p.name||'photo.jpg'});if(p&&p.kind==='video'&&p.dataUrl&&p.dataUrl.length<9000000)a.push({kind:'video',dataUrl:p.dataUrl,name:p.name||'video.mp4'});});}}catch(e){}"
changed = False
if "window.__vidApi.get())||(typeof" in t:
    print("vidnative: format.js pehle se laga hai")
elif t.count(old) == 1:
    open(f, "w", encoding="utf-8").write(t.replace(old, new))
    changed = True
    print("vidnative: format.js badal di")
else:
    print("vidnative: format.js ki line nahi mili", t.count(old))

if changed:
    h = open("index.html", encoding="utf-8").read()
    def bump(m):
        n = int(m.group(3)) + 1 if m.group(3) else 1
        return m.group(1) + "format.js?v=" + str(n) + m.group(4)
    h2, c = re.subn(r"""(src=["'][^"']*)format\.js(\?v=(\d+))?(["'])""", bump, h, count=1)
    if c == 1:
        open("index.html", "w", encoding="utf-8").write(h2)
        print("vidnative: index.html mein format.js ka version badhaya")
    else:
        print("vidnative: format.js ka tag nahi mila, version nahi badla")

# ---------- 2) server: asli video ko video-model ko bhejna ----------
p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDNATIVE" in s:
    print("vidnative: server pehle se laga hai")
else:
    helper = r'''# VIDNATIVE helpers
_OR_VID_CACHE = {"t": 0, "m": []}
def _or_video_models():
    import time, requests
    if _OR_VID_CACHE["m"] and time.time() - _OR_VID_CACHE["t"] < 3600:
        return list(_OR_VID_CACHE["m"])
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=15)
        out = []
        for m in r.json().get("data", []):
            ins = (m.get("architecture") or {}).get("input_modalities") or []
            pr = m.get("pricing") or {}
            if "video" in ins and str(pr.get("prompt")) in ("0", "0.0") and str(pr.get("completion")) in ("0", "0.0"):
                out.append((m.get("context_length") or 0, m.get("id")))
        out.sort(reverse=True)
        ids = [i for _, i in out if i][:3]
        if ids:
            _OR_VID_CACHE["t"] = time.time()
            _OR_VID_CACHE["m"] = ids
        return ids
    except Exception:
        return []

def _call_video_native(prompt, video):
    import re, requests
    key = os.environ.get("OPENROUTER_API_KEY")
    url = getattr(video, "dataUrl", "") or ""
    if not key or not url.startswith("data:video"):
        return ""
    text = VIDEO_RULES + "\n\nUSER KA SAWAAL: " + (prompt or "Is video mein kya ho raha hai, poori detail se batao.")
    content = [{"type": "text", "text": text}, {"type": "video_url", "video_url": {"url": url}}]
    for model in _or_video_models()[:2]:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "HTTP-Referer": "https://saathi-ai-y48j.onrender.com", "X-Title": "Saathi AI"},
                json={"model": model, "messages": [{"role": "system", "content": VIDEO_SYSTEM}, {"role": "user", "content": content}], "max_tokens": 2000},
                timeout=70,
            )
            if r.status_code != 200:
                continue
            ch = r.json().get("choices") or []
            if ch:
                txt = (ch[0].get("message", {}).get("content") or "").strip()
                txt = re.sub(r"[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]+", "", txt)
                if txt:
                    return txt
        except Exception:
            continue
    return ""

'''
    a = "def _call_vision_v2("
    o2 = "    if images:\n        raw = _call_vision_v2(body.message, images)"
    n2 = '''    videos = [a for a in (body.attachments or []) if a.kind == "video" and a.dataUrl]
    if videos:  # VIDNATIVE
        try:
            _nv = _call_video_native(body.message, videos[0])
        except Exception:
            _nv = ""
        if _nv:
            return {"service": "chat", "reply": _nv, "model": "saathi-video"}

''' + o2
    if s.count(a) == 1 and s.count(o2) == 1:
        s = s.replace(a, helper + a).replace(o2, n2)
        open(p, "w", encoding="utf-8").write(s)
        print("vidnative: server patch lag gaya")
    else:
        print("vidnative: server lines nahi mili", s.count(a), s.count(o2))
