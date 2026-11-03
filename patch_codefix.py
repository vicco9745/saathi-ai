p='app/main.py'
s=open(p,encoding='utf-8').read()
if 'fix_code_blocks' in s:
    print('codefix: pehle se laga hai')
else:
    a='from ichat_ai.response_engine import get_response\n'
    b='"reply": result.get("reply") or "",'
    c='"reply": result if isinstance(result, str) else str(result),'
    if a in s and s.count(b)==1 and s.count(c)==1:
        s=s.replace(a,a+'from ichat_ai.code_fix import fix_code_blocks\n',1)
        s=s.replace(b,'"reply": fix_code_blocks(result.get("reply") or ""),',1)
        s=s.replace(c,'"reply": fix_code_blocks(result if isinstance(result, str) else str(result)),',1)
        open(p,'w',encoding='utf-8').write(s)
        print('codefix: laga diya')
    else:
        print('codefix: jagah nahi mili', a in s, s.count(b), s.count(c))
