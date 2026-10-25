with open('app/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 718 (index 717) par yeh gadbad hai:
# "        )            "- [4-6 main points]\n\n""
# Hum isko sahi karenge

if len(lines) > 717:
    # Purani galat line ko replace karna
    # Hum bracket ke baad ek new line aur proper syntax dalenge
    lines[717] = '        )\n'

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('SUCCESS! Syntax error theek kar diya gaya.')
