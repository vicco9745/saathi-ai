THIS_IS_A_DELIBERATE_ERROR_TO_TEST
"""
Saathi AI Backend
==================

Yeh backend aapki index.html (frontend) ke saath kaam karta hai.
Abhi isme yeh features hain:

1. /v1/chat      -> Chat ka jawab deta hai. Agar "allow_web_search" true hai
                    aur AI ko jawab nahi pata, toh DuckDuckGo se search karke
                    jawab banata hai (free, koi API key nahi chahiye).
2. /v1/image     -> Abhi tak koi real image-generation AI connect nahi hai.
3. /v1/website   -> Ready hai.
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
VALID_API_KEY = os.environ.get("SAATHI_API_KEY", "test-key-123")

def check_api_key(x_api_key: Optional[str]):
    if not x_api_key or x_api_key.strip() != VALID_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API key invalid ya missing hai."
        )

# ── Request models ────────────────────────────────────────────────────────
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

# ── Free web search: DuckDuckGo ──────────────────────────────────────────
def search_duckduckgo(query: str):
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

        answer = data.get("Answer") or data.get("AbstractText")
        if answer:
            return answer.strip(), sources

        for item in related:
            if isinstance(item, dict) and item.get("Text"):
                return item["Text"].strip(), sources

        return None, sources
    except Exception:
        return None, []

# ── Free News API — Google News RSS ──────────────────────────────────────
def fetch_news(query: str = None, lang: str = "hi", country: str = "IN"):
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

# ── LLM placeholder ──────────────────────────────────────────────────────
def generate_reply_from_llm(message: str, memory: List[str], search_context: Optional[str]) -> str:
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

# ── Endpoints ────────────────────────────────────────────────────────────
@app.post("/v1/chat")
def chat(req: ChatRequest, x_api_key: Optional[str] = Header(None)):
    

    search_context = None
    sources = []
    msg_lower = (req.message or "").lower()

    # News detection
    news_keywords = [
        "news", "khabar", "khabrein", "samachar", "samachaar",
        "आज की खबर", "आज की ख़बर", "ताज़ा खबर", "ताजा खबर", "समाचार", "न्यूज़", "न्यूज",
        "latest news", "breaking news", "live news", "headlines",
        "aaj ki", "taja", "taaza"
    ]
    is_news_request = any(kw in msg_lower for kw in news_keywords)
    
    if is_news_request:
        dev_count = sum(1 for c in req.message if '\u0900' <= c <= '\u097F')
        news_lang = "hi" if dev_count > 3 else "en"
        topic = None
        for t in ["cricket", "bollywood", "politics", "sports", "business", "technology", "world"]:
            if t in msg_lower:
                topic = t
                break
        news_text, news_sources = fetch_news(query=topic, lang=news_lang)
        if news_text:
            search_context = news_text
            sources = news_sources
    elif req.allow_web_search:
        search_context, sources = search_duckduckgo(req.message)

    # 🚨 NAYA SMART SYSTEM PROMPT 🚨
    system = (
        "Aap Saathi-AI hain. Aapko hamesha ek bahut hi sharif aur madadgar insaan ki tarah baat karni hai. "
        "Jab bhi user koi website ya code maange, to aapko sabse pehle ek naya aur pyara message likhna hai (jaise: 'Ji bilkul! Maine aapke liye yeh taiyar kar diya hai. Maine ise check kar liya hai.'). "
        "Uske baad aapko poora code HTML format mein dena hai, taaki website use card ke roop mein dikha sake. "
    )
