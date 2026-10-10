with open('app/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

helper = '''

def _strip_markdown(text: str) -> str:
    """Jawab se *** , ** , ## , ### jaise markdown symbols hata do.
    Sirf saaf plain text rakho — headings, bullets, sab as-is."""
    if not text:
        return text
    import re as _r
    t = text
    # Triple asterisk/underscore
    t = _r.sub(r'\\*\\*\\*+', '', t)
    t = _r.sub(r'___+', '', t)
    # Double asterisk / underscore (bold/italic)
    t = _r.sub(r'\\*\\*', '', t)
    t = _r.sub(r'(?<!\\w)__(?!\\w)', '', t)
    # Headings: ## ### etc — hata do hashes
    t = _r.sub(r'(?m)^\\s*#{1,6}\\s*', '', t)
    # Horizontal rule --- or ___
    t = _r.sub(r'(?m)^\\s*[-*_]{3,}\\s*$', '', t)
    # Inline code backticks
    t = t.replace('`', '')
    # Leading asterisk in bullets -> convert to bullet dot
    t = _r.sub(r'(?m)^\\s*\\*\\s+', '• ', t)
    # Stray asterisks leftover
    t = _r.sub(r'(?<!\\w)\\*(?!\\w)', '', t)
    # Extra blank lines
    t = _r.sub(r'\\n{3,}', '\\n\\n', t)
    return t.strip()
'''

if '_strip_markdown' not in code:
    marker = 'def _call_vision_v2('
    idx = code.find(marker)
    if idx == -1:
        print('FAIL: _call_vision_v2 not found')
        raise SystemExit(1)
    code = code[:idx] + helper.strip() + '\n\n\n' + code[idx:]
    print('OK: _strip_markdown added')
else:
    print('SKIP: already exists')

# Apply _strip_markdown to all replies before return

# 1. Vision path
old1 = 'reply = _polish_vision_reply(raw, body.message)'
new1 = 'reply = _strip_markdown(_polish_vision_reply(raw, body.message))'
if old1 in code and new1 not in code:
    code = code.replace(old1, new1, 1)
    print('OK: vision path wrapped')
elif new1 in code:
    print('SKIP: vision already wrapped')

# 2. Normal text chat return (result.get reply)
old2 = '''    if isinstance(result, dict):
        return {
            "service": "chat",
            "reply": result.get("reply"),
            "sources": result.get("sources", []),
            "model": "saathi"
        }
    return {
        "service": "chat",
        "reply": result,
        "model": "saathi"
    }'''
new2 = '''    if isinstance(result, dict):
        return {
            "service": "chat",
            "reply": _strip_markdown(result.get("reply") or ""),
            "sources": result.get("sources", []),
            "model": "saathi"
        }
    return {
        "service": "chat",
        "reply": _strip_markdown(result if isinstance(result, str) else str(result)),
        "model": "saathi"
    }'''
if old2 in code:
    code = code.replace(old2, new2, 1)
    print('OK: text chat path wrapped')
elif '_strip_markdown(result.get("reply")' in code:
    print('SKIP: text chat already wrapped')

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('SAVED')
