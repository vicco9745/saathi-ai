p='ichat_ai/ai_providers.py'
s=open(p,encoding='utf-8').read()
a=s.find('def _call_groq(')
b=s.find('def _call_openrouter(')
if a<0 or b<0 or b<a:
    print('model: jagah nahi mili')
else:
    seg=s[a:b]
    if 'GROQ_MODEL' in seg:
        print('model: pehle se laga hai')
    else:
        seg=seg.replace('"model": "openai/gpt-oss-120b",','"model": GROQ_MODEL,',1)
        seg=seg.replace('"temperature": 0.7,','"temperature": GROQ_TEMPERATURE,',1)
        imp='from ichat_ai.model_config import GROQ_MODEL, GROQ_TEMPERATURE\n\n\n'
        s=s[:a]+imp+seg+s[b:]
        open(p,'w',encoding='utf-8').write(s)
        print('model: laga diya', 'GROQ_MODEL' in seg, 'GROQ_TEMPERATURE' in seg)
