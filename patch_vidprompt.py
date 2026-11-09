p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDEO_RULES" in s:
    print("vidprompt: pehle se laga hai")
    raise SystemExit
rules = '''VIDEO_RULES = """VIDEO MODE (upar ke photo/document wale rules aur 3-hisse wale format ko is video ke liye IGNORE karo):
Neeche di gayi tasveerein EK hi video ke frames hain, kram mein. Inhe photo mat samjho aur 'photo', 'frame' ya 'image' shabd use mat karo; sab kuch 'video mein' ke roop mein batao.
Jawab Hinglish mein, saaf aur seedha, in hisson mein:
1. Video mein kya ho raha hai: shuru se ant tak scene-by-scene kahani, kaun-kaun dikh raha hai (kapde, jagah, kaam), woh kya kar raha hai.
2. Jo bol ya likha hua dikhe (subtitles ya text), use video ki baat-cheet ki tarah likho aur batao ki woh kya keh raha hai.
3. Video ka matlab aur sandesh: yeh kis baare mein hai, ismein se kya seekh milti hai, aur agar baat kamyabi ya tarakki ki hai to kamyab hone ke liye video kya sikhata hai.
Spelling ya grammar ki galtiyan mat nikalo. Chehre se kisi asli insaan ki pehchaan ya naam mat batao; sirf wahi batao jo dikhta hai ya likha hai. Jo saaf na dikhe use andaaza kehkar batao, banao mat."""

'''
a = "def _call_vision_v2("
old = '    text_prompt = VISION_RULES + "\\n\\nUSER KA SAWAAL: " + (prompt or default_prompt)'
new = '''    if is_video:
        text_prompt = VISION_RULES + "\\n\\n" + VIDEO_RULES + "\\n\\nUSER KA SAWAAL: " + (prompt or default_prompt)
    else:
        text_prompt = VISION_RULES + "\\n\\nUSER KA SAWAAL: " + (prompt or default_prompt)'''
if s.count(a) == 1 and s.count(old) == 1:
    s = s.replace(a, rules + a).replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
    print("vidprompt: patch lag gaya")
else:
    print("vidprompt: lines nahi mili, kuch nahi badla", s.count(a), s.count(old))
