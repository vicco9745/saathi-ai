p='ichat_ai/ai_providers.py'
s=open(p,encoding='utf-8').read()
if 'ichat_ai.samajh' in s:
    print('samajh: pehle se laga hai')
else:
    marker='def _call_gemini(prompt):'
    block='try:\n    from ichat_ai.samajh import SAMAJH_RULES\n    SYSTEM_INSTRUCTION += SAMAJH_RULES\nexcept Exception:\n    pass\n\n\n'
    if marker in s:
        s=s.replace(marker,block+marker,1)
        open(p,'w',encoding='utf-8').write(s)
        print('samajh: laga diya')
    else:
        print('samajh: marker nahi mila')
