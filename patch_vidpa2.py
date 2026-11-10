j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
if "__vidPA" in t:
    print("vidpa2: pehle se hai")
else:
    t = t.replace("typeof renderPendingAttachments === 'function'", "true")
    t = t.replace("typeof tryFlushSend === 'function'", "true")
    t = t.replace("renderPendingAttachments()", "window.__vidRender()")
    t = t.replace("tryFlushSend()", "window.__vidFlush()")
    t = t.replace("pendingAttachments", "window.__vidPA()")
    helper = (
        "window.__vidPA=function(){try{if(window.__vidApi)return window.__vidApi.get();if(typeof pendingAttachments!=='undefined')return pendingAttachments;}catch(e){}return undefined;};\n"
        "window.__vidRender=function(){try{if(window.__vidApi)window.__vidApi.render();}catch(e){}};\n"
        "window.__vidFlush=function(){try{if(window.__vidApi)window.__vidApi.flush();}catch(e){}};\n"
    )
    open(j, "w", encoding="utf-8").write(helper + t)
    print("vidpa2: saathi_video.js badal di")
for f in ["index.html", "site_patches/98_video.py"]:
    s = open(f, encoding="utf-8").read()
    if "saathi_video.js?v=5" in s:
        open(f, "w", encoding="utf-8").write(s.replace("saathi_video.js?v=5", "saathi_video.js?v=6"))
        print(f + ": v=6 kar diya")
    else:
        print(f + ": v=5 nahi mila, chhoda")
