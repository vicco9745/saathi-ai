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

    # Pehle yahan ek "guess karo ki search chahiye ya nahi" wala heuristic
    # tha, jo bahut zyada baar (har normal message par) search shuru kar
    # deta tha — isse user ko baar baar galat/random results milte the.
    # Ab search SIRF tabhi hoti hai jab frontend khud "/search ..." command
    # se explicitly allow_web_search=true bhejta hai — koi guessing nahi.
    search_context = None
    sources = []
    if req.allow_web_search:
        search_context, sources = search_duckduckgo(req.message)

    reply = generate_reply_from_llm(req.message, req.memory or [], search_context)

    response = {"reply": reply}
    if sources:
        response["sources"] = sources
    return response


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
    # TODO: Yahan LLM se HTML code generate karwana hai jab LLM ready ho.
    raise HTTPException(
        status_code=503,
        detail="Website generation abhi backend mein connect nahi hai. Koi LLM jodni hogi."
    )


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
