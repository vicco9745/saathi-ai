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
    system = "Aap Saathi-AI hain. Kripya apne jawab mein kisi bhi tarah ka Markdown (jaise **, *, #, |, ---) bilkul use NAHI karna. Sirf saaf-suthre normal paragraphs mein likho."
    reply = call_groq(req.message, system=system)
    return {"reply": reply}

@app.get("/")
def health():
    return {"status": "Saathi backend chal raha hai"}
