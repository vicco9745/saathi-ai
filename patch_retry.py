p = "ichat_ai/response_engine.py"
s = open(p, encoding="utf-8").read()
if "ai_provider_answer retry" in s:
    print("pehle se laga hai")
    raise SystemExit
old = '        print(f"[get_response] ai_provider_answer CRASHED: {type(e).__name__}: {e}")\n        ai_answer = None\n'
new = old + '''
    if not ai_answer:
        try:
            import time as _t
            _t.sleep(3)
            print("[get_response] ai_provider_answer retry")
            ai_answer = ai_provider_answer(original_text, history=history, lang_pref=lang_pref)
        except Exception as e:
            print(f"[get_response] retry failed: {type(e).__name__}: {e}")
            ai_answer = None
'''
if s.count(old) != 1:
    print("match nahi mila, kuch nahi badla:", s.count(old))
    raise SystemExit
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("response_engine.py badal gaya")
