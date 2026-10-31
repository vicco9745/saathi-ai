import os
import requests
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def call_groq(prompt: str, system: str = "") -> str:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key: return "GROQ_API_KEY set nahi hai."
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": (
                    ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]
                ),
            },
            timeout=60,
        )
        return r.json()["choices"][0]["message"]["content"].strip() if r.status_code == 200 else f"Groq error: {r.status_code}"
    except Exception as e: return f"Crash: {e}"

class ChatRequest(BaseModel):
    message: str
    image: Optional[str] = None

@app.post("/v1/chat")
def chat(req: ChatRequest, x_api_key: Optional[str] = Header(None)):
    system = (
        "Aap Saathi-AI hain. Aapko hamesha ek bahut hi sharif aur samajhdar insaan ki tarah baat karni hai. "
        "SABSE ZAROORI NIYAM: Jab bhi aap koi Heading dein, toh use HAMESHA double star (**Heading**) ke beech mein likhein. "
        "Har heading ke baad ek khali line (\\n\\n) chhodein. Baaki normal text ko bilkul saaf likhein."
    )
    
    if req.image:
        g_key = os.environ.get("GEMINI_API_KEY")
        if not g_key:
            return {"reply": "Google Key (GEMINI_API_KEY) set nahi hai. Kripya Render par key add karein."}
        
        try:
            # Base64 से 'data:image/jpeg;base64,' हटाएँ
            b64_data = req.image.split(",")[1] if "," in req.image else req.image
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": f"{system}\n\nUser ka sawal: {req.message}"},
                        {"inline_data": {"mime_type": "image/jpeg", "data": b64_data}}
                    ]
                }]
            }
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={g_key}",
                headers={"Content-Type": "application/json"},
                json=payload, timeout=120
            )
            if r.status_code == 200:
                reply = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                return {"reply": reply}
            else:
                return {"reply": f"Google AI Error: {r.status_code} - {r.text}"}
        except Exception as e:
            return {"reply": f"Google AI Crash: {e}"}

    reply = call_groq(req.message, system=system)
    return {"reply": reply}

@app.get("/")
def health(): return {"status": "Saathi backend chal raha hai"}
