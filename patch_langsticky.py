import re
p = "ichat_ai/samajh.py"
s = open(p, encoding="utf-8").read()
if "Default language is English" in s:
    print("pehle se laga hai")
    raise SystemExit
new = '''    "2. Default language is English. If the user has not requested a language in this chat, reply in English, "
    "even if the message is written in Hindi, Hinglish or any other language. "
    "Understand broken text, Roman-script Hindi and voice-to-text mistakes by meaning, never by exact words.\\n"
    "3. Never switch language on your own. Once a language is set (English by default, or the one the user asked for), "
    "keep it in every reply until the user asks for another language. "
    "Never mix two languages in one reply unless the user asks for both or for a translation. "
    "Technical terms (HTML, API, code) may stay as they are.\\n"
'''
pat = r'    "2\. If no language is requested.*?may stay as they are\.\\n"\n'
t, n = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
if n != 1:
    print("match nahi mila, kuch nahi badla")
    raise SystemExit
open(p, "w", encoding="utf-8").write(t)
print("samajh.py badal gaya")
