p = 'app/main.py'
s = open(p, encoding='utf-8').read()
a = s.find('def _polish_vision_reply')
e = s.find('    user_prompt = (', a)
tag = 'Aaj ki tareekh:'
if a == -1 or e == -1:
    print('jagah nahi mili', a, e)
elif tag in s[a:e + 400]:
    print('pehle se laga hua hai')
else:
    add = ('    system += ("\\n\\nAaj ki tareekh: " + __import__("datetime").date.today().strftime("%d %B %Y") + ". "\n'
           '        "Isse pehle ki tareekh beet chuki hai; use bhavishya ki, sample ya typo mat kaho. "\n'
           '        "Tareekh mein mahina aur saal poora likho. Aise shabd mat likho jinka matlab pakka na ho; seedhi aam bhasha mein likho.")\n\n')
    open(p, 'w', encoding='utf-8').write(s[:e] + add + s[e:])
    print('done')
