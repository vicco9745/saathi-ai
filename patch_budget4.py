import re
p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''_BUI_EN = {"newBudget": "New Budget", "name": "Name", "nameHint": "e.g. Home budget", "total": "Total budget", "totalHint": "Enter amount", "expTitle": "Expenses - tick and enter amount", "addOwn": "Add your own expense", "totalSpent": "Total spent", "saving": "Savings", "submit": "Submit", "needName": "Enter a name", "needTotal": "Enter the total budget", "budget": "Budget", "spent": "Spent", "myBudgets": "My budgets", "seeAll": "All budgets", "noBudget": "No budget saved yet", "createNew": "Create a new budget", "notFound": "This budget was not found", "report": "Budget Report", "expense": "Expense", "amount": "Amount", "allTotalBudget": "Total budget", "allTotalSpent": "Total spent", "allTotalSaving": "Total savings", "c0": "Food", "c1": "Rent", "c2": "Electricity / Bills", "c3": "Travel", "c4": "Medicine", "c5": "Education", "c6": "Entertainment", "c7": "Shopping"}
_BUI_GROUPS = [
    ["newBudget", "name", "nameHint", "total", "totalHint", "expTitle", "addOwn", "totalSpent", "saving", "submit", "needName"],
    ["needTotal", "budget", "spent", "myBudgets", "seeAll", "noBudget", "createNew", "notFound", "report", "expense", "amount"],
    ["allTotalBudget", "allTotalSpent", "allTotalSaving", "c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7"],
]
_BUI_META = ("Return ONLY one JSON object, no markdown: {\"intent\": \"create\" or \"show\", \"lang\": \"BCP-47 code of the language of the user message, for example zh-CN, es, ar, ta\", \"cur\": \"currency symbol of the main country of that language\"}. "
             "intent is show if the user wants to see or check saved budgets, savings or a report, otherwise create.")
_BUI_TR = ("Translate every value of the JSON object after the word strings into the language of the user message. Keep the same keys. "
           "Return ONLY the JSON object, no markdown, no explanation. Keep each value short and natural.")
def _bui_json(out):
    import json as _j
    i = out.find("{")
    k = out.rfind("}")
    return _j.loads(out[i:k + 1])
@__APP__.post("/v1/budget-ui2")
def _budget_ui2(body: _BudgetUIReq, key=Depends(require_api_key)):
    import json as _j
    from concurrent.futures import ThreadPoolExecutor
    text = body.text.strip()[:300]
    errs = []
    def meta():
        try:
            return _bui_json(_call_groq(text, system=_BUI_META))
        except Exception as e:
            errs.append("meta: " + str(e)[:80])
            return {}
    def part(g):
        try:
            payload = "User message: " + text + "\nstrings: " + _j.dumps({k: _BUI_EN[k] for k in g}, ensure_ascii=False)
            d = _bui_json(_call_groq(payload, system=_BUI_TR))
            return {k: str(d.get(k, "")).strip() for k in g if str(d.get(k, "")).strip()}
        except Exception as e:
            errs.append("translate: " + str(e)[:80])
            return {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        fm = ex.submit(meta)
        fp = [ex.submit(part, g) for g in _BUI_GROUPS]
        mt = fm.result()
        labels = {}
        for f in fp:
            labels.update(f.result())
    intent = "show" if str(mt.get("intent", "")).lower().startswith("show") else "create"
    return {"intent": intent, "lang": str(mt.get("lang", "en")).strip() or "en", "cur": str(mt.get("cur", "")).strip(), "labels": labels, "err": "; ".join(errs)}

'''
if '/v1/budget-ui2' in s:
    print('budget4 server: pehle se laga hai')
else:
    m = re.search(r'@(\w+)\.post\(\s*["\']/v1/budget-ui["\']', s)
    a = s.find('def _detect_action(msg: str) -> str:')
    if not m or a < 0 or '_BudgetUIReq' not in s:
        print('budget4 server: jagah nahi mili', bool(m), a)
    else:
        s = s[:a] + BLOCK.replace('__APP__', m.group(1)) + s[a:]
        open(p, 'w', encoding='utf-8').write(s)
        print('budget4 server: laga diya')
