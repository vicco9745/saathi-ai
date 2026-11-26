p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''from pydantic import BaseModel as _SFBM
class _SiteFixReq(_SFBM):
    html: str
    errors: str = ""
_SF_SYSTEM = (
    "You fix HTML websites. You get a full HTML document and a list of errors found when it ran in a browser. "
    "Return ONLY the complete corrected HTML document, starting with <!DOCTYPE html> and ending with </html>, "
    "no markdown fences, no explanation. Fix every listed error. Do not remove features and do not change the design or the text. "
    "Images: only picsum.photos or placehold.co, never source.unsplash.com. Every button and link must work. "
    "Always include <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> in the head."
)
@app.post("/v1/website-fix")
def website_fix(body: _SiteFixReq, key=Depends(require_api_key)):
    h = (body.html or "").strip()
    if not h or len(h) > 60000:
        return {"html": h}
    try:
        out = _call_groq("ERRORS FOUND:\n" + (body.errors or "")[:2000] + "\n\nHTML:\n" + h, system=_SF_SYSTEM)
    except Exception:
        return {"html": h}
    out = (out or "").replace("```html", "").replace("```", "").strip()
    i = out.lower().find("<!doctype")
    if i < 0:
        i = out.lower().find("<html")
    if i < 0:
        return {"html": h}
    out = out[i:]
    if "</html>" not in out.lower():
        return {"html": h}
    return {"html": out}

'''
marker = '@app.post("/v1/website")'
if '/v1/website-fix' in s:
    print('sitefix server: pehle se laga hai')
elif s.count(marker) != 1:
    print('sitefix server: jagah nahi mili', s.count(marker))
else:
    s = s.replace(marker, BLOCK + marker, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('sitefix server: laga diya')
