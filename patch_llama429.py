p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
if "fallback {_fm}" in s:
    print("pehle se laga hai")
    raise SystemExit
old = '''        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            print(f"[groq] HTTP {resp.status_code}")
            return None
        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            return None
        return (choices[0].get("message", {}).get("content") or "").strip() or None
'''
new = '''        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 429:
            print(f"[groq] HTTP 429 body: {resp.text[:300]}")
            for _fm in ("llama-3.3-70b-versatile", "llama-3.1-8b-instant"):
                _p2 = {k: v for k, v in payload.items() if k not in ("frequency_penalty", "presence_penalty")}
                _p2["model"] = _fm
                try:
                    resp = requests.post(url, headers=headers, json=_p2, timeout=30)
                except Exception as _e2:
                    print(f"[groq] fallback {_fm} crashed: {_e2}")
                    continue
                print(f"[groq] fallback {_fm} -> HTTP {resp.status_code}")
                if resp.status_code == 200:
                    break
        if resp.status_code != 200:
            print(f"[groq] HTTP {resp.status_code}")
            return None
        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            return None
        return (choices[0].get("message", {}).get("content") or "").strip() or None
'''
if s.count(old) != 1:
    print("match nahi mila, kuch nahi badla:", s.count(old))
    raise SystemExit
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("ai_providers.py badal gaya")
