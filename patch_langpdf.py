p = 'app/main.py'
s = open(p, encoding='utf-8').read()
R = [
    ('"or (b) an IMAGE / picture / photo / drawing / illustration. "',
     '"(b) an IMAGE / picture / photo / drawing / illustration, or (c) a PDF / document / report / letter file. "'),
    ('"Questions about websites or images, or anything else, are NONE. "',
     '"Questions about websites, images or PDFs, or anything else, are NONE. "'),
    ('"Reply with exactly one line and nothing else: \'website\' or "',
     '"Reply with exactly one line and nothing else: \'website\' or \'pdf\' or "'),
    ('            if out.startswith("website"):\n                return "website"\n',
     '            if out.startswith("website"):\n                return "website"\n            if out.startswith("pdf"):\n                return "pdf"\n'),
]
if 'out.startswith("pdf")' in s:
    print('langpdf: pehle se laga hai')
elif all(s.count(a) == 1 for a, b in R):
    for a, b in R:
        s = s.replace(a, b, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('langpdf: laga diya')
else:
    print('langpdf: jagah nahi mili', [s.count(a) for a, b in R])
