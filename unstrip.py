with open('app/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('reply = _strip_markdown(_polish_vision_reply(raw, body.message))',
                    'reply = _polish_vision_reply(raw, body.message)')
code = code.replace('_strip_markdown(result.get("reply") or "")', 'result.get("reply") or ""')
code = code.replace('_strip_markdown(result if isinstance(result, str) else str(result))',
                    'result if isinstance(result, str) else str(result)')

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('SAVED main.py — strip removed')
