p = "app/main.py"
s = open(p, encoding="utf-8").read()
if '"language": "hi"' in s:
    print("audiohi: pehle se laga hai")
    raise SystemExit
o1 = 'data={"model": model, "response_format": "json", "temperature": "0"},'
n1 = 'data={"model": model, "response_format": "json", "temperature": "0", "language": "hi"},'
o2 = "Ise 'Jo likha ya bola dikha' hisse mein bola hua maan kar use karo."
n2 = "Ise 'Jo likha ya bola dikha' hisse mein bola hua maan kar use karo, par 'transcript' shabd mat likho aur use shabd-ba-shabd copy mat karo; agar woh bekaar ya angrezi anuvaad jaisa lage to ignore karo."
if s.count(o1) == 1 and s.count(o2) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(o1, n1).replace(o2, n2))
    print("audiohi: patch lag gaya")
else:
    print("audiohi: lines nahi mili, kuch nahi badla", s.count(o1), s.count(o2))
