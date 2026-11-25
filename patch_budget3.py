import re
p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''_BUI_KEYS = ["newBudget", "name", "nameHint", "total", "totalHint", "expTitle", "addOwn", "totalSpent", "saving", "submit", "needName", "needTotal", "budget", "spent", "myBudgets", "seeAll", "noBudget", "createNew", "notFound", "report", "expense", "amount", "allTotalBudget", "allTotalSpent", "allTotalSaving", "c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7"]
_BUI_SYSTEM = (
    "Detect the language of the user message. Return ONLY one JSON object, no markdown: "
    "{\"intent\": \"create\" or \"show\", \"lang\": BCP-47 code such as zh-CN or es or ar, "
    "\"cur\": the currency symbol used in the main country of that language, "
    "\"labels\": {key: translation}}. "
    "intent is show if the user wants to see or check saved budgets, savings or a report, otherwise create. "
    "Translate these English labels into the language of the message, short and natural, one translation per key. Keys (key=English): "
    "newBudget=New Budget | name=Name | nameHint=e.g. Home budget | total=Total budget | totalHint=Enter amount | "
    "expTitle=Expenses - tick and enter amount | addOwn=Add your own expense | totalSpent=Total spent | saving=Savings | submit=Submit | "
    "needName=Enter a name | needTotal=Enter the total budget | budget=Budget | spent=Spent | myBudgets=My budgets | seeAll=All budgets | "
    "noBudget=No budget saved yet | createNew=Create a new budget | notFound=This budget was not found | report=Budget Report | "
    "expense=Expense | amount=Amount | allTotalBudget=Total budget | allTotalSpent=Total spent | allTotalSaving=Total savings | "
    "c0=Food | c1=Rent | c2=Electricity / Bills | c3=Travel | c4=Medicine | c5=Education | c6=Entertainment | c7=Shopping. "
    "Output every key listed."
)
class _BudgetUIReq(BaseModel):
    text: str
@__APP__.post("/v1/budget-ui")
def _budget_ui(body: _BudgetUIReq, key=Depends(require_api_key)):
    import json as _jb
    try:
        out = _call_groq(body.text.strip()[:300], system=_BUI_SYSTEM).strip()
        i = out.find("{")
        j = out.rfind("}")
        d = _jb.loads(out[i:j + 1])
        raw = d.get("labels") if isinstance(d.get("labels"), dict) else {}
        labels = {k: str(raw.get(k, "")).strip() for k in _BUI_KEYS if str(raw.get(k, "")).strip()}
        intent = "show" if str(d.get("intent", "")).lower().startswith("show") else "create"
        return {"intent": intent, "lang": str(d.get("lang", "en")).strip() or "en", "cur": str(d.get("cur", "")).strip(), "labels": labels}
    except Exception:
        return {"intent": "create", "lang": "en", "cur": "", "labels": {}}

'''
if '/v1/budget-ui' in s:
    print('budget server: pehle se laga hai')
else:
    m = re.search(r'@(\w+)\.post\(\s*["\']/v1/title["\']', s)
    a = s.find('def _detect_action(msg: str) -> str:')
    pk = s.find('require_api_key')
    pb = s.find('BaseModel')
    if not m or a < 0 or pk < 0 or pb < 0 or pk > a or pb > a:
        print('budget server: jagah nahi mili', bool(m), a, pk, pb)
    else:
        app = m.group(1)
        pa = re.search(r'^' + app + r'\s*=', s, re.M)
        if not pa or pa.start() > a:
            print('budget server: app pehle nahi bana', app)
        else:
            s = s[:a] + BLOCK.replace('__APP__', app) + s[a:]
            open(p, 'w', encoding='utf-8').write(s)
            print('budget server: laga diya')
