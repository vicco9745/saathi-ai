j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
if "__vidPA" in t:
    print("vidpa: pehle se hai")
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
    print("vidpa: saathi_video.js badal di")
for f in ["index.html", "site_patches/98_video.py"]:
    s = open(f, encoding="utf-8").read()
    if "saathi_video.js?v=3" in s:
        open(f, "w", encoding="utf-8").write(s.replace("saathi_video.js?v=3", "saathi_video.js?v=4"))
        print(f + ": v=4 kar diya")
    else:
        print(f + ": v=3 nahi mila, chhoda")
