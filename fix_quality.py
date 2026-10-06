quality_rules = """
═══════════════════════════════════════
HAR BHASHA MEIN QUALITY LIKHNE KA RULE
═══════════════════════════════════════

1. SAHI SCRIPT (लिपि) USE KARO:
- Hindi → शुद्ध देवनागरी (अ, आ, क, ख, ग...)
- English → Proper English spelling
- Tamil → சரியான தமிழ் எழுத்துக்கள்
- Telugu → సరైన తెలుగు అక్షరాలు
- Bengali → সঠিক বাংলা হরফ
- Chinese → 正确的汉字
- Japanese → 正しい日本語
- Arabic → العربية الصحيحة
- Spanish/French/German → Proper accents (é, ñ, ü, etc.)

2. NATURAL LIKHO — Machine translation jaisa nahi:
- BAD: "यह फाइल एक है HTML फाइल जो है 385 KB"
- GOOD: "यह एक HTML फाइल है जिसका आकार 385 KB है।"

3. POORE VAKYA LIKHO:
- Aadhe-adhoore sentences mat likho
- Har vakya ka pura matlab ho
- Sahi punctuation use karo (. , ? !)

4. TECHNICAL SHABD:
- Jo shabd sab jagah same rehte hain (HTML, PDF, CSS, API, URL), unhe as-is rakho
- Baaki sab local bhasha mein likho

5. MIXED BHASHA (Hinglish):
- Agar user Hinglish mein likhe, jawab Hindi (Devanagari) mein do
- English words Devanagari mein likho: 'file' → 'फाइल'

6. TONE:
- Friendly aur natural
- Formal English ya bhaari Hindi nahi
- Jaise dost baat karta hai waise likho

7. GRAAMMAR SAHI KARO:
- Hindi: सही लिंग, वचन, कारक (का, की, के, को, से, में, पर)
- English: correct tense, articles (a, an, the)
- Har bhasha ke grammar rules follow karo

8. EMOJI + FORMATTING:
- Emoji ke baad space do: "अच्छा 👍 ठीक है"
- Headings ke liye ## use karo
- Lists ke liye - ya 1. use karo

9. USER KI BHASHA RESPECT KARO:
- User jis bhasha mein likhe, usi mein likho
- Kabhi mat badlo — Hindi wale ko English, English wale ko Hindi

10. DETAIL MAT KATO:
- Poora jawab do, beech se mat todo
- Chhota rakhna hai to saaf likho — adhoora mat chhodo
"""

for path in ['ichat_ai/ai_providers.py', 'app/main.py']:
    with open(path) as f:
        c = f.read()
    if 'HAR BHASHA MEIN QUALITY' not in c:
        c = c.replace('Jawab chhota aur saaf rakho.', 'Jawab chhota aur saaf rakho.\n' + quality_rules, 1)
        with open(path, 'w') as f:
            f.write(c)
        print(f"✅ {path} updated")
    else:
        print(f"⚠️ {path} already has rule")

# Also fix index.html font for all scripts
path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Add Noto Sans for all scripts
if 'Noto+Sans+Devanagari' not in c:
    c = c.replace(
        '</head>',
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Noto+Sans+Tamil:wght@400;500;600;700&family=Noto+Sans+Telugu:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;500;600;700&display=swap" rel="stylesheet">\n</head>',
        1
    )
    print("✅ Multi-script fonts added")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ index.html saved")
