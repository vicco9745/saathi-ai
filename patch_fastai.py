p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
if '"reasoning_effort"' in s:
    print("already patched")
else:
    a = '''            "presence_penalty": 0.3,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)'''
    b = '''            "presence_penalty": 0.3,
            "reasoning_effort": "low",
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)'''
    c = '''_p2 = {k: v for k, v in payload.items() if k not in ("frequency_penalty", "presence_penalty")}'''
    d = '''_p2 = {k: v for k, v in payload.items() if k not in ("frequency_penalty", "presence_penalty") and (k != "reasoning_effort" or "gpt-oss" in _fm)}'''
    assert a in s and c in s, "match nahi mila"
    s = s.replace(a, b, 1).replace(c, d, 1)
    open(p, "w", encoding="utf-8").write(s)
    print("patched")
