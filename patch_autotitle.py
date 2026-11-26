import re
p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''class _Title2Req(BaseModel):
    message: str
_TITLE2_SYSTEM = (
    "Write a chat title for the user's first message. Use the same language and script as the message. "
    "4 to 8 words, specific and descriptive about the topic or task, not a generic label. "
    "No quotes, no emoji, no trailing punctuation, no prefix like Title. Output only the title."
)
@__APP__.post("/v1/title2")
def _title2(body: _Title2Req, key=Depends(require_api_key)):
    try:
        out = _call_groq(body.message.strip()[:300], system=_TITLE2_SYSTEM).strip().splitlines()[0].strip()
        out = out.strip('"\'“”‘’`*# ').rstrip('.।!?。 ')
        if 2 <= len(out) <= 80:
            return {"title": out}
    except Exception:
        pass
    return {"title": ""}

'''
if '/v1/title2' in s:
    print('autotitle server: pehle se laga hai')
else:
    m = re.search(r'@(\w+)\.post\(\s*["\']/v1/title["\']', s)
    a = s.find('def _detect_action(msg: str) -> str:')
    pk = s.find('require_api_key')
    pb = s.find('BaseModel')
    if not m or a < 0 or pk < 0 or pb < 0 or pk > a or pb > a:
        print('autotitle server: jagah nahi mili', bool(m), a, pk, pb)
    else:
        s = s[:a] + BLOCK.replace('__APP__', m.group(1)) + s[a:]
        open(p, 'w', encoding='utf-8').write(s)
        print('autotitle server: laga diya')
