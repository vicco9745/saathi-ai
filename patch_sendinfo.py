import re
f = "format.js"
t = open(f, encoding="utf-8").read()
old = "b.attachments=snap;"
new = r"""b.attachments=snap;try{var __k={};snap.forEach(function(x){var n=(x.kind||'?')+(/^video-frame/.test(x.name||'')?'(frame)':'');__k[n]=(__k[n]||0)+1;});var __d=document.createElement('div');__d.id='sendInfo';__d.textContent='Bhej raha hoon: '+Object.keys(__k).map(function(n){return n+' x'+__k[n];}).join(', ');__d.style.cssText='position:fixed;top:70px;left:50%;transform:translateX(-50%);z-index:99999;padding:6px 12px;border-radius:14px;font:600 12px/1.2 sans-serif;color:#fff;background:#2563eb;max-width:90%;text-align:center;';document.body.appendChild(__d);setTimeout(function(){try{__d.remove();}catch(e){}},25000);}catch(e){}"""
if "sendInfo" in t:
    print("sendinfo: pehle se laga hai")
elif t.count(old) == 1:
    open(f, "w", encoding="utf-8").write(t.replace(old, new))
    print("sendinfo: format.js badal di")
    h = open("index.html", encoding="utf-8").read()
    def bump(m):
        n = int(m.group(3)) + 1 if m.group(3) else 1
        return m.group(1) + "format.js?v=" + str(n) + m.group(4)
    h2, c = re.subn(r"""(src=["'][^"']*)format\.js(\?v=(\d+))?(["'])""", bump, h, count=1)
    if c == 1:
        open("index.html", "w", encoding="utf-8").write(h2)
        print("sendinfo: format.js ka version badhaya")
    else:
        print("sendinfo: format.js ka tag nahi mila")
else:
    print("sendinfo: line nahi mili", t.count(old))
