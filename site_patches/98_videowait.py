# video ke frame taiyaar hone tak send rokta hai

# 1) index.html: attBusy ko video ka intezaar sikhana
p = "index.html"
s = open(p, encoding="utf-8").read()
old = "function attBusy(){return uploadLoading>0||pendingAttachments.some(a=>a.loadUntil&&a.loadUntil>Date.now());}"
new = "function attBusy(){return uploadLoading>0||pendingAttachments.some(a=>(a.loadUntil&&a.loadUntil>Date.now())||a.__vidBusy);}"
if "__vidBusy" in s:
    print("videowait: index.html mein pehle se hai")
elif s.count(old) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
    print("videowait: attBusy badal diya")
else:
    print("videowait: attBusy wali line nahi mili, index.html nahi badla")

# 2) saathi_video.js: frame nikalte waqt flag lagana, kaam khatam hone par hatana
j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
if "__vidBusy" in t:
    print("videowait: saathi_video.js mein pehle se hai")
else:
    a1 = "done.add(a);"
    a2 = "}).catch(function () { say('Video padhne me gadbad hui'); });"
    if t.count(a1) == 1 and t.count(a2) == 1:
        t = t.replace(a1, "done.add(a); a.__vidBusy = true;")
        t = t.replace(a2, "}).catch(function () { say('Video padhne me gadbad hui'); }).then(function () { a.__vidBusy = false; try { if (typeof tryFlushSend === 'function') tryFlushSend(); } catch (e) {} });")
        open(j, "w", encoding="utf-8").write(t)
        print("videowait: saathi_video.js badal di")
    else:
        print("videowait: saathi_video.js ki lines nahi mili, kuch nahi badla")
