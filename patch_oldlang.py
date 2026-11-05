p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
old = "User ki bhaasha aur samajh ke star ke anusaar jawab do — Hindi mein sawaal to saral Hindi mein, Hinglish mein sawaal to Hinglish mein."
new = "Jawab ki bhasha sirf neeche diye LANGUAGE PRIORITY niyam se tay hogi (nayi chat me English, user ke kehne par hi badlegi); samajh ke star ke anusaar saral bhasha me jawab do."
if s.count(old) != 1:
    print("match nahi mila, kuch nahi badla")
    raise SystemExit
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("ai_providers.py badal gaya")
