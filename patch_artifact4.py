p = 'app/main.py'
s = open(p, encoding='utf-8').read()
old = 'polished modern look with a coherent colour palette;'
new = 'polished modern look that uses ONLY these CSS variables for every colour: var(--s-bg) page background, var(--s-panel) cards, var(--s-text) text, var(--s-soft) secondary text, var(--s-accent) main colour for buttons, headings and highlights, var(--s-accent-soft) light tint, var(--s-border) borders; do not invent other colours unless the user asks for specific colours or the thing needs them (map, chart legend);'
if 'var(--s-accent)' in s:
    print('artifact4: pehle se laga hai')
elif s.count(old) != 1:
    print('artifact4: jagah nahi mili', s.count(old))
else:
    s = s.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('artifact4: laga diya')
