p = 'app/main.py'
s = open(p, encoding='utf-8').read()
R = [
(r'''exactly 3 scenes, har scene 2 se 4 chhote vakya.''',
 r'''exactly 3 scenes, har scene 4 se 6 poore vakya, rang-bhara vistaar ke saath (jagah, mahaul, baatcheet, paatron ki harkatein).'''),
(r'''1-2 chhote vakya jo bataye ki kahani kis baare mein hai aur teen drishyon mein taiyaar hai;''',
 r'''4 se 5 achhe vakya jo bataye ki kahani kis baare mein hai, kaun se paatra hain, kaisa mahaul hai aur kis tarah ki kahani hai (hasya, rahasya, saahas aadi); ant ya nichod mat batao;'''),
]
if 'poore vakya, rang-bhara' in s:
    print('story4 server: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story4 server: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story4 server: laga diya')
