# Fix 1: app/main.py timeouts
path = 'app/main.py'
with open(path) as f:
    c = f.read()

c = c.replace('timeout=90,', 'timeout=300,')
c = c.replace('timeout=180,', 'timeout=300,')

# Shorten analysis system prompt
old = '''            "Tum ek professional code reviewer ho. User ne ek file/code bheja hai. "
            "Uska POORA detail mein analysis karo aur ye format follow karo:\\n\\n"
            "## 📄 File Ka Naam aur Type\\n"
            "[HTML/CSS/JS/Python kya hai]\\n\\n"
            "## 📋 Isme Kya-Kya Hai\\n"
            "- Sections (header, hero, services, waghairah)\\n"
            "- Features (buttons, forms, animations)\\n"
            "- Design (colors, fonts, layout)\\n"
            "- Images aur unke sources\\n\\n"
            "## ✅ Achhi Baatein\\n"
            "[Kya sahi hai]\\n\\n"
            "## ⚠️ Kamiyan (Missing Things)\\n"
            "[Kya missing hai — jo honi chahiye thi]\\n\\n"
            "## 🔧 Kya-Kya Improve Kar Sakte Hain\\n"
            "[Suggestions list]\\n\\n"
            "## 🌟 Quality Rating: X/10\\n"
            "[Kyun ye rating di]\\n\\n"
            "Aakhir mein: 'Bataaiye kya-kya theek karwana hai — main turant kar dunga.'\\n\\n"
            "User ki bhasha mein jawab do (Hindi/English/Hinglish)."'''

new = '''            "Tum ek professional code reviewer ho. User ne file bheji hai. "
            "CHHOTA aur SAARBHUT analysis do (max 200 words):\\n\\n"
            "## 📄 File Type\\n"
            "[HTML/CSS/JS/Python]\\n\\n"
            "## 📋 Kya-Kya Hai\\n"
            "- [4-6 main points]\\n\\n"
            "## ✅ Achhi Baatein\\n"
            "- [3-4 points]\\n\\n"
            "## ⚠️ Kamiyan\\n"
            "- [3-4 points]\\n\\n"
            "## 🔧 Improvements\\n"
            "- [3-4 suggestions]\\n\\n"
            "## 🌟 Rating: X/10\\n\\n"
            "Chhota rakho. User ki bhasha mein."'''

if old in c:
    c = c.replace(old, new)
    print("✅ Analysis prompt shortened")
else:
    print("⚠️ Analysis prompt not found")

with open(path, 'w') as f:
    f.write(c)
print("✅ Timeouts fixed")

# Fix 2: index.html - limit file content size
path2 = 'index.html'
with open(path2, encoding='utf-8') as f:
    c2 = f.read()

old2 = "msgToSend=(text?text+'\\n\\n':'')+'Ye file check karo aur poori detail mein batao kya-kya hai, kya improve karna hai:\\n\\n=== File: '+fileWithContent.name+' ===\\n'+fileWithContent.content;"

new2 = "msgToSend=(text?text+'\\n\\n':'')+'Ye file check karo:\\n\\n=== File: '+fileWithContent.name+' ===\\n'+fileWithContent.content.slice(0,20000);"

if old2 in c2:
    c2 = c2.replace(old2, new2)
    with open(path2, 'w', encoding='utf-8') as f:
        f.write(c2)
    print("✅ File size limited to 20000 chars")
else:
    print("⚠️ File size limit not applied")
