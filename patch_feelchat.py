p = "ichat_ai/response_engine.py"
s = open(p, encoding="utf-8").read()
if "_is_feel_chat" in s:
    print("already patched")
else:
    helper = '''
_FEEL_WORDS = ("udaas", "dukhi", "dukh ho", "dukh hai", "rona", "ro raha", "ro rahi", "pareshan", "akela", "akeli", "gussa", "khush", "thaka", "thaki", "haha", "hehe", "lol", "sad", "lonely", "upset", "angry", "happy", "tired", "depressed", "उदास", "दुखी", "दुख", "रो रहा", "रो रही", "परेशान", "अकेला", "अकेली", "गुस्सा", "खुश", "थक", "हाहा")
_FACT_WORDS = ("news", "khabar", "price", "rate", "score", "weather", "mausam", "scam", "fraud", "legit", "genuine", ".com", "search", "dhundho", "khojo", "who is", "kaun hai", "खबर", "मौसम", "दाम", "भाव", "स्कोर", "स्कैम", "ठगी", "ढूँढो", "ढूंढो", "खोजो")

def _is_feel_chat(q):
    q = q.lower()
    return any(w in q for w in _FEEL_WORDS) and not any(w in q for w in _FACT_WORDS)


'''
    a = "def get_response(user_text, history=None, lang_pref=None):"
    b = "if any(k in _q for k in _FRESH) or any(k in _q for k in _CHK) or _story_real(_q):"
    assert a in s and b in s, "match nahi mila"
    s = s.replace(a, helper + a, 1)
    s = s.replace(b, "if (not _is_feel_chat(_q) and (any(k in _q for k in _FRESH) or any(k in _q for k in _CHK))) or _story_real(_q):", 1)
    open(p, "w", encoding="utf-8").write(s)
    print("response_engine patched")

q = "ichat_ai/insaan.py"
t = open(q, encoding="utf-8").read()
old = r'''"Do not repeat the same reaction again and again.\n"'''
new = r'''"Do not repeat the same reaction again and again. "
    "LAUGHTER: When the user laughs or jokes ('haha', 'hehe', 'lol', a funny remark), laugh along naturally ('haha', 'arre yaar, ye to mast tha') and add a light joke or reaction of your own, the way a friend does. Do not search or explain a joke, just enjoy it with them.\n"'''
if "LAUGHTER" in t:
    print("insaan already patched")
else:
    assert old in t, "insaan match nahi mila"
    open(q, "w", encoding="utf-8").write(t.replace(old, new, 1))
    print("insaan patched")
