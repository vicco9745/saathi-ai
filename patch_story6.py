p = 'app/main.py'
s = open(p, encoding='utf-8').read()
R = [
(r'''_STORY_WORD = _re_story.compile(r"(kahani|kahaani|कहानी|story|stories)", _re_story.I)''',
 r'''_STORY_WORD = _re_story.compile(r"(\bkahani|\bkahaani|कहानी|कथा|कहाणी|गोष्ट|\bstory|\bstories|\bcuento|\bhistoria|\bhistória|\bhistoire|\bconte\b|\bgeschichte|\bmärchen|\bracconto|\bcerita|\bkisah|\bhikaye|\bkathai|\bgalpo|கதை|গল্প|కథ|કથા|ਕਹਾਣੀ|物語|故事|이야기|قصة|کہانی|\bрассказ|\bистория|\bсказка)", _re_story.I)'''),
(r'''    if not (_STORY_WORD.search(t) and _STORY_VERB.search(t)):''',
 r'''    if not _STORY_WORD.search(t):'''),
(r'''ya sachchi ghatna ke baare mein hai, to sirf:''',
 r'''ya sachchi ghatna ke baare mein hai, ya user asal mein kahani nahi maang raha (jaise Instagram story, news story, kahani ka matlab ya kahani ke baare mein sawaal), to sirf:'''),
(r'''koi emoji nahi."''',
 r'''koi emoji nahi. "
    "Do aur keys bhi do, scenes ke bahar: \"lang\" (kahani ki bhasha ka BCP-47 code, jaise hi-IN, en-US, ta-IN, bn-IN) aur \"ui\" object jisme usi bhasha mein ye chhote label hon: "
    "\"story\" (kahani shabd), \"read\" (padhne ka samay, jaise '{n} min read', {n} jagah zaroor rakho), \"scene\" (drishya shabd), "
    "\"listen\", \"again\", \"copy\", \"share\" (button ke naam, ek-ek shabd)."'''),
(r'''return {"note": str(d.get("note", "")).strip(), "title": title,''',
 r'''return {"lang": str(d.get("lang", "")).strip(), "ui": (d.get("ui") if isinstance(d.get("ui"), dict) else {}), "note": str(d.get("note", "")).strip(), "title": title,'''),
]
if '"ui": (d.get("ui")' in s:
    print('story6 server: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('story6 server: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('story6 server: laga diya')
