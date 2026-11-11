p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "SPEECHDEFAULT" in s:
    print("speech: pehle se laga hai")
    raise SystemExit
anchor = '        print("VIDEO: transcript chars =", len(_tr))\n'
block = anchor + r'''        # SPEECHDEFAULT: jab tak user dekhne ko na kahe, sirf bola hua shabd batao
        import re as _re2
        _SEE = _re2.compile(r"dekh|dikh|kya\s*-?\s*kya|kya\s+ho\s+raha|kya\s+hai|scene|describe|visual|kaun|kapde|vistar|detail|poori|\bsee\b|\blook\b|what.?s in|show")
        if not _SEE.search((body.message or "").lower()):
            if _tr:
                return {"service": "chat", "reply": "**Video mein bola gaya:**\n\n" + _tr, "model": "saathi-audio"}
            return {"service": "chat", "reply": "Is video mein mujhe bola hua kuch sunai nahi diya. Agar chahte hain ki main video dekh kar bataun, to 'video dekh kar batao' likh kar bhejiye.", "model": "saathi-audio"}
'''
if s.count(anchor) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(anchor, block))
    print("speech: patch lag gaya")
else:
    print("speech: line nahi mili, kuch nahi badla", s.count(anchor))
