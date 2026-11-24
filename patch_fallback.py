p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
if "_ut = user_text" in s:
    print("already patched")
else:
    i = s.index("def ai_provider_answer(")
    j = s.index("# ABILITIES", i)
    seg = s[i:j]
    loop = "    for name, fn in _PROVIDERS:\n"
    assert seg.count(loop) == 1, "loop match nahi mila"
    add = ("    for name, fn in _PROVIDERS:\n"
           "        _ut = user_text\n"
           "        if name != \"groq\" and lang_pref and str(lang_pref).strip().lower() == \"hi\":\n"
           "            _ut = \"(Jawab sirf Hindi mein, Devanagari lipi mein do, chhota aur dost jaisa.)\\n\" + user_text\n")
    seg = seg.replace(loop, add, 1).replace("fn(user_text)", "fn(_ut)")
    open(p, "w", encoding="utf-8").write(s[:i] + seg + s[j:])
    print("fallback patched")
