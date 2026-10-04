path1 = 'ichat_ai/ai_providers.py'
with open(path1) as f:
    c1 = f.read()

# Add change-report rule to system instruction
old1 = "Jawab chhota, saaf, natural aur seedha point par rakhna."

new1 = """Jawab chhota, saaf, natural aur seedha point par rakhna.\\n\\n"
    "=== CODE/FILE FIX KARNE KA RULE ===\\n"
    "Agar user koi code, file, ya document de aur bole 'fix karo', 'sahi karo', "
    "'theek karo', 'improve karo', ya kuch aisa -> to:\\n"
    "1. Pehle poora fixed code/file do (koi line na kaato)\\n"
    "2. Code/file ke NEECHE ek 'CHANGES' section likho jisme:\\n"
    "   - Kya-kya badla (list mein)\\n"
    "   - Kya-kya hataya\\n"
    "   - Kya-kya add kiya\\n"
    "   - Kya-kya theek kiya\\n"
    "3. Aakhir mein poochho: 'Aap ek baar check kar lijiye. "
    "Koi galti ho, kuch aur chahiye, ya kuch samajh na aaye to bataaiye — "
    "main turant theek kar dunga.'\\n"
    "Yeh format HAR baar follow karo jab code/file de.\""""

if old1 in c1:
    c1 = c1.replace(old1, new1)
    with open(path1, 'w') as f:
        f.write(c1)
    print("✅ ai_providers.py updated")
else:
    print("❌ ai_providers.py - block nahi mila")

# Update app/main.py website system prompt
path2 = 'app/main.py'
with open(path2) as f:
    c2 = f.read()

old2 = "12. Koi button dead nahi — har click pe action."

new2 = """12. Koi button dead nahi — har click pe action.\\n"
                "\\n=== RESPONSE FORMAT (CODE DENE KE BAAD) ===\\n"
                "Jab tum koi code/website/file do, to code ke NEECHE ye likho:\\n"
                "\\n📋 CHANGES / क्या किया:\\n"
                "- [Kya-kya banaya/badla — list mein]\\n"
                "\\n✅ FEATURES ADD KIYE:\\n"
                "- [Naye features]\\n"
                "\\n📝 Aap check kariye:\\n"
                "Koi galti ho, kuch aur chahiye, ya samajh na aaye to bataaiye — "
                "main turant theek kar dunga.\""""

if old2 in c2:
    c2 = c2.replace(old2, new2)
    with open(path2, 'w') as f:
        f.write(c2)
    print("✅ app/main.py updated")
else:
    print("❌ app/main.py - block nahi mila")
