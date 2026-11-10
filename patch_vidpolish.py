p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDPOLISH" in s:
    print("vidpolish: pehle se laga hai")
else:
    old = "_polish_vision_reply(raw, body.message)"
    new = '(raw if any("video-frame" in (getattr(a, "name", "") or "") for a in images) else _polish_vision_reply(raw, body.message))  # VIDPOLISH'
    if s.count(old) == 1:
        open(p, "w", encoding="utf-8").write(s.replace(old, new))
        print("vidpolish: patch lag gaya")
    else:
        print("vidpolish: line nahi mili, kuch nahi badla", s.count(old))
