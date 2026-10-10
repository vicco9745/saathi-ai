with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old = "t = t.replace(/^[\\p{Emoji}\\p{Punct}\\s]+/u, '').trim();"
new = "t = t.replace(/^[\\s\\p{P}\\p{S}]+/gu, '').trim();"

if old in html:
    html = html.replace(old, new)
    print('OK: emoji regex badla')
elif new in html:
    print('SKIP: already fixed')
else:
    # Try alternate form
    old2 = "t = t.replace(/^[\\p{Emoji}\\p{Punct}\\s]+/u, '').trim();"
    new2 = "t = t.replace(/^[\\s!@#$%^&*()_+\\-=\\[\\]{};:'\",.<>?/\\\\|`~]+/, '').trim();"
    if old2 in html:
        html = html.replace(old2, new2)
        print('OK: emoji regex (sada) badla')
    else:
        print('FAIL: nahi mila - manual dekhenge')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
