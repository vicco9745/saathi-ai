p = 'app/main.py'
s = open(p, encoding='utf-8').read()
FN = r'''def _pdf_web_context(prompt):
    import os, re, datetime
    from concurrent.futures import ThreadPoolExecutor
    key = os.environ.get("TAVILY_API_KEY") or os.environ.get("TAVILY_KEY") or ""
    if not key:
        print("PDF search: TAVILY_API_KEY not set")
        return ""
    try:
        q = _call_groq(prompt, system=(
            "If writing the document the user asks for needs facts from the internet "
            "(news, prices, markets, companies, places, people, statistics, recent events, current data), "
            "reply with 1 to 3 short web search queries, one per line, no numbering, no explanation. "
            "If no web facts are needed (for example a bill, resume, certificate or plain template), reply exactly NONE."
        ))
    except Exception:
        return ""
    lines = [re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", l).strip() for l in (q or "").splitlines() if l.strip()]
    if not lines or lines[0].upper().startswith("NONE"):
        return ""
    qs = [l[:200] for l in lines[:3]]
    def one(qq):
        try:
            import requests
            r = requests.post(
                "https://api.tavily.com/search",
                headers={"Authorization": "Bearer " + key},
                json={"api_key": key, "query": qq, "search_depth": "advanced", "max_results": 5, "include_answer": True},
                timeout=25,
            )
            if r.status_code != 200:
                print("PDF search http", r.status_code)
                return None
            return r.json()
        except Exception as e:
            print("PDF search error", repr(e)[:120])
            return None
    with ThreadPoolExecutor(max_workers=3) as ex:
        res = list(ex.map(one, qs))
    parts = []
    for qq, d in zip(qs, res):
        if not d:
            continue
        if d.get("answer"):
            parts.append("SUMMARY for " + qq + ": " + str(d["answer"])[:600])
        for it in (d.get("results") or [])[:5]:
            parts.append("- " + str(it.get("title", ""))[:120] + " (" + str(it.get("url", "")) + "): " + str(it.get("content", ""))[:600])
    if not parts:
        return ""
    return (
        "WEB SOURCES (fetched on " + datetime.date.today().isoformat() + "; use these for current facts, numbers and dates, "
        "name the source next to each such number, and end the document with an h2 Sources section listing the sources used):\n"
        + "\n".join(parts)[:9000]
    )

'''
ACC_OLD = '        "Use only numbers the user supplied; where such a number is needed but missing, leave a clearly marked [fill in] in the table. "\n'
ACC_NEW = '        "Use only numbers the user supplied or that appear in the WEB SOURCES block of the request; where such a number is needed but in neither, leave a clearly marked [fill in] in the table. "\n'
CALL_OLD = '    html_body = _call_groq(body.prompt, system=system)'
CALL_NEW = '    _ctx = _pdf_web_context(body.prompt)\n    html_body = _call_groq(body.prompt + (("\\n\\n" + _ctx) if _ctx else ""), system=system)'
if '_pdf_web_context' in s:
    print('pdf5: pehle se laga hai')
else:
    bad = []
    if s.count(ACC_OLD) != 1: bad.append('accuracy')
    if s.count(CALL_OLD) != 1: bad.append('call')
    if s.count('def _pdf_theme_from_prompt(t):') != 1: bad.append('themefn')
    if bad:
        print('pdf5: jagah nahi mili', bad)
    else:
        s = s.replace(ACC_OLD, ACC_NEW, 1)
        s = s.replace(CALL_OLD, CALL_NEW, 1)
        s = s.replace('def _pdf_theme_from_prompt(t):', FN + 'def _pdf_theme_from_prompt(t):', 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('pdf5: laga diya')
