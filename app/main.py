import os
import requests as _req
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .db import init_db
from .auth import require_api_key, record_usage
from ichat_ai.response_engine import get_response

app = FastAPI(
    title="iChat API",
    version="1.0.0",
    description="One API gateway for iChat services."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

class ChatAttachment(BaseModel):
    kind: Optional[str] = None
    dataUrl: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    model: str = "auto"
    memory: Optional[List[str]] = []
    allow_web_search: Optional[bool] = False
    attachments: Optional[List[ChatAttachment]] = []

class GenericRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024

@app.get("/")
def home():
    return {"name": "iChat API", "status": "online"}

@app.get("/v1/me")
def me(key=Depends(require_api_key)):
    return {
        "name": key[1],
        "owner": bool(key[3]),
        "plan": key[5],
        "requests": key[6],
        "limit": None if key[3] else "configured by plan"
    }

SYSTEM_INSTRUCTION = (
    "Tum Saathi ho, ek AI assistant jise Vikas ne banaya hai. "
    "Hamesha khud ko sirf 'Saathi' bolna. Apna asli model/provider kabhi mat batana. "
    "Agar koi pooche 'tumhe kisne banaya' to bolna: 'Mujhe Vikas ne banaya hai.' "
    "\n\n=== BHASHA KA RULE (SABSE ZAROORI) ===\n"
    "1. User JIS bhasha mein likhe, USI bhasha mein jawab do.\n"
    "2. Agar user bole 'English mein jawab do' ya 'in English' ya 'Hindi nahi aati' -> SIRF ENGLISH.\n"
    "3. Agar user bole 'Hindi mein jawab do' ya 'in Hindi' ya 'English nahi aati' -> SIRF HINDI (Devanagari).\n"
    "4. Hindi likhe -> Hindi jawab. Hinglish likhe -> Hindi jawab. English likhe -> English jawab.\n"
    "5. Chinese -> Chinese. Tamil -> Tamil. Har bhasha ka respect karo.\n"
    "KABHI user ki bhasha mat badlo. Jawab chhota aur saaf rakho.

═══════════════════════════════════════
HAR BHASHA MEIN QUALITY LIKHNE KA RULE
═══════════════════════════════════════

1. SAHI SCRIPT (लिपि) USE KARO:
- Hindi → शुद्ध देवनागरी (अ, आ, क, ख, ग...)
- English → Proper English spelling
- Tamil → சரியான தமிழ் எழுத்துக்கள்
- Telugu → సరైన తెలుగు అక్షరాలు
- Bengali → সঠিক বাংলা হরফ
- Chinese → 正确的汉字
- Japanese → 正しい日本語
- Arabic → العربية الصحيحة
- Spanish/French/German → Proper accents (é, ñ, ü, etc.)

2. NATURAL LIKHO — Machine translation jaisa nahi:
- BAD: "यह फाइल एक है HTML फाइल जो है 385 KB"
- GOOD: "यह एक HTML फाइल है जिसका आकार 385 KB है।"

3. POORE VAKYA LIKHO:
- Aadhe-adhoore sentences mat likho
- Har vakya ka pura matlab ho
- Sahi punctuation use karo (. , ? !)

4. TECHNICAL SHABD:
- Jo shabd sab jagah same rehte hain (HTML, PDF, CSS, API, URL), unhe as-is rakho
- Baaki sab local bhasha mein likho

5. MIXED BHASHA (Hinglish):
- Agar user Hinglish mein likhe, jawab Hindi (Devanagari) mein do
- English words Devanagari mein likho: 'file' → 'फाइल'

6. TONE:
- Friendly aur natural
- Formal English ya bhaari Hindi nahi
- Jaise dost baat karta hai waise likho

7. GRAAMMAR SAHI KARO:
- Hindi: सही लिंग, वचन, कारक (का, की, के, को, से, में, पर)
- English: correct tense, articles (a, an, the)
- Har bhasha ke grammar rules follow karo

8. EMOJI + FORMATTING:
- Emoji ke baad space do: "अच्छा 👍 ठीक है"
- Headings ke liye ## use karo
- Lists ke liye - ya 1. use karo

9. USER KI BHASHA RESPECT KARO:
- User jis bhasha mein likhe, usi mein likho
- Kabhi mat badlo — Hindi wale ko English, English wale ko Hindi

10. DETAIL MAT KATO:
- Poora jawab do, beech se mat todo
- Chhota rakhna hai to saaf likho — adhoora mat chhodo
"
)


def _call_openrouter_vision(prompt: str, images: list) -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise HTTPException(503, "OPENROUTER_API_KEY set nahi hai")

    content = [{"type": "text", "text": prompt or "Is photo me kya hai? Puri detail batao."}]
    for img in images[:3]:
        url = img.dataUrl or ""
        if not url.startswith("data:image"):
            continue
        content.append({
            "type": "image_url",
            "image_url": {"url": url},
        })

    models_to_try = [
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.2-11b-vision-instruct:free",
        "qwen/qwen-2-vl-7b-instruct:free",
        "openrouter/free",
    ]

    last_err = None
    for model in models_to_try:
        try:
            r = _req.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": content},
                    ],
                },
                timeout=300,
            )
            if r.status_code != 200:
                last_err = f"{model}: HTTP {r.status_code}"
                continue
            data = r.json()
            choices = data.get("choices") or []
            if not choices:
                last_err = f"{model}: no choices"
                continue
            txt = (choices[0].get("message", {}).get("content") or "").strip()
            if txt:
                return txt
        except Exception as e:
            last_err = f"{model}: {e}"

    raise HTTPException(500, f"Vision fail: {last_err}")


import re as _re

def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # ═══ STEP 1: LAMBA MESSAGE = FILE UPLOAD → हमेशा ANALYZE ═══
    if len(msg) > 1500:
        return "analyze"
    # ═══ STEP 2: FILE MARKERS ═══
    if '=== file:' in m or '===file:' in m:
        return "analyze"
    if 'user ne neeche file bheji' in m or 'user ne neeche file bheja' in m:
        return "analyze"
    if 'file ka naam:' in m and '---' in m:
        return "analyze"
    if 'file bheji' in m or 'file bheja' in m or 'file check' in m or 'file padho' in m or 'file dekho' in m or 'file batao' in m:
        return "analyze"
    # ═══ STEP 3: Code + analyze words ═══
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo'])
    if has_code and has_analyze:
        return "analyze"
    # PDF
    if _re.search(r"\bpdf\b|पीडीएफ|पी\.डी\.एफ|document banao|report banao|docx banao|letter banao", m):
        return "pdf"
    # Website
    if _re.search(r"\bwebsite\b|\bsite\b|वेबसाइट|webpage|landing page|html page|homepage banao|web page", m):
        return "website"
    # Image (banane ke liye — dekhne ke liye nahi)
    if _re.search(r"(image|photo|picture|तस्वीर|फोटो|चित्र|pic).*(banao|banaao|bana do|generate|create|banade|बनाओ|बनाओ|बना दो|बनाएं|बनायें)", m) or \
       _re.search(r"(banao|banaao|generate|create|bana do).*(image|photo|picture|तस्वीर|फोटो|चित्र)", m):
        return "image"
    return "chat"


@app.post("/v1/chat")
def chat(body: ChatRequest, key=Depends(require_api_key)):
    record_usage(key, "chat")

    # Agar user ne image bheji hai to vision path use karo
    images = [a for a in (body.attachments or []) if a.kind == "photo" and a.dataUrl]

    if images:
        reply = _call_openrouter_vision(body.message, images)
        return {
            "service": "chat",
            "reply": reply,
            "model": "saathi-vision",
        }

    # Auto-detect: kya user PDF/website/image banana chahta hai?
    action = _detect_action(body.message)

    if action == "analyze":
        system = (
            "Tum ek professional code reviewer ho. User ne file bheji hai. "
            "CHHOTA aur SAARBHUT analysis do (max 200 words):\n\n"
            "## 📄 File Type\n"
            "[HTML/CSS/JS/Python]\n\n"
            "## 📋 Kya-Kya Hai\n"
            "- [4-6 main points]\n\n"
            "## ✅ Achhi Baatein\n"
            "- [3-4 points]\n\n"
            "## ⚠️ Kamiyan\n"
            "- [3-4 points]\n\n"
            "## 🔧 Improvements\n"
            "- [3-4 suggestions]\n\n"
            "## 🌟 Rating: X/10\n\n"
            "Chhota rakho. User ki bhasha mein."
        )
        try:
            reply = _call_groq(body.message, system=system)
            return {"service": "chat", "reply": reply, "model": "saathi", "kind": "analysis"}
        except Exception as e:
            return {"service": "chat", "reply": f"Analysis mein problem: {e}", "model": "saathi"}

    if action == "pdf":
        try:
            import base64 as _b64
            from io import BytesIO as _BIO
            from xhtml2pdf import pisa as _pisa
            system = (
                "Tum ek professional document writer ho. User ki request ke hisab se "
                "ek achha HTML document banao (title, headings, paragraphs, lists). "
                "Sirf pure HTML return karo — <html> se shuru, </html> par khatam. "
                "User jis bhasha mein likhe usi bhasha mein content banao. "
                "Sirf HTML, koi explanation nahi, koi markdown nahi."
            )
            html_body = _call_groq(body.message, system=system).strip()
            if "```" in html_body:
                html_body = html_body.replace("```html", "").replace("```", "").strip()
            full_html = "<html><head><meta charset='utf-8'></head><body>" + html_body + "</body></html>"
            buf = _BIO()
            _pisa.CreatePDF(full_html, dest=buf, encoding="utf-8")
            pdf_b64 = _b64.b64encode(buf.getvalue()).decode("utf-8")
            buf.close()
            return {
                "service": "chat",
                "reply": "Yeh raha aapka PDF.",
                "pdf_base64": pdf_b64,
                "filename": "saathi.pdf",
                "model": "saathi",
                "kind": "pdf",
            }
        except Exception as e:
            return {"service": "chat", "reply": f"PDF banane mein problem aayi: {e}", "model": "saathi"}

    if action == "website":
        try:
            system = (
                "Tum ek expert full-stack web developer ho. User ki request ke hisab se ek "
                "COMPLETE, FULLY WORKING HTML website banao (HTML + inline CSS + JS). "
                "Sirf pure HTML code return karo, koi explanation nahi, koi markdown nahi. "
                "Shuru <!DOCTYPE html> se, khatam </html> par.\n"
                "ZAROORI RULES:\n"
                "1. IMAGES: Sirf picsum.photos ya placehold.co use karo. source.unsplash.com KABHI NAHI (band hai).\n"
                "2. HAR BUTTON KAAM KARE: nav links smooth scroll, Get Started contact pe, hamburger JS toggle.\n"
                "3. IMAGE UPLOAD: input type=file with preview.\n"
                "4. EDIT: headings pe contenteditable=true, Edit button.\n"
                "5. ADD/DELETE: Add Item button, har item pe delete button.\n"
                "6. FORM: submit pe alert + reset.\n"
                "7. SMOOTH SCROLL: html{scroll-behavior:smooth}.\n"
                "8. HOVER EFFECTS: har button aur card pe.\n"
                "9. MOBILE RESPONSIVE: media queries.\n"
                "10. CSS VARIABLES colors ke liye.\n"
                "11. Koi button dead nahi — har click pe action.\n"
                "\n📋 CHANGES / क्या किया (code ke neeche likho):\n"
                "- [Kya-kya banaya/badla — list mein]\n"
                "\n✅ FEATURES ADD KIYE:\n"
                "- [Naye features]\n"
                "\n📝 Aap check kariye:\n"
                "Koi galti ho, kuch aur chahiye, ya samajh na aaye to bataaiye — "
                "main turant theek kar dunga."
            )
            html = _call_groq(body.message, system=system).strip()
            if "```" in html:
                html = html.replace("```html", "").replace("```", "").strip()
            return {
                "service": "chat",
                "reply": "Yeh raha aapki website ka code.",
                "html": html,
                "filename": "index.html",
                "model": "saathi",
                "kind": "website",
            }
        except Exception as e:
            return {"service": "chat", "reply": f"Website banane mein problem aayi: {e}", "model": "saathi"}

    if action == "image":
        try:
            import urllib.parse as _up
            encoded = _up.quote(body.message)
            image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024"
            return {
                "service": "chat",
                "reply": "Yeh rahi aapki image.",
                "image_url": image_url,
                "model": "saathi",
                "kind": "image",
            }
        except Exception as e:
            return {"service": "chat", "reply": f"Image banane mein problem aayi: {e}", "model": "saathi"}

    # Warna normal text chat
    result = get_response(body.message)
    if isinstance(result, dict):
        return {
            "service": "chat",
            "reply": result.get("reply"),
            "sources": result.get("sources", []),
            "model": "saathi"
        }
    return {
        "service": "chat",
        "reply": result,
        "model": "saathi"
    }


import os as _os
import requests as _requests
from dotenv import load_dotenv as _load_dotenv

_load_dotenv()

def _call_groq(prompt: str, system: str = "") -> str:
    """Groq se reply laata hai. Poora output deta hai, fallback OpenRouter se."""
    key = _os.environ.get("GROQ_API_KEY")
    if not key:
        try:
            return _call_openrouter(prompt, system)
        except Exception:
            raise HTTPException(503, "GROQ_API_KEY set nahi hai")
    try:
        r = _requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": (
                    ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]
                ),
                "max_tokens": 8000,
                "temperature": 0.6,
            },
            timeout=300,
        )
        if r.status_code != 200:
            print(f"[groq] HTTP {r.status_code}, OpenRouter fallback")
            return _call_openrouter(prompt, system)
        data = r.json()
        content = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        finish = data.get("choices", [{}])[0].get("finish_reason", "")
        if finish == "length" or (content and not content.rstrip().endswith((">", "}", ")", "]", ".", "!", "?", "`"))):
            print(f"[groq] Response cut ho gaya (finish={finish}), OpenRouter try")
            try:
                alt = _call_openrouter(prompt, system)
                if alt and len(alt) > len(content):
                    return alt
            except Exception:
                pass
        return content
    except HTTPException:
        raise
    except Exception as e:
        try:
            return _call_openrouter(prompt, system)
        except Exception:
            raise HTTPException(500, f"Groq crash: {e}")


def _call_openrouter(prompt: str, system: str = "") -> str:
    """OpenRouter se reply laata hai (fallback ke liye)."""
    key = _os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise HTTPException(503, "OPENROUTER_API_KEY set nahi hai")
    try:
        r = _requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openrouter/free",
                "messages": (
                    ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]
                ),
                "max_tokens": 8000,
            },
            timeout=300,
        )
        if r.status_code != 200:
            raise HTTPException(500, f"OpenRouter error: {r.status_code}")
        return (r.json().get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"OpenRouter crash: {e}")


@app.post("/v1/image")
def image(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "image")
    import urllib.parse
    prompt = (body.prompt or "").strip()
    if not prompt:
        raise HTTPException(400, "Prompt khaali nahi ho sakta")
    width = body.width or 1024
    height = body.height or 1024
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )
    return {
        "service": "image",
        "image_url": image_url,
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": "saathi-image"
    }

@app.post("/v1/video")
def video(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "video")
    raise HTTPException(501, "Video model/provider अभी connect नहीं है")

@app.post("/v1/voice")
def voice(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "voice")
    raise HTTPException(501, "Voice model/provider अभी connect नहीं है")

@app.post("/v1/pdf")
def pdf(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "pdf")
    import base64
    from io import BytesIO
    from xhtml2pdf import pisa

    system = (
        "Tum ek professional document writer ho. User ki request ke hisab se "
        "ek achha HTML document banao (title, headings, paragraphs). "
        "Sirf pure HTML return karo — <html> se shuru, </html> par khatam. "
        "Sirf HTML content, koi CSS, koi markdown, koi explanation nahi."
    )
    html_body = _call_groq(body.prompt, system=system)
    html_body = html_body.strip()
    if "```" in html_body:
        html_body = html_body.replace("```html", "").replace("```", "").strip()

    full_html = "<html><head><meta charset=\'utf-8\'></head><body>" + html_body + "</body></html>"

    pdf_buffer = BytesIO()
    pisa.CreatePDF(full_html, dest=pdf_buffer, encoding="utf-8")
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    return {
        "pdf_base64": pdf_b64,
        "filename": "saathi.pdf",
    }

@app.post("/v1/code")
def code(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "code")
    raise HTTPException(501, "Coding model अभी connect नहीं है")

@app.post("/v1/website")
def website(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "website")
    system = (
                "Tum ek expert full-stack web developer ho. User ki request ke hisab se ek "
                "COMPLETE, FULLY WORKING HTML website banao (HTML + inline CSS + JS). "
                "Sirf pure HTML code return karo, koi explanation nahi, koi markdown nahi. "
                "Shuru <!DOCTYPE html> se, khatam </html> par.\n"
                "ZAROORI RULES:\n"
                "1. IMAGES: Sirf picsum.photos ya placehold.co use karo. source.unsplash.com KABHI NAHI (band hai).\n"
                "2. HAR BUTTON KAAM KARE: nav links smooth scroll, Get Started contact pe, hamburger JS toggle.\n"
                "3. IMAGE UPLOAD: input type=file with preview.\n"
                "4. EDIT: headings pe contenteditable=true, Edit button.\n"
                "5. ADD/DELETE: Add Item button, har item pe delete button.\n"
                "6. FORM: submit pe alert + reset.\n"
                "7. SMOOTH SCROLL: html{scroll-behavior:smooth}.\n"
                "8. HOVER EFFECTS: har button aur card pe.\n"
                "9. MOBILE RESPONSIVE: media queries.\n"
                "10. CSS VARIABLES colors ke liye.\n"
                "11. Koi button dead nahi — har click pe action.\n"
                "\n📋 CHANGES / क्या किया (code ke neeche likho):\n"
                "- [Kya-kya banaya/badla — list mein]\n"
                "\n✅ FEATURES ADD KIYE:\n"
                "- [Naye features]\n"
                "\n📝 Aap check kariye:\n"
                "Koi galti ho, kuch aur chahiye, ya samajh na aaye to bataaiye — "
                "main turant theek kar dunga."
        "user ki request ke hisab se daalo."
    )
    html = _call_groq(body.prompt, system=system)
    html = html.strip()
    if "```" in html:
        html = html.replace("```html", "").replace("```", "").strip()
    return {"html": html, "filename": "index.html"}
