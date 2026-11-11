p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "VIDEOCAP" in s:
    print("videocap: pehle se laga hai")
    raise SystemExit
anchor = "VISION_SYSTEM_INSTRUCTION = ("
add = '''# VIDEOCAP
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTION + " Saathi video bhi padh sakta hai: jab user video bhejta hai, to uske frames dekhe jaate hain aur aawaaz likhi jaati hai. Agar user poochhe 'kya tum video dekh sakte ho', to kaho haan aur video bhejne ko kaho. Kabhi mat kaho ki tum video nahi dekh sakte. Agar user pehle bheje gaye video ke baare mein poochhe aur uske frames tumhare paas nahi hain, to kaho ki video dobara bhejein."

'''
if s.count(anchor) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(anchor, add + anchor))
    print("videocap: patch lag gaya")
else:
    print("videocap: line nahi mili, kuch nahi badla", s.count(anchor))
