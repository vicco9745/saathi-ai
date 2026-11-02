p = 'app/main.py'
s = open(p, encoding='utf-8').read()
if 'Hisse 2 mein sirf' in s:
    print('pehle se laga hua hai')
else:
    old1 = '        reply = _polish_vision_reply(raw, body.message)'
    new1 = ('        raw = __import__("re").sub(r"[\\u3000-\\u303f\\u3400-\\u9fff\\uff00-\\uffef]+", "", raw)\n'
            '        reply = __import__("re").sub(r"[\\u3000-\\u303f\\u3400-\\u9fff\\uff00-\\uffef]+", "", _polish_vision_reply(raw, body.message))')
    old2 = '- Apni taraf se koi baat mat jodo."""'
    new2 = ('- Sirf Hindi (Devanagari), English ya Roman Hindi mein likho. Chinese, Japanese ya Korean akshar kabhi mat likho.\n'
            '- Phone number ya tareekh ke aage ka bindu ya colon (jaise TEL. NO.:) label ka hissa hai, number ka nahi. Pura number likho jaisa dikh raha hai.\n'
            '- Address ki line ka ek shabd do hisson mein mat todo (jaise LAMAHI ek hi shabd hai).\n'
            '- Apni taraf se koi baat mat jodo."""')
    if s.count(old1) != 1 or s.count(old2) != 1:
        print('jagah nahi mili', s.count(old1), s.count(old2))
    else:
        s = s.replace(old1, new1).replace(old2, new2)
        a = s.find('def _polish_vision_reply')
        e = s.find('    user_prompt = (', a)
        if a == -1 or e == -1:
            print('polish jagah nahi mili', a, e)
        else:
            add = ('    system += (\n'
                   '        "\\n\\nHisse 2 mein sirf wahi galat ya adhoora likho jo dastavez mein saaf dikhta hai, jaise kata, dhundhla ya mita hua. "\n'
                   '        "Agar raw text mein koi shabd ya number tumhe unclear lage, use dastavez ki galti mat kaho; use jaisa hai waisa hi likho. "\n'
                   '        "Date ke format, barcode ya dikhne ke dhang par tippani mat karo. Sirf Hindi, English ya Roman Hindi mein likho, koi Chinese akshar nahi. "\n'
                   '        "Phone number mein bindu ya colon label ka hissa hai, number ka nahi; number ko adhoora mat kaho."\n'
                   '    )\n\n')
            s = s[:e] + add + s[e:]
            open(p, 'w', encoding='utf-8').write(s)
            print('done')
