import re
p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
ok1 = False
if "VIDEOCAP2" in s:
    print("videocap3: ai_providers pehle se laga hai")
    ok1 = True
elif re.search(r"^SYSTEM_INSTRUCTION = \(", s, re.M):
    add = '''

# VIDEOCAP2
SYSTEM_INSTRUCTION += (
    " Saathi video bhi padh sakta hai: jab user video bhejta hai to uske frames dekhe jaate hain aur aawaaz likhi jaati hai. "
    "Agar user poochhe ki kya tum video dekh sakte ho, to apne shabdon mein haan kaho aur video bhejne ko kaho. "
    "Kabhi mat kaho ki tum video nahi dekh sakte. Agar user kisi pehle bheje video ke baare mein poochhe aur uske frames tumhare paas nahi hain, to kaho ki video dobara bhejein."
)
'''
    open(p, "w", encoding="utf-8").write(s.rstrip("\n") + add)
    print("videocap3: asli nirdesh mein jod diya")
    ok1 = True
else:
    print("videocap3: SYSTEM_INSTRUCTION nahi mila, kuch nahi badla")

q = "ichat_ai/response_engine.py"
t = open(q, encoding="utf-8").read()
if ok1 and "# VIDEOQ:" in t:
    a = t.index("    # VIDEOQ:")
    b = t.index("    if _matches_any(normalized_original, _CREATOR_PATTERNS):", a)
    open(q, "w", encoding="utf-8").write(t[:a] + t[b:])
    print("videocap3: chipka hua jawab hata diya")
elif "# VIDEOQ:" not in t:
    print("videocap3: chipka hua jawab pehle se nahi hai")
else:
    print("videocap3: chipka hua jawab rehne diya")
