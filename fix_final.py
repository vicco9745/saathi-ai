path = 'app/main.py'
with open(path) as f:
    c = f.read()

old = '''def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # ANALYZE — SABSE PEHLE (highest priority)
    if '=== file:' in m or '===file:' in m:
        return "analyze"
    if 'user ne neeche file bheji' in m:
        return "analyze"
    if 'file ka naam:' in m and '---' in m:
        return "analyze"
    if 'file analyze karo' in m or 'file padho' in m:
        return "analyze"
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo', 'file check', 'file dekho', 'file batao'])
    if has_code and (has_analyze or len(m) > 500):
        return "analyze"'''

new = '''def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # ═══ STEP 1: LAMBA MESSAGE = FILE UPLOAD → हमेशा ANALYZE ═══
    if len(msg) > 1500:
        return "analyze"
    # ═══ STEP 2: FILE MARKERS ═══
    if '=== file:' in m or '===file:' in m:
        return "analyze"
    if 'user ne neeche file bheji' in m or 'user ne neeche file bheja' in m:
        return "analyze"
    if 'file ka naam:' in m and '---' in m:
        return "analyze"
    if 'file bheji' in m or 'file bheja' in m or 'file check' in m or 'file padho' in m or 'file dekho' in m or 'file batao' in m:
        return "analyze"
    # ═══ STEP 3: Code + analyze words ═══
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo'])
    if has_code and has_analyze:
        return "analyze"'''

if old in c:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print("✅ Backend fix ho gaya")
else:
    print("❌ Block nahi mila")
