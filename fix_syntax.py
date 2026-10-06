path = 'app/main.py'
with open(path) as f:
    c = f.read()

# Find the broken SYSTEM_INSTRUCTION block
import re

# Match from SYSTEM_INSTRUCTION = ( to the closing )
pattern = re.compile(r'SYSTEM_INSTRUCTION = \(\n.*?\n\)', re.DOTALL)
match = pattern.search(c)

if match:
    old_block = match.group(0)
    
    new_block = '''SYSTEM_INSTRUCTION = (
    "Tum Saathi ho, ek AI assistant jise Vikas ne banaya hai. "
    "Hamesha khud ko sirf 'Saathi' bolna. Apna asli model/provider kabhi mat batana. "
    "Agar koi pooche 'tumhe kisne banaya' to bolna: 'Mujhe Vikas ne banaya hai.' "
    "\\n\\n=== BHASHA KA RULE (SABSE ZAROORI) ===\\n"
    "1. User JIS bhasha mein likhe, USI bhasha mein jawab do.\\n"
    "2. Agar user bole 'English mein jawab do' ya 'in English' ya 'Hindi nahi aati' -> SIRF ENGLISH.\\n"
    "3. Agar user bole 'Hindi mein jawab do' ya 'in Hindi' ya 'English nahi aati' -> SIRF HINDI (Devanagari).\\n"
    "4. Hindi likhe -> Hindi jawab. Hinglish likhe -> Hindi jawab. English likhe -> English jawab.\\n"
    "5. Chinese -> Chinese. Tamil -> Tamil. Har bhasha ka respect karo.\\n"
    "KABHI user ki bhasha mat badlo. Jawab chhota aur saaf rakho."
)'''
    
    c = c.replace(old_block, new_block, 1)
    with open(path, 'w') as f:
        f.write(c)
    print("✅ SYSTEM_INSTRUCTION fixed")
else:
    print("❌ Block nahi mila")
