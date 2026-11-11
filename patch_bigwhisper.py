p = "app/main.py"
s = open(p, encoding="utf-8").read()
old = 'for model in ("whisper-large-v3-turbo", "whisper-large-v3"):'
new = 'for model in ("whisper-large-v3", "whisper-large-v3-turbo"):'
if new in s:
    print("bigwhisper: pehle se laga hai")
elif s.count(old) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
    print("bigwhisper: patch lag gaya")
else:
    print("bigwhisper: line nahi mili, kuch nahi badla", s.count(old))
