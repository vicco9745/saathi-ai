path = 'ichat_ai/ai_providers.py'
with open(path) as f:
    c = f.read()

old = '''_PROVIDERS = [
    ("openrouter", _call_openrouter),
    ("groq", _call_groq),
    ("gemini", _call_gemini),
    ("deepseek", _call_deepseek),
]'''

new = '''_PROVIDERS = [
    ("groq", _call_groq),
    ("openrouter", _call_openrouter),
    ("gemini", _call_gemini),
    ("deepseek", _call_deepseek),
]'''

if old in c:
    c = c.replace(old, new)
    with open(path, 'w') as f:
        f.write(c)
    print("OK - Groq first, OpenRouter fallback")
else:
    print("FAIL - providers block nahi mila")
