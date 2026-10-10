with open('app/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

endpoint = '''

class DesignRequest(BaseModel):
    prompt: str
    photo: Optional[str] = None  # data URL
    model: Optional[str] = "Default"


def _clean_html(h: str) -> str:
    h = (h or "").strip()
    if "```" in h:
        h = h.replace("```html", "").replace("```", "").strip()
    return h


@app.post("/v1/design")
def make_design(body: DesignRequest, key=Depends(require_api_key)):
    """HTML/CSS se design banao — card, poster, banner, invitation, kuch bhi."""
    record_usage(key, "design")

    system = (
        "Tum ek expert graphic designer aur frontend developer ho. "
        "User jo bhi design mange — wedding card, greeting card, poster, banner, "
        "visiting card, invitation, certificate, menu, flyer, kuch bhi — "
        "uska COMPLETE HTML+CSS design banao.\\n\\n"
        "RULES:\\n"
        "1. Sirf pure HTML return karo — <!DOCTYPE html> se shuru, </html> par khatam.\\n"
        "2. Sab CSS inline <style> tag mein ho — alag file nahi.\\n"
        "3. Design mobile aur desktop dono par sahi dikhe — responsive.\\n"
        "4. Text saaf aur bada ho — print karne layak.\\n"
        "5. Sundar fonts use karo — Google Fonts ke through (link tag se).\\n"
        "6. Colors, shadows, borders, gradients — sab professional ho.\\n"
        "7. Agar user photo bheje to usko <img> se design mein lagao.\\n"
        "8. Text user ki bhasha mein — Hindi likhe to Hindi, English likhe to English.\\n"
        "9. Har cheez jo user ne kahi — naam, tareekh, jagah, rang, sab daalo.\\n"
        "10. Koi markdown nahi, koi explanation nahi, sirf HTML.\\n\\n"
        "DIMENSION: Agar card hai to A4 ya 800x600 jaisa. Agar social post hai to square (1080x1080). "
        "Agar banner hai to wide (1200x400). User ne jo kaha uske hisab se."
    )

    prompt_text = body.prompt or ""
    if body.photo and body.photo.startswith("data:image"):
        prompt_text += "\\n\\n[User ki photo neeche di hai — ise design mein shamil karo: " + body.photo[:100] + "... ]"

    try:
        html = _call_groq(prompt_text, system=system)
        html = _clean_html(html)
        if not html or "<html" not in html.lower():
            raise HTTPException(500, "Design generate nahi hua")
        return {
            "service": "design",
            "reply": "Yeh raha aapka design.",
            "html": html,
            "filename": "design.html",
            "kind": "design",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, "Design banane mein problem: " + str(e))
'''

if '/v1/design' not in code:
    code = code.rstrip() + endpoint
    print('OK: /v1/design endpoint added')
else:
    print('SKIP: already exists')

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(code)

import ast
try:
    ast.parse(code)
    print('SYNTAX OK')
except SyntaxError as e:
    print('SYNTAX ERROR:', e)
    raise SystemExit(1)

print('SAVED')
