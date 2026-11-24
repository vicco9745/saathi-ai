p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
if "_casual" in s:
    print("already patched")
else:
    i = s.index("def _call_groq(")
    j = s.index("def _call_openrouter(")
    seg = s[i:j]
    a = '        payload = {\n            "model": GROQ_MODEL,\n'
    assert seg.count(a) == 1, "payload anchor nahi mila"
    assert seg.count('"max_tokens": 3000,') == 1, "max_tokens nahi mila"
    block = r'''        _TASKW = ("likh", "kahani", "story", "article", "blog", "script", "code", "program", "banao", "bana do", "search", "news", "khabar", "samjhao", "explain", "translate", "anuvad", "kya hai", "kaun", "kitna", "scam", "legit", "लिख", "कहानी", "लेख", "बनाओ", "समझाओ", "खबर", "ख़बर", "अनुवाद", "क्या है", "कौन", "कितना", "पैसे")
        _casual = len(prompt) <= 120 and "Question:" not in prompt and not any(w in prompt.lower() for w in _TASKW)
        if _casual:
            try:
                from ichat_ai.insaan import CHAT_FIRST as _CF
                _sys_content = (
                    "Tum Saathi ho, Vikas ne tumhe banaya hai. Khud ko sirf Saathi bolna aur apna asli model kabhi mat batana. "
                    "Agar koi sachchi se pooche ki tum insaan ho ya AI, to kindly sach batao ki tum AI ho. "
                    "Agar user Hindi ya Hinglish mein likhe to jawab hamesha Hindi (Devanagari) mein do; sirf English mein likhe to English mein.\n\n"
                ) + _CF
            except Exception:
                _casual = False
'''
    seg = seg.replace(a, block + a, 1).replace('"max_tokens": 3000,', '"max_tokens": (400 if _casual else 3000),', 1)
    open(p, "w", encoding="utf-8").write(s[:i] + seg + s[j:])
    print("compact patched")
