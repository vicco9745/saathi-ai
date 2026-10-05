path = 'app/main.py'
with open(path) as f:
    c = f.read()

# Fix the detect function to catch file analysis text
old = '''    # ANALYZE — SABSE PEHLE (highest priority)
    if '=== file:' in m or '===file:' in m:
        return "analyze"'''

new = '''    # ANALYZE — SABSE PEHLE (highest priority)
    if '=== file:' in m or '===file:' in m:
        return "analyze"
    if 'user ne neeche file bheji' in m:
        return "analyze"
    if 'file ka naam:' in m and '---' in m:
        return "analyze"
    if 'file analyze karo' in m or 'file padho' in m:
        return "analyze"'''

if old in c:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print("✅ Detect fix ho gaya")
else:
    print("❌ Block nahi mila")
