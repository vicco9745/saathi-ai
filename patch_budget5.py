p = 'app/main.py'
s = open(p, encoding='utf-8').read()
NEW = r'''    def _extract(d, g):
        if not isinstance(d, dict):
            return {}
        for _ in range(3):
            if any(k in d for k in g):
                break
            inner = [v for v in d.values() if isinstance(v, dict)]
            if not inner:
                break
            d = inner[0]
        res = {k: str(d.get(k, "")).strip() for k in g if str(d.get(k, "")).strip()}
        if not res:
            vals = [str(v).strip() for v in d.values() if isinstance(v, str) and str(v).strip()]
            if len(vals) == len(g):
                res = dict(zip(g, vals))
        return res
    def part(g):
        out = ""
        try:
            payload = "The user wrote: " + text + "\nTranslate the values of this JSON object into the language the user wrote in. Keep the same keys. Return only the JSON object.\n" + _j.dumps({k: _BUI_EN[k] for k in g}, ensure_ascii=False)
            out = _call_groq(payload, system=_BUI_TR)
            res = _extract(_bui_json(out), g)
            if not res:
                errs.append("empty: " + out.replace("\n", " ")[:90])
            return res
        except Exception as e:
            errs.append("translate: " + str(e)[:50] + " | " + str(out).replace("\n", " ")[:60])
            return {}
'''
if 'def _extract(d, g)' in s:
    print('budget5: pehle se laga hai')
else:
    base = s.find('/v1/budget-ui2')
    a = s.find('    def part(g):', base)
    b = s.find('    with ThreadPoolExecutor(max_workers=4) as ex:', base)
    if base < 0 or a < 0 or b < 0 or b < a:
        print('budget5: jagah nahi mili', base, a, b)
    else:
        s = s[:a] + NEW + s[b:]
        s = s.replace('Translate every value of the JSON object after the word strings into the language of the user message.', 'Translate the values of the JSON object into the language of the user message.', 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget5: laga diya')
