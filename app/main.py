import os
import requests as _req
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .db import init_db
from .auth import require_api_key, record_usage
from ichat_ai.response_engine import get_response
from ichat_ai.code_fix import fix_code_blocks

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
    history: Optional[List[dict]] = []
    lang_pref: Optional[str] = None
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
    "Agar koi pooche 'tumhe kisne banaya' to bolna: 'Mujhe Vikas ne banaya hai.'\n\n"
    "=== BHASHA KA RULE (SABSE ZAROORI) ===\n"
    "1. User JIS bhasha mein likhe, USI bhasha mein jawab do.\n"
    "2. 'English mein jawab do' -> SIRF ENGLISH.\n"
    "3. 'Hindi mein jawab do' -> SIRF HINDI (Devanagari).\n"
    "4. Hindi likhe -> Hindi. Hinglish likhe -> Hindi. English likhe -> English.\n"
    "5. Chinese->Chinese, Tamil->Tamil. Har bhasha ka respect karo.\n"
    "6. KABHI user ki bhasha mat badlo. Jawab chhota aur saaf rakho.\n\n"
    "=== QUALITY RULES (SABSE ZAROORI) ===\n"
    "1. SAHI LIPI: Hindi->शुद्ध देवनागरी. English->proper spelling.\n"
    "2. NATURAL likho: 'यह एक HTML फाइल है जिसका आकार 385 KB है।' (machine translation jaisa nahi).\n"
    "3. POORE VAKYA likho: aadhe-adhoore nahi, sahi punctuation (. , ? !) use karo.\n"
    "4. Technical shabd (HTML, PDF, CSS, API, URL) as-is rakho, baaki Hindi mein.\n"
    "5. Emoji ke baad space do: 'अच्छा 👍 ठीक'\n"
    "6. Headings ke liye DEFAULT mein **bold** aur emoji use karo (jaise **📄 File Type**). ## ya ### sirf tab use karo jab user saaf bole. Lists ke liye - ya 1. use karo.\n"
    "7. Poora jawab do — beech se mat todo, adhoora mat chhodo.\n"
    "8. Detail chahiye to saaf likho, chhota chahiye to seedha point par.\n"
    "9. User ki bhasha mein headings bhi likho: 'फाइल का प्रकार', 'क्या-क्या है', 'अच्छी बातें', 'कमियाँ', 'सुधार', 'रेटिंग'.\n"
    "10. Emojis use karo headings mein (📄 📋 ✅ ⚠️ 🔧 🌟) jaisi reference mein thi."
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

_ACTION_HINT = {}
_FOREIGN_WORDS = {
    "para", "pero", "quiero", "crea", "crear", "hazme", "puedes", "una", "los", "las", "del", "sitio",
    "pour", "une", "les", "des", "je", "mon", "fais", "peux",
    "und", "ich", "ein", "eine", "mit", "bitte", "erstelle", "mach", "webseite",
    "crie", "fazer", "fammi", "sito", "per", "con", "che",
    "yang", "dan", "untuk", "buatkan", "tolong", "saya", "bisa", "situs",
    "bir", "bana", "een", "het", "voor", "maak", "mij", "dla", "gumawa", "paki",
}
_INTENT_SYSTEM = (
    "You are an intent classifier. The user message can be in ANY language. "
    "Decide if the user is asking you RIGHT NOW to create (a) a WEBSITE / web page / landing page, "
    "or (b) an IMAGE / picture / photo / drawing / illustration. "
    "Questions about websites or images, or anything else, are NONE. "
    "Reply with exactly one line and nothing else: 'website' or "
    "'image|<one detailed English description of the picture to generate>' or 'none'."
)


def _needs_lang_check(msg):
    m = (msg or "").strip()
    if not m or len(m) > 600:
        return False
    for ch in m:
        if ord(ch) > 127 and ch.isalpha() and not ("\u0900" <= ch <= "\u097f"):
            return True
    import re as _re2
    words = set(_re2.findall(r"[a-z]+", m.lower()))
    return bool(words & _FOREIGN_WORDS)


def _detect_action(msg: str) -> str:
    base = _detect_action_base(msg)
    if base in ("analyze", "pdf", "website", "image"):
        return base
    try:
        if _needs_lang_check(msg):
            out = _call_groq(msg.strip()[:600], system=_INTENT_SYSTEM).strip().strip("`'\" ").lower()
            if out.startswith("website"):
                return "website"
            if out.startswith("image"):
                hint = out.split("|", 1)[1].strip() if "|" in out else ""
                if hint:
                    if len(_ACTION_HINT) > 200:
                        _ACTION_HINT.clear()
                    _ACTION_HINT[msg] = hint
                return "image"
    except Exception:
        pass
    return base


def _detect_action_base(msg: str) -> str:
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
    # ═══ Kahani / Story / Poem ═══
    if any(x in m for x in ["kahani","कहानी","story","किस्सा","कविता","poem","शायरी","baal","baat","बात","joke","चुटकुला"]):
        return "chat"
    return "chat"


@app.post("/v1/chat")
def chat(body: ChatRequest, key=Depends(require_api_key)):
    record_usage(key, "chat")

    # Agar user ne image bheji hai to vision path use karo
    images = [a for a in (body.attachments or []) if a.kind == "photo" and a.dataUrl]

    if images:
        raw = _call_vision_v2(body.message, images)
        raw = __import__("re").sub(r"[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]+", "", raw)
        reply = __import__("re").sub(r"[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]+", "", _polish_vision_reply(raw, body.message))
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
            encoded = _up.quote(_ACTION_HINT.pop(body.message, None) or body.message)
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
    try:
        result = get_response(body.message, history=body.history or [], lang_pref=body.lang_pref)
    except TypeError:
        try:
            result = get_response(body.message, history=body.history or [])
        except TypeError:
            result = get_response(body.message)
    if isinstance(result, dict):
        return {
            "service": "chat",
            "reply": fix_code_blocks(result.get("reply") or ""),
            "sources": result.get("sources", []),
            "model": "saathi"
        }
    return {
        "service": "chat",
        "reply": fix_code_blocks(result if isinstance(result, str) else str(result)),
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
                "max_tokens": 32000,
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
                "max_tokens": 32000,
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

VISION_SYSTEM_INSTRUCTION = (
    "Tum Saathi ho — ek insaan jaisa madadgaar saathi. User ne tumhe kuch bheja hai "
    "(photo, video, file, kuch bhi). Tumhara kaam hai usse DEKHNA, SAMJHNA, aur "
    "insaan ki tarah jawab dena.\n\n"
    "═══ SABSE PEHLA NIYAM ═══\n"
    "KABHI MAT KEHNA: 'file mil gayi', 'photo mil gayi', 'video mil gaya', "
    "'attachment mila', 'yeh ek photo hai'. User ko pata hai usne kya bheja. "
    "Use batao ki us cheez ke ANDAR kya hai.\n\n"
    "═══ JAWAB KA DHANCHA — 4 HISSE, IS KARM MEIN ═══\n\n"
    "◆ HISSA 1 — VIVARAN (kya-kya hai, kahan-kahan)\n"
    "Jo bhi bheja gaya hai uska POORA bayaan do. Jaise koi insaan aankhon ke saamne "
    "rakh kar gin raha ho:\n"
    "- Photo ho to: kya dikh raha hai, upar kya likha hai, neeche kya, beech mein kya, "
    "rang kaise hain, text padh kar do, button/icon/box/chart — jo bhi dikh raha hai "
    "uska naam lekar batao. Kahan hai yeh bhi batao — 'upar dayein taraf', 'beech mein', "
    "'neeche bayen'.\n"
    "- Video ho to: kitna lamba hai, kya-kya dikha, kya bola gaya, shuru se ant tak kram mein.\n"
    "- File/PDF ho to: kitne panne, har panne par kya, sheershak kya.\n"
    "Chhota-sa vivaran kaafi nahi. Poora kholkar batao — user ko lage ki tumne sach mein "
    "usse dekha hai, dhyaan se dekha hai.\n\n"
    "◆ HISSA 2 — KAAM (yeh kis kaam ki hai)\n"
    "Ab batao yeh cheez asal mein kis kaam aati hai, kahan istemal hoti hai, kyun bani "
    "hoti hai. Jaise: 'Yeh chart trading mein kaam aata hai — isse pata chalta hai ki "
    "sone ka bhaav upar jayega ya neeche. Log ise dekh kar tay karte hain ki kharidna "
    "hai ya bechna hai.'\n\n"
    "◆ HISSA 3 — SALAH (achha hai ya bura)\n"
    "Yahan imaandaar bano — dost ki tarah.\n"
    "- Achhi cheez ho to: 'Yeh aapke kaam ki cheez hai, ise sambhal kar rakhiye.'\n"
    "- Koi khatra, dhokha, galat baat ho to: 'Dhyaan dijiye — isse door rahiye.'\n"
    "- Koi kami ya galti ho to: 'Ismein ek baat sudhaarni chahiye — [kya].'\n"
    "Kabhi jhooti tareef mat karo. Kabhi bevajah dar mat dikhao. Jaisa dikh raha hai, "
    "waisa saaf kaho — pyaar se, par sach.\n\n"
    "◆ HISSA 4 — SAWAAL (aage kya?)\n"
    "Aakhir mein user se poochho — insaan ki tarah:\n"
    "- 'Kya aap iske baare mein kuch aur jaanna chahte hain?'\n"
    "- 'Aap isse kuch banwana chahte hain — jaise PDF, card, ya kuch aur?'\n"
    "- 'Kya main ismein kuch sudhaar kar sakta hoon?'\n"
    "Sawaal poochne ka matlab baatcheet jaari rakhna hai — user ko akela mat chhodo.\n\n"
    "═══ BHASHA KA RULE ═══\n"
    "User jis bhasha mein likhe, usi bhasha mein jawab do. Natural Hinglish/Hindi likho — "
    "'maine dekha', 'samjha', 'lagta hai', 'bataiye', 'theek hai', 'achha'. "
    "Machine translation jaise shabd MAT use karo — 'mulf fahaasat', 'pehchaan banayi', "
    "'bikau pressure', 'status' jaisi ajeeb bhasha nahi. Seedhi, aam bolchaal ki bhasha.\n\n"
    "Lambaai: jitna vishay maangta hai utna. Chhota mat karo, badha-chadha bhi mat karo.\n\n"
    "Agar user ne saath mein kuch likha hai (jaise 'iski PDF banao') to pehle upar ke "
    "chaaron hisse poore karo, PHIR jo maanga gaya kaam karo."
)


def _polish_vision_reply(vision_text: str, user_message: str) -> str:
    """Vision model ke tukde-tukde jawab ko saaf, insaan-jaisi bhasha mein likho.
    User ki bhasha detect karke usi mein likho — Hindi, English, Arabic, Tamil, jo bhi."""
    if not vision_text or not vision_text.strip():
        return vision_text

    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return vision_text

    system = (
        "Tum ek sachche aur dhyaan se padhne wale sahayak ho. Neeche ek vision AI ka raw observation hai: "
        "photo ya file mein jo likha ya dikha uska vivaran. Raw text mein shabd bigde ho sakte hain, unhe theek karo, "
        "lekin koi nayi baat apni taraf se mat jodo.\n\n"
        "═══ SABSE ZAROORI NIYAM ═══\n"
        "- Sirf wahi likho jo raw observation mein hai. Andaza ya apni taraf se jodi hui baat bilkul nahi.\n"
        "- Naam, pata, number, tareekh, ID jaisi cheezein bilkul waisi hi likho jaisi raw text mein hain. Unki vartani mat badlo aur beech mein koi anjaan akshar mat ghusao.\n"
        "- Jo saaf nahi dikha, uske baare mein seedha likho: saaf nahi dikh raha.\n"
        "- Jo cheez photo mein nahi hai, use photo ki baat bata kar mat likho.\n"
        "- Ek hi baat do baar mat likho. Bekaar ya adhoore shabd mat likho.\n\n"
        "═══ BHASHA ═══\n"
        "User jis bhasha mein likhe usi mein jawab do. Agar user ne kuch nahi likha to Hindi mein likho. Saaf, aam bolchaal ki bhasha.\n\n"
        "═══ JAWAB KA DHANCHA ═══\n"
        "Teen hisse, har ek ka chhota saaf heading (heading bhi usi bhasha mein jisme jawab likh rahe ho):\n"
        "1. Photo mein kya likha hai: mukhya baatein points mein. Photo mein jo bhi naam, pata, phone number, form number, tareekh, reference number aur ID hai, ek bhi mat chhodo.\n"
        "2. Kya sahi hai aur kya galat ya adhoora: yeh us dastavez ke baare mein batao jo photo mein hai (kya theek lagta hai, kya adhoora ya shak wala hai). Apne hi jawab ke shabdon ki vartani par tippani mat karo aur bina aadhaar galtiyan mat nikalo. Agar kuch galat nahi dikha to saaf likho. Yeh pakka mat kaho ki dastavez asli hai; sirf itna kaho ki jaanch aadhikarik jagah par karni chahiye.\n"
        "3. Kya karna chahiye: saaf salah. Jaana chahiye ya nahi, aage ke kadam kya hain, koi khatra ho to uska upay.\n\n"
        "Lambaai: jitna vishay maange utna. Koi bhumika nahi, koi bekaar line nahi."
    )

    system += ("\n\nAaj ki tareekh: " + __import__("datetime").date.today().strftime("%d %B %Y") + ". "
        "Isse pehle ki tareekh beet chuki hai; use bhavishya ki, sample ya typo mat kaho. "
        "Tareekh mein mahina aur saal poora likho. Aise shabd mat likho jinka matlab pakka na ho; seedhi aam bhasha mein likho.")

    system += (
        "\n\nRaw observation mein agar phone ki screen ke hisse (page number jaise 3/3, buttons) "
        "ya dastavez adhoora dikhne ki baat ho, use jawab mein mat likho. "
        "Raw text mein jo naam, number, saal likha hai use mat badlo aur use typo ya anuman mat kaho. "
        "Barcode ko dastavez asli hone ka saboot mat batao."
    )

    system += (
        "\n\nHisse 2 mein sirf wahi galat ya adhoora likho jo dastavez mein saaf dikhta hai, jaise kata, dhundhla ya mita hua. "
        "Agar raw text mein koi shabd ya number tumhe unclear lage, use dastavez ki galti mat kaho; use jaisa hai waisa hi likho. "
        "Date ke format, barcode ya dikhne ke dhang par tippani mat karo. Sirf Hindi, English ya Roman Hindi mein likho, koi Chinese akshar nahi. "
        "Phone number mein bindu ya colon label ka hissa hai, number ka nahi; number ko adhoora mat kaho."
    )

    user_prompt = (
        "USER KA MESSAGE:\n" + (user_message or "(kuch nahi likha, sirf file bheji)") + "\n\n"
        "VISION AI KA RAW OUTPUT (ise saaf karke dobara likho):\n" + vision_text
    )

    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 32000,
                "temperature": 0.4,
            },
            timeout=120,
        )
        if r.status_code != 200:
            return vision_text
        data = r.json()
        choices = data.get("choices") or []
        if not choices:
            return vision_text
        polished = (choices[0].get("message", {}).get("content") or "").strip()
        return polished if polished else vision_text
    except Exception:
        return vision_text


def _strip_markdown(text: str) -> str:
    """Jawab se *** , ** , ## , ### jaise markdown symbols hata do.
    Sirf saaf plain text rakho — headings, bullets, sab as-is."""
    if not text:
        return text
    import re as _r
    t = text
    # Triple asterisk/underscore
    t = _r.sub(r'\*\*\*+', '', t)
    t = _r.sub(r'___+', '', t)
    # Double asterisk / underscore (bold/italic)
    t = _r.sub(r'\*\*', '', t)
    t = _r.sub(r'(?<!\w)__(?!\w)', '', t)
    # Headings: ## ### etc — hata do hashes
    t = _r.sub(r'(?m)^\s*#{1,6}\s*', '', t)
    # Horizontal rule --- or ___
    t = _r.sub(r'(?m)^\s*[-*_]{3,}\s*$', '', t)
    # Inline code backticks
    t = t.replace('`', '')
    # Leading asterisk in bullets -> convert to bullet dot
    t = _r.sub(r'(?m)^\s*\*\s+', '• ', t)
    # Stray asterisks leftover
    t = _r.sub(r'(?<!\w)\*(?!\w)', '', t)
    # Extra blank lines
    t = _r.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


VISION_RULES = """Photo ko bahut dhyaan se padho. Niyam:
- Photo mein jo likha hai, har naam, pata, phone number, form number, tareekh (din, mahina, saal), reference number aur ID bilkul waise hi likho jaise dikh rahe hain. Andaza mat lagao, vartani mat badlo.
- Jo saaf nahi padha jaata, wahan likho: saaf nahi dikh raha.
- Phone ki screen ke hisse (status bar, battery, buttons, page number jaise 3/3, menu) dastavez ka hissa nahi hain. Unhe ignore karo.
- Dastavez adhoora ya kata hua sirf tab kaho jab photo mein saaf kata hua dikhe.
- Sirf Hindi (Devanagari), English ya Roman Hindi mein likho. Chinese, Japanese ya Korean akshar kabhi mat likho.
- Phone number ya tareekh ke aage ka bindu ya colon (jaise TEL. NO.:) label ka hissa hai, number ka nahi. Pura number likho jaisa dikh raha hai.
- Address ki line ka ek shabd do hisson mein mat todo (jaise LAMAHI ek hi shabd hai).
- Apni taraf se koi baat mat jodo."""

def _call_vision_v2(prompt: str, images: list) -> str:
    content = [{"type": "text", "text": VISION_RULES + "\n\nUSER KA SAWAAL: " + (prompt or "Is photo me kya hai? Puri detail batao.")}]
    for img in images[:3]:
        url = img.dataUrl or ""
        if not url.startswith("data:image"):
            continue
        content.append({"type": "image_url", "image_url": {"url": url}})

    errors = []
    import time as _time

    # Groq (तेज़, पर 429 आ सकता है — इसलिए 3 बार कोशिश)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        groq_models = ["qwen/qwen3.8-27b"]
        for model in groq_models:
            for attempt in range(3):
                try:
                    r = _req.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": "Bearer " + groq_key, "Content-Type": "application/json"},
                        json={"model": model, "messages": [{"role": "system", "content": SYSTEM_INSTRUCTION}, {"role": "user", "content": content}], "max_tokens": 2000},
                        timeout=120,
                    )
                    if r.status_code == 429:
                        wait = (attempt + 1) * 2
                        errors.append("groq/" + model + ": 429 (wait " + str(wait) + "s)")
                        _time.sleep(wait)
                        continue
                    if r.status_code != 200:
                        errors.append("groq/" + model + ": " + str(r.status_code))
                        break
                    data = r.json()
                    choices = data.get("choices") or []
                    if choices:
                        txt = (choices[0].get("message", {}).get("content") or "").strip()
                        if txt:
                            return txt
                    break
                except Exception as e:
                    errors.append("groq/" + model + ": " + str(e))
                    break

    # OpenRouter (भरोसेमंद फॉलबैक) — अब चालू मॉडल्स
    or_key = os.environ.get("OPENROUTER_API_KEY")
    if or_key:
        or_models = [
            "qwen/qwen3.8-27b:free",
            "google/gemma-4-31b-it:free",
            "nvidia/nemotron-nano-12b-v2-vl:free",
            "thinkingmachines/inkling-small:free",
        ]
        for model in or_models:
            try:
                r = _req.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": "Bearer " + or_key, "Content-Type": "application/json", "HTTP-Referer": "https://saathi-ai-y48j.onrender.com", "X-Title": "Saathi AI"},
                    json={"model": model, "messages": [{"role": "system", "content": SYSTEM_INSTRUCTION}, {"role": "user", "content": content}], "max_tokens": 2000},
                    timeout=120,
                )
                if r.status_code != 200:
                    errors.append("or/" + model + ": " + str(r.status_code))
                    continue
                data = r.json()
                choices = data.get("choices") or []
                if choices:
                    txt = (choices[0].get("message", {}).get("content") or "").strip()
                    if txt:
                        return txt
            except Exception as e:
                errors.append("or/" + model + ": " + str(e))

    err_text = " | ".join(errors[-6:]) if errors else "no keys"
    raise HTTPException(500, "Vision fail: " + err_text)

class TitleRequest(BaseModel):
    message: Optional[str] = ""
    image: Optional[str] = None


def _fit29(t):
    t = (t or "").strip()
    if len(t) <= 29:
        return t
    cut = t[:29]
    if " " in cut and t[29] != " ":
        cut = cut[:cut.rfind(" ")]
    return cut.strip()


def _title_from_text(text: str) -> str:
    if not text or not text.strip():
        return ""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        t = text.strip().replace("\n", " ")
        return t[:40] + ("…" if len(t) > 40 else "")
    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": "User ke message ka 25-29 akshar ka chat title banao. Sirf title likho, koi quote nahi, koi punctuation nahi. User ki bhasha mein hi rakho. Example: 'Gold chart analysis', 'Pizza recipe', 'Python bug fix', 'मौसम की जानकारी'."},
                    {"role": "user", "content": text},
                ],
                "max_tokens": 60,
                "temperature": 0.3,
            },
            timeout=30,
        )
        if r.status_code != 200:
            t = text.strip().replace("\n", " ")
            return t[:40] + ("…" if len(t) > 40 else "")
        data = r.json()
        t = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        t = t.replace("\n", " ").replace('"', '').replace("'", "").strip()
        return _fit29(t) if t else text.strip()[:40]
    except Exception:
        t = text.strip().replace("\n", " ")
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
                        {"type": "text", "text": "Is photo ka 25-29 akshar ka chat title banao. Sirf title likho, koi quote nahi. Jo bhasha user ne likha ho usme, warna Hindi/Hinglish. Example: 'Gold price chart', 'Smartphone photo', 'Restaurant menu'."},
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                    ]},
                ],
                "max_tokens": 60,
                "temperature": 0.3,
            },
            timeout=40,
        )
        if r.status_code != 200:
            return "Photo message"
        data = r.json()
        t = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        t = t.replace("\n", " ").replace('"', '').replace("'", "").strip()
        return _fit29(t) if t else "Photo message"
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
        "uska COMPLETE HTML+CSS design banao.\n\n"
        "RULES:\n"
        "1. Sirf pure HTML return karo — <!DOCTYPE html> se shuru, </html> par khatam.\n"
        "2. Sab CSS inline <style> tag mein ho — alag file nahi.\n"
        "3. Design mobile aur desktop dono par sahi dikhe — responsive.\n"
        "4. Text saaf aur bada ho — print karne layak.\n"
        "5. Sundar fonts use karo — Google Fonts ke through (link tag se).\n"
        "6. Colors, shadows, borders, gradients — sab professional ho.\n"
        "7. Agar user photo bheje to usko <img> se design mein lagao.\n"
        "8. Text user ki bhasha mein — Hindi likhe to Hindi, English likhe to English.\n"
        "9. Har cheez jo user ne kahi — naam, tareekh, jagah, rang, sab daalo.\n"
        "10. Koi markdown nahi, koi explanation nahi, sirf HTML.\n\n"
        "DIMENSION: Agar card hai to A4 ya 800x600 jaisa. Agar social post hai to square (1080x1080). "
        "Agar banner hai to wide (1200x400). User ne jo kaha uske hisab se."
    )

    prompt_text = body.prompt or ""
    if body.photo and body.photo.startswith("data:image"):
        prompt_text += "\n\n[User ki photo neeche di hai — ise design mein shamil karo: " + body.photo[:100] + "... ]"

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


@app.post("/v1/describe")
def describe_site(body: GenericRequest, key=Depends(require_api_key)):
    raw = (body.prompt or "").strip()
    if not raw:
        raise HTTPException(400, "Prompt khaali nahi ho sakta")
    req, _, html = raw.partition("=====HTML=====")
    system = (
        "You write the short message shown to a user right after their website was built. "
        "LANGUAGE: Write in the same language and script as the user's request. If the request is Hinglish "
        "(Hindi in Roman letters) or Hindi, write in Devanagari Hindi. If English, English. Any other language: that language. "
        "FORMAT (markdown): first line is a bold sentence saying the website is ready, then an em dash and the site name in italics, "
        "for example: **Your website is ready** — *Site Name*. Then a blank line, then a bold heading meaning 'What is included'. "
        "Then 5 to 8 bullet lines, each starting with '- ' in the form '- **Label** — short detail'. "
        "Then a blank line and ONE closing sentence telling the user to tap the card to preview the live site, "
        "copy or download the code, and ask for any changes. "
        "CONTENT: Mention only things that really exist in the given HTML (sections, menu links, forms, buttons, animations, "
        "responsive layout, interactive features). Do not invent features, do not mention code details, do not use emojis, "
        "do not add any other text. Keep it under 130 words."
    )
    try:
        text = _call_groq(
            "User ki request:\n" + req.strip()[:1500] + "\n\nBani hui website ka HTML:\n" + html.strip()[:6000],
            system=system,
        ).strip()
    except Exception:
        text = ""
    return {"service": "describe", "reply": text}
