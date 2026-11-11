p = "ichat_ai/response_engine.py"
s = open(p, encoding="utf-8").read()
if "VIDEOQ" in s:
    print("videoq: pehle se laga hai")
    raise SystemExit
anchor = "    if _matches_any(normalized_original, _CREATOR_PATTERNS):\n"
add = '''    # VIDEOQ: kya tum video dekh sakte ho
    import re as _vre
    if _vre.search(r"(video|वीडियो).{0,25}(dekh|देख|padh|पढ़|samajh|समझ|sun|सुन|support|kar sakt|कर सक)|(dekh|देख|padh|पढ़|samajh|समझ|sun|सुन).{0,25}(video|वीडियो)", original_text.lower()) and len(original_text) < 80:
        reply = ("हाँ, मैं वीडियो पढ़ सकता हूँ। वीडियो भेजिए: कुछ न लिखें तो मैं उसमें बोले गए शब्द बताऊँगा, और 'video dekh kar batao' लिखें तो जो दिख रहा है वह बताऊँगा।" if _lang == "hi"
                 else "Yes, I can read videos. Send one: with no text I will tell you the words spoken in it, and write 'video dekh kar batao' and I will tell you what is visible.")
        add_conversation(original_text, reply)
        return reply

'''
if s.count(anchor) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(anchor, add + anchor))
    print("videoq: patch lag gaya")
else:
    print("videoq: line nahi mili, kuch nahi badla", s.count(anchor))
