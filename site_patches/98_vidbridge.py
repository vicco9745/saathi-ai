p = "index.html"
s = open(p, encoding="utf-8").read()
if "__vidApi" in s:
    print("vidbridge: pehle se hai")
else:
    old = "let pendingAttachments=[];"
    new = old + "window.__vidApi={get:function(){return pendingAttachments;},render:function(){renderPendingAttachments();updateActionButton();},flush:function(){tryFlushSend();}};"
    if s.count(old) == 1:
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
        print("vidbridge: bridge laga diya")
    else:
        print("vidbridge: line nahi mili", s.count(old))
