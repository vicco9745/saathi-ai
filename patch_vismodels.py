p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "_or_vision_models" in s:
    print("vismodels: pehle se laga hai")
    raise SystemExit
helper = '''_OR_VIS_CACHE = {"t": 0, "m": []}
def _or_vision_models():
    import time, requests
    if _OR_VIS_CACHE["m"] and time.time() - _OR_VIS_CACHE["t"] < 3600:
        return list(_OR_VIS_CACHE["m"])
    try:
        r = requests.get("https://openrouter.ai/api/v1/models", timeout=15)
        out = []
        for m in r.json().get("data", []):
            ins = (m.get("architecture") or {}).get("input_modalities") or []
            pr = m.get("pricing") or {}
            if "image" in ins and str(pr.get("prompt")) in ("0", "0.0") and str(pr.get("completion")) in ("0", "0.0"):
                out.append((m.get("context_length") or 0, m.get("id")))
        out.sort(reverse=True)
        ids = [i for _, i in out if i][:6]
        if ids:
            _OR_VIS_CACHE["t"] = time.time()
            _OR_VIS_CACHE["m"] = ids
        return ids
    except Exception:
        return []

'''
a = "def _call_vision_v2("
b = "        or_models = ["
c = "        for model in or_models:"
if s.count(a) == 1 and s.count(b) == 1 and s.count(c) == 1:
    s = s.replace(a, helper + a)
    s = s.replace(b, "        or_models = _or_vision_models() + [")
    s = s.replace(c, "        for model in list(dict.fromkeys(or_models)):")
    open(p, "w", encoding="utf-8").write(s)
    print("vismodels: patch lag gaya")
else:
    print("vismodels: lines nahi mili, kuch nahi badla", s.count(a), s.count(b), s.count(c))
