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
    if not key:
        return "GROQ_API_KEY set nahi hai."
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
        if r.status_code != 200:
            return f"Groq error: {r.status_code} - {r.text}"
        data = r.json()
        return (data["choices"][0]["message"]["content"] or "").strip()
    except Exception as e:
        return f"Crash: {e}"

class ChatRequest(BaseModel):
    message: str

@app.post("/v1/chat")
def chat(req: ChatRequest, x_api_key: Optional[str] = Header(None)):
    system = (
        "Aap Saathi-AI hain. Aapko ek bahut hi sharif aur samajhdar insaan ki tarah baat karni hai. "
        "SABSE ZAROORI NIYAM: Jab bhi aap koi Heading dein (jaise 'Pehla Adhyay', 'Shuruaat', 'Ant'), toh use HAMESHA double star (**Heading**) ke beech mein likhein. "
        "Har heading ke baad ek khali line (\\n\\n) chhodein. "
        "Baaki normal text ko bilkul saaf aur bina kisi markdown ke likhein (jaise bina kisi star ke). "
        "Sirf headings ke liye star ka istemal karein."
    )
    reply = call_groq(req.message, system=system)
    return {"reply": reply}

@app.get("/")
def health():
    return {"status": "Saathi backend chal raha hai"}
