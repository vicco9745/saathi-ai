path = 'app/main.py'
with open(path) as f:
    c = f.read()

old = '''def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # Analyze: agar code/file hai aur 'batao/check/analyze/dekho' bhi hai
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo'])
    if has_code and (has_analyze or len(m) > 500):
        return "analyze"'''

new = '''def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # ANALYZE — SABSE PEHLE (highest priority)
    if '=== file:' in m or '===file:' in m:
        return "analyze"
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo', 'file check', 'file dekho', 'file batao'])
    if has_code and (has_analyze or len(m) > 500):
        return "analyze"'''

if old in c:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print("✅ File priority fix ho gaya")
else:
    print("❌ Block nahi mila")
