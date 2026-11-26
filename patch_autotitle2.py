p = 'app/main.py'
s = open(p, encoding='utf-8').read()
old = '"4 to 8 words, specific and descriptive about the topic or task, not a generic label. "'
new = '"About 25 characters long (between 20 and 28), 3 to 5 words, specific and descriptive about the topic or task, not a generic label. For Chinese, Japanese or Korean use 8 to 14 characters. "'
if 'About 25 characters long' in s:
    print('autotitle2 server: pehle se laga hai')
elif s.count(old) != 1:
    print('autotitle2 server: jagah nahi mili', s.count(old))
else:
    s = s.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('autotitle2 server: laga diya')
