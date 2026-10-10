with open('app/main.py', 'r', encoding='utf-8') as f:
    code = f.read()

endpoint = '''

class TitleRequest(BaseModel):
    message: Optional[str] = ""
    image: Optional[str] = None


def _title_from_text(text: str) -> str:
    if not text or not text.strip():
        return ""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        t = text.strip().replace("\\n", " ")
        return t[:40] + ("…" if len(t) > 40 else "")
    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": "User ke message ka 3-6 shabd ka chat title banao. Sirf title likho, koi quote nahi, koi punctuation nahi. User ki bhasha mein hi rakho."},
                    {"role": "user", "content": text},
                ],
                "max_tokens": 30,
                "temperature": 0.3,
            },
            timeout=30,
        )
        if r.status_code != 200:
            t = text.strip().replace("\\n", " ")
            return t[:40] + ("…" if len(t) > 40 else "")
        data = r.json()
        t = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        t = t.replace("\\n", " ").replace('"', '').replace("'", "").strip()
        return t[:50] if t else text.strip()[:40]
    except Exception:
        t = text.strip().replace("\\n", " ")
        return t[:40] + ("…" if len(t) > 40 else "")


def _title_from_image(image_data_url: str) -> str:
    if not image_data_url or not image_data_url.startswith("data:image"):
        return "Photo message"
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return "Photo message"
    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "qwen/qwen3.8-27b",
                "messages": [
                    {"role": "user", "content": [
                        {"type": "text", "text": "Is photo ka 3-5 shabd ka chat title banao. Sirf title likho, koi quote nahi. User ki bhasha mein, warna Hindi/Hinglish."},
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                    ]},
                ],
                "max_tokens": 30,
                "temperature": 0.3,
            },
            timeout=40,
        )
        if r.status_code != 200:
            return "Photo message"
        data = r.json()
        t = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        t = t.replace("\\n", " ").replace('"', '').replace("'", "").strip()
        return t[:50] if t else "Photo message"
    except Exception:
        return "Photo message"


@app.post("/v1/title")
def make_title(body: TitleRequest, key=Depends(require_api_key)):
    record_usage(key, "title")
    text = (body.message or "").strip()
    if text:
        title = _title_from_text(text)
    elif body.image:
        title = _title_from_image(body.image)
    else:
        title = "New chat"
    return {"title": title}
'''

if '/v1/title' not in code:
    code = code.rstrip() + endpoint
    print('OK: /v1/title endpoint added')
else:
    print('SKIP: already exists')

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('SAVED')
