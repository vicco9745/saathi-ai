# Fix 1: app/main.py
path = 'app/main.py'
with open(path) as f:
    c = f.read()

old = '10. Headings ke liye ### ya ## use MAT karo. Sirf **bold** use karo aur emoji lagao. Jaise: "**📄 File Type**" ya "**📋 Kya-Kya Hai**". Hash symbols (#) bilkul mat likho.'

new = '10. Headings ke liye DEFAULT mein sirf **bold** aur emoji use karo. Jaise: "**📄 File Type**" ya "**📋 Kya-Kya Hai**". Hash symbols (##, ###) TABHI use karo jab user SAFA bole "markdown headings use karo" ya "### use karo". Warna kabhi mat likho.'

if old in c:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print("OK - main.py")
else:
    print("FAIL - main.py")

# Fix 2: ichat_ai/ai_providers.py
path2 = 'ichat_ai/ai_providers.py'
with open(path2) as f:
    c2 = f.read()

old2 = 'headings bhi Hindi mein aur **bold** mein: **📄 फाइल का प्रकार**, **📋 क्या-क्या है**, **✅ अच्छी बातें**, **⚠️ कमियाँ**, **🔧 सुधार**, **🌟 रेटिंग**. Hash (#) symbols kabhi mat use karo.'

new2 = 'headings bhi Hindi mein aur **bold** mein: **📄 फाइल का प्रकार**, **📋 क्या-क्या है**, **✅ अच्छी बातें**, **⚠️ कमियाँ**, **🔧 सुधार**, **🌟 रेटिंग**. Hash symbols (##, ###) sirf tab use karo jab user saaf bole "markdown headings do". Warna default **bold** hi use karo.'

if old2 in c2:
    c2 = c2.replace(old2, new2)
    with open(path2, 'w') as f:
        f.write(c2)
    print("OK - ai_providers.py")
else:
    print("FAIL - ai_providers.py")
