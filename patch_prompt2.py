p = 'app/main.py'
s = open(p, encoding='utf-8').read()
pairs = [
(r'''"Teen hisse, har ek ka chhota saaf heading:\n"''',
 r'''"Teen hisse, har ek ka chhota saaf heading (heading bhi usi bhasha mein jisme jawab likh rahe ho):\n"'''),
(r'''"1. Photo mein kya likha hai: jo cheez hai usi ke baare mein, mukhya baatein points mein.\n"''',
 r'''"1. Photo mein kya likha hai: mukhya baatein points mein. Photo mein jo bhi naam, pata, phone number, form number, tareekh, reference number aur ID hai, ek bhi mat chhodo.\n"'''),
(r'''"2. Kya sahi hai aur kya galat ya adhoora: dono alag-alag batao, kaaran ke saath. Agar kuch galat nahi dikha to saaf likho ki kuch galat nahi dikha.\n"''',
 r'''"2. Kya sahi hai aur kya galat ya adhoora: yeh us dastavez ke baare mein batao jo photo mein hai (kya theek lagta hai, kya adhoora ya shak wala hai). Apne hi jawab ke shabdon ki vartani par tippani mat karo aur bina aadhaar galtiyan mat nikalo. Agar kuch galat nahi dikha to saaf likho. Yeh pakka mat kaho ki dastavez asli hai; sirf itna kaho ki jaanch aadhikarik jagah par karni chahiye.\n"'''),
]
bad = [o[:40] for o, n in pairs if s.count(o) != 1]
if bad:
    print('jagah nahi mili:', bad)
else:
    for o, n in pairs:
        s = s.replace(o, n)
    open(p, 'w', encoding='utf-8').write(s)
    print('done')
