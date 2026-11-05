import urllib.request as U
p = 'app/pdf_multilang.py'
lines = open(p, encoding='utf-8').read().split('\n')
CAND = {
    'korean': ('https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/nanumgothic/NanumGothic-Regular.ttf', 'NanumGothic-Regular.ttf'),
    'japanese': ('https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/mplus1p/MPLUS1p-Regular.ttf', 'MPLUS1p-Regular.ttf'),
    'chinese': ('https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf', 'NotoSansSC.ttf'),
}
def ok(u):
    try:
        r = U.urlopen(U.Request(u, method='HEAD'), timeout=25)
        return r.status == 200
    except Exception as e:
        print('  check fail:', e)
        return False
changed = False
for i, l in enumerate(lines):
    for k, (u, f) in CAND.items():
        if l.strip().startswith("'" + k + "':"):
            if '.ttf' in l:
                print(k + ': pehle se ttf hai')
            elif ok(u):
                lines[i] = "        '" + k + "': (\"" + u + "\", \"" + f + "\"),"
                changed = True
                print(k + ': ttf font laga diya')
            else:
                print(k + ': URL nahi chala, purana rakha')
if changed:
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))
