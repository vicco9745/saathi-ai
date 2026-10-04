path = 'app/main.py'
with open(path) as f:
    c = f.read()

old = '"11. Koi button dead nahi — har click pe action."'

new = '''"11. Koi button dead nahi — har click pe action.\\n"
                "\\n📋 CHANGES / क्या किया (code ke neeche likho):\\n"
                "- [Kya-kya banaya/badla — list mein]\\n"
                "\\n✅ FEATURES ADD KIYE:\\n"
                "- [Naye features]\\n"
                "\\n📝 Aap check kariye:\\n"
                "Koi galti ho, kuch aur chahiye, ya samajh na aaye to bataaiye — "
                "main turant theek kar dunga."'''

count = c.count(old)
if count > 0:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print(f"OK - {count} jagah fix ho gaya")
else:
    print("FAIL - Block nahi mila")
