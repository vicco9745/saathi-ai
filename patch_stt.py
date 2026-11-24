p = "app/main.py"
s = open(p, encoding="utf-8").read()
a = '        data["language"] = lg\n    for model in ("whisper-large-v3-turbo", "whisper-large-v3"):'
assert s.count(a) == 1, "stt match nahi mila"
b = ('        data["language"] = lg\n'
     '    if lg == "hi":\n'
     '        data["prompt"] = "यह दो दोस्तों की हिंदी बातचीत है। अरे यार, क्या हुआ? हाँ जी, अच्छा अच्छा। मन उदास है, आज दिन अच्छा गया। साथी, मुझे बताओ।"\n'
     '    for model in ("whisper-large-v3-turbo", "whisper-large-v3"):')
open(p, "w", encoding="utf-8").write(s.replace(a, b, 1))
print("patched")
