import re
p = 'app/main.py'
s = open(p, encoding='utf-8').read()
ml = open('app/pdf_multilang.py', encoding='utf-8').read()
ok = ('def _generate_chart_png' in ml) or re.search(r'from\s+\S+\s+import[^\n]*_generate_chart_png', ml)
OLD = '''        "Allowed tags only: h1, h2, h3, p, ul, li, blockquote, table with tr, th and td, and <pagebreak/>. "
'''
NEW = r'''        "Allowed tags only: h1, h2, h3, p, ul, li, blockquote, table with tr, th and td, <pagebreak/>, <box text='...'/> and <chart .../>. "
        "BOX: <box text='one short key point or summary'/> for a highlighted key point; the text must not contain apostrophes or the > character. "
        "CHARTS: only when the user supplied real numbers or asked for a chart of numbers they gave. Never make up data points. "
        "Write the data attribute in SINGLE quotes with valid JSON inside, exactly like these: "
        "<chart type='bar' title='Monthly sales' data='[{\"label\":\"Jan\",\"value\":120},{\"label\":\"Feb\",\"value\":150}]'/> ; "
        "<chart type='line' title='Equity curve' data='[{\"x\":1,\"y\":100},{\"x\":2,\"y\":110}]'/> ; "
        "<chart type='candlestick' title='Price' data='[{\"time\":\"Mon\",\"open\":10,\"high\":12,\"low\":9,\"close\":11}]'/>. "
        "The chart title must not contain apostrophes or the > character. "
'''
if "<chart type='bar'" in s:
    print('pdf2: pehle se laga hai')
elif not ok:
    print('pdf2: chart function pdf_multilang.py tak nahi pahunchta, kuch nahi badla')
elif s.count(OLD) != 1:
    print('pdf2: jagah nahi mili', s.count(OLD))
else:
    s = s.replace(OLD, NEW, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('pdf2: laga diya')
