p = 'app/main.py'
s = open(p, encoding='utf-8').read()
if 'VISION_RULES' in s:
    print('pehle se laga hua hai')
else:
    text = '''Photo ko bahut dhyaan se padho. Niyam:
- Photo mein jo likha hai, har naam, pata, phone number, form number, tareekh (din, mahina, saal), reference number aur ID bilkul waise hi likho jaise dikh rahe hain. Andaza mat lagao, vartani mat badlo.
- Jo saaf nahi padha jaata, wahan likho: saaf nahi dikh raha.
- Phone ki screen ke hisse (status bar, battery, buttons, page number jaise 3/3, menu) dastavez ka hissa nahi hain. Unhe ignore karo.
- Dastavez adhoora ya kata hua sirf tab kaho jab photo mein saaf kata hua dikhe.
- Apni taraf se koi baat mat jodo.'''
    rules = 'VISION_RULES = """' + text + '"""\n\n'
    old = '    content = [{"type": "text", "text": prompt or "Is photo me kya hai? Puri detail batao."}]'
    new = '    content = [{"type": "text", "text": VISION_RULES + "\\n\\nUSER KA SAWAAL: " + (prompt or "Is photo me kya hai? Puri detail batao.")}]'
    d = s.find('def _call_vision_v2')
    a = s.find('def _polish_vision_reply')
    e = s.find('    user_prompt = (', a)
    i = s.find(old, d)
    if d == -1 or a == -1 or e == -1 or i == -1 or not (e < d < i):
        print('jagah nahi mili', d, a, e, i)
    else:
        add = ('    system += (\n'
               '        "\\n\\nRaw observation mein agar phone ki screen ke hisse (page number jaise 3/3, buttons) "\n'
               '        "ya dastavez adhoora dikhne ki baat ho, use jawab mein mat likho. "\n'
               '        "Raw text mein jo naam, number, saal likha hai use mat badlo aur use typo ya anuman mat kaho. "\n'
               '        "Barcode ko dastavez asli hone ka saboot mat batao."\n'
               '    )\n\n')
        s = s[:i] + new + s[i + len(old):]
        s = s[:d] + rules + s[d:]
        s = s[:e] + add + s[e:]
        open(p, 'w', encoding='utf-8').write(s)
        print('done')
