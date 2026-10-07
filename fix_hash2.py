path = 'app/main.py'
with open(path) as f:
    c = f.read()

old = '"6. Headings ke liye ## use karo. Lists ke liye - ya 1. use karo.\\n"'
new = '"6. Headings ke liye DEFAULT mein **bold** aur emoji use karo (jaise **📄 File Type**). ## ya ### sirf tab use karo jab user saaf bole. Lists ke liye - ya 1. use karo.\\n"'

if old in c:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print("OK - main.py updated")
else:
    print("FAIL")

# Check ai_providers.py
path2 = 'ichat_ai/ai_providers.py'
with open(path2) as f:
    c2 = f.read()

if 'headings' in c2.lower() or 'Headings' in c2:
    print("ai_providers has heading rule")
else:
    print("ai_providers - no heading rule (ok)")
