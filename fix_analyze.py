path = 'app/main.py'
with open(path) as f:
    c = f.read()

# Detect function me analyze action jodo
old = '''def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()'''

new = '''def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # Analyze: agar code/file hai aur 'batao/check/analyze/dekho' bhi hai
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo'])
    if has_code and (has_analyze or len(m) > 500):
        return "analyze"'''

if old in c:
    c = c.replace(old, new)
    print("✅ Detect function updated")
else:
    print("❌ Detect function nahi mila")

# Add analyze handler in chat endpoint
old2 = '''    # Auto-detect: kya user PDF/website/image banana chahta hai?
    action = _detect_action(body.message)'''

new2 = '''    # Auto-detect: kya user PDF/website/image banana chahta hai?
    action = _detect_action(body.message)

    if action == "analyze":
        system = (
            "Tum ek professional code reviewer ho. User ne ek file/code bheja hai. "
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
            "User ki bhasha mein jawab do (Hindi/English/Hinglish)."
        )
        try:
            reply = _call_groq(body.message, system=system)
            return {"service": "chat", "reply": reply, "model": "saathi", "kind": "analysis"}
        except Exception as e:
            return {"service": "chat", "reply": f"Analysis mein problem: {e}", "model": "saathi"}'''

if old2 in c:
    c = c.replace(old2, new2)
    print("✅ Analyze handler added")
else:
    print("❌ Chat endpoint nahi mila")

with open(path, 'w') as f:
    f.write(c)
print("✅ Saved")
