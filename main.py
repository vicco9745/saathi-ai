"""
Saathi AI Backend
==================

Yeh backend aapki index.html (frontend) ke saath kaam karta hai.
Abhi isme yeh features hain:

1. /v1/chat      -> Chat ka jawab deta hai. Agar "allow_web_search" true hai
                    aur AI ko jawab nahi pata, toh DuckDuckGo se search karke
                    jawab banata hai (free, koi API key nahi chahiye).
2. /v1/image     -> Abhi tak koi real image-generation AI connect nahi hai.
                    Ready hai, bas API key/provider daalna hai (neeche dekhein).
3. /v1/website   -> Abhi tak koi real LLM connect nahi hai. Ready hai.
4. /v1/video     -> Abhi tak koi real video-generation AI connect nahi hai.

IMPORTANT — jab bhi aap koi LLM (Gemini/OpenAI/Claude) connect karna chahein,
neeche "generate_reply_from_llm()" function mein bas woh call daal dena hai —
baaki sab structure taiyar hai.
"""

import os
import re
import requests
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Saathi AI Backend")

# CORS khula rakha hai kyunki frontend ek local HTML file (WebView) se chalta hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API KEY ──────────────────────────────────────────────────────────────
# Render.com par Environment Variable "SAATHI_API_KEY" set karna.
# Agar set nahi hai, toh yeh default sirf testing ke liye hai — production
# mein hamesha environment variable use karna, isko hardcode mat rakhna.
VALID_API_KEY = os.environ.get("SAATHI_API_KEY", "test-key-123")


def check_api_key(x_api_key: Optional[str]):
    if not x_api_key or x_api_key.strip() != VALID_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API key invalid ya missing hai."
        )


# ── Request models (frontend jo bhejta hai, uska shape) ────────────────
class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "Default"
    memory: Optional[List[str]] = []
    allow_web_search: Optional[bool] = False


class ImageRequest(BaseModel):
    prompt: str
    model: Optional[str] = "Default"


class WebsiteRequest(BaseModel):
    prompt: str
    model: Optional[str] = "Default"


class VideoRequest(BaseModel):
    prompt: str
    model: Optional[str] = "Default"
    include_voice: Optional[bool] = False
    voice_lang: Optional[str] = "hi-IN"


class PdfRequest(BaseModel):
    prompt: str
    model: Optional[str] = "Default"


# ── Free web search: DuckDuckGo Instant Answer API (no API key needed) ──
def search_duckduckgo(query: str):
    """
    DuckDuckGo ka free Instant Answer API use karta hai.
    Yeh factual/simple sawalon ke liye kaam karta hai (jaise "capital of X",
    "who is Y", etc). Complex/current-events sawalon ke liye itna bharosemand
    nahi hai — aage chal kar Google/Bing Search API se upgrade kiya ja sakta hai.

    Return karta hai: (answer_text, sources_list). sources_list mein har item
    {"title": ..., "url": ...} hota hai — yeh frontend ke "Sources" button
    mein dikhta hai.
    """
    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=6,
        )
        resp.raise_for_status()
        data = resp.json()

        sources = []
        abstract_url = data.get("AbstractURL")
        abstract_source = data.get("AbstractSource") or "Source"
        if abstract_url:
            sources.append({"title": abstract_source, "url": abstract_url})

        related = data.get("RelatedTopics") or []
        for item in related:
            if isinstance(item, dict) and item.get("FirstURL"):
                sources.append({
                    "title": (item.get("Text") or item["FirstURL"])[:80],
                    "url": item["FirstURL"],
                })
            if len(sources) >= 10:
                break

        # DuckDuckGo kabhi seedha answer deta hai, kabhi abstract text
        answer = data.get("Answer") or data.get("AbstractText")
        if answer:
            return answer.strip(), sources

        for item in related:
            if isinstance(item, dict) and item.get("Text"):
                return item["Text"].strip(), sources

        return None, sources
    except Exception:
        return None, []


# ── Free News API — Google News RSS (no API key needed) ───────────────
def fetch_news(query: str = None, lang: str = "hi", country: str = "IN"):
    """
    Google News RSS se latest khabar laata hai.
    - query: khaas topic (jaise "cricket", "bollywood", "delhi")
    - lang: "hi" (Hindi) ya "en" (English)
    - country: "IN" (India) ya "US", "GB", etc.

    Return: (news_text, sources_list)
    """
    import xml.etree.ElementTree as ET
    try:
        if query:
            url = f"https://news.google.com/rss/search?q={query}&hl={lang}&gl={country}&ceid={country}:{lang}"
        else:
            url = f"https://news.google.com/rss?hl={lang}&gl={country}&ceid={country}:{lang}"

        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        items = root.findall(".//item")

        if not items:
            return None, []

        sources = []
        news_lines = []
        for i, item in enumerate(items[:7]):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            pub_date = item.findtext("pubDate", "").strip()
            if title:
                news_lines.append(f"{i+1}. {title}")
                sources.append({"title": title[:80], "url": link})

        if news_lines:
            header = "आज की ताज़ा खबरें:" if lang == "hi" else "Latest News:"
            return header + "\n\n" + "\n".join(news_lines), sources

        return None, []

    except Exception as e:
        print(f"[news] CRASHED: {e}")
        return None, []


# ── LLM placeholder — jab aap LLM connect karo, isme call daal dena ─────
def generate_reply_from_llm(message: str, memory: List[str], search_context: Optional[str]) -> str:
    """
    Abhi yahan koi real LLM (Gemini/OpenAI/Claude) connect nahi hai.
    Jab connect karna ho, is function ke andar apne LLM provider ka
    API call daal dena — memory aur search_context ko prompt/system-message
    mein context ki tarah bhej dena.

    Filhaal, agar search se kuch mila hai toh wahi seedha jawab ki tarah
    de diya jata hai (bina LLM ke bhi kaam chalta rahe, isliye).
    """
    if search_context:
        return search_context

    memory_note = ""
    if memory:
        memory_note = " (Yaad rakhi gayi baatein: " + "; ".join(memory) + ")"

    return (
        "Abhi tak koi AI model (LLM) connect nahi hai backend mein, "
        "isliye main sirf itna bata sakta hoon ki tumne kaha: \"" + message + "\"."
        + memory_note
    )


# ── Endpoints ─────────────────────────────────────────────────────────
@app.post("/v1/chat")
def chat(req: ChatRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)

    search_context = None
    sources = []
    msg_lower = (req.message or "").lower()

    # News detection — kya user news maang raha hai?
    news_keywords = [
        "news", "khabar", "khabrein", "samachar", "samachaar",
        "आज की खबर", "आज की ख़बर", "ताज़ा खबर", "ताजा खबर", "समाचार", "न्यूज़", "न्यूज",
        "latest news", "breaking news", "live news", "headlines",
        "aaj ki", "taja", "taaza"
    ]
    is_news_request = any(kw in msg_lower for kw in news_keywords)

    if is_news_request:
        # Language detect
        dev_count = sum(1 for c in req.message if '\u0900' <= c <= '\u097F')
        news_lang = "hi" if dev_count > 3 else "en"
        # Topic detect (agar user ne koi topic bola ho)
        topic = None
        for t in ["cricket", "bollywood", "politics", "sports", "business", "technology", "world"]:
            if t in msg_lower:
                topic = t
                break
        print(f"[NEWS-DEBUG] is_news_request=True, topic={topic}, lang={news_lang}")
        news_text, news_sources = fetch_news(query=topic, lang=news_lang)
        print(f"[NEWS-DEBUG] news_text={'MILA (' + str(len(news_text)) + ' chars)' if news_text else 'NAHI MILA (None)'}")
        if news_text:
            search_context = news_text
            sources = news_sources

    elif req.allow_web_search:
        search_context, sources = search_duckduckgo(req.message)

    system = (
        "Tum Saathi ho - ek friendly, helpful AI assistant. "
        "Hindi/Hinglish mein natural baat karo. "
        "Agar user kahani, kavita, ya creative cheez maange to KHUD se likho, "
        "web search ka result use mat karo. "
        "Sirf facts, news, ya current info ke liye diya gaya context use karo. "
        "Agar news context diya gaya hai, to usse achchhe se Hindi mein summary bana kar do — "
        "har khabar ka chhota point do, aur sources bhi mention karo."
    )
    if search_context:
        system += "\n\nContext:\n" + search_context

    try:
        reply = call_groq(req.message, system=system)
    except Exception:
        if search_context:
            reply = search_context
        else:
            reply = "Sorry, abhi AI se connect nahi ho pa raha."

    response = {"reply": reply}
    if sources:
        response["sources"] = sources
    return response




def call_groq(prompt: str, system: str = "") -> str:
    """Groq API se reply laata hai."""
    import os as _os
    key = _os.environ.get("GROQ_API_KEY")
    if not key:
        raise HTTPException(status_code=503, detail="GROQ_API_KEY set nahi hai")
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-120b",
                "messages": (
                    ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]
                ),
            },
            timeout=60,
        )
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Groq error: {r.status_code}")
        data = r.json()
        return (data["choices"][0]["message"]["content"] or "").strip()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq crash: {e}")


@app.post("/v1/image")
def generate_image(req: ImageRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    # TODO: Yahan kisi image-generation API (Stability AI / DALL-E / Gemini
    # Image) ka call daalna hai jab woh ready ho.
    raise HTTPException(
        status_code=503,
        detail="Image generation abhi backend mein connect nahi hai. Koi image-gen API jodni hogi."
    )


@app.post("/v1/website")
def generate_website(req: WebsiteRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    system = (
        "Tum ek expert web developer ho. User ki request ke hisab se ek "
        "COMPLETE, ready-to-use HTML file banao (HTML + inline CSS + JS). "
        "Sirf pure HTML code return karo, koi explanation nahi, koi markdown "
        "code-fence nahi (``` nahi). Shuru <!DOCTYPE html> se aur khatam "
        "</html> par. Design modern, responsive aur sundar rakho. "
        "Hindi/English content user ki request ke hisab se daalo."
    )
    html = call_groq(req.prompt, system=system)
    # Agar model ne ```html fence lagaya to hata do
    html = html.strip()
    if html.startswith("```"):
        html = html.split("\n", 1)[1] if "\n" in html else html
        if html.endswith("```"):
            html = html[:-3]
        html = html.strip()
    if "```" in html:
        html = html.replace("```html", "").replace("```", "").strip()
    return {"html": html, "filename": "index.html" }


@app.post("/v1/video")
def generate_video(req: VideoRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    # TODO: Yahan kisi video-generation API (Runway / Pika / Google Veo)
    # ka call daalna hai jab woh ready ho.
    raise HTTPException(
        status_code=503,
        detail="Video generation abhi backend mein connect nahi hai. Koi video-gen API jodni hogi."
    )


@app.post("/v1/pdf")
def generate_pdf(req: PdfRequest, x_api_key: Optional[str] = Header(None)):
    check_api_key(x_api_key)
    # TODO: Professional-dikhne-wala PDF banane ke liye yeh tarika achha rahega:
    #   1. LLM se prompt ke content ka HTML+CSS banwao (headings, colors, icons,
    #      layout — jaisa reference design mein tha)
    #   2. Us HTML ko WeasyPrint (pip install weasyprint) se PDF mein convert karo:
    #        from weasyprint import HTML
    #        pdf_bytes = HTML(string=html_content).write_pdf()
    #   3. pdf_bytes ko base64 karke "pdf_base64" field mein bhej do
    # Filhaal koi LLM/PDF-render library connect nahi hai, isliye abhi error.
    raise HTTPException(
        status_code=503,
        detail="PDF generation abhi backend mein connect nahi hai. LLM + WeasyPrint jaisi library jodni hogi."
    )


@app.get("/")
def health():
    return {"status": "Saathi backend chal raha hai"}
