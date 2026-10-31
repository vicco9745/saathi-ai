import os
import requests
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def call_groq(prompt: str, system: str = "", image_b64: str = None) -> str:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key: return "GROQ_API_KEY set nahi hai."
    
    try:
        # अगर इमेज है, तो मल्टीमॉडल (Vision) मॉडल इस्तेमाल करें
        if image_b64:
            model = "qwen/qwen3.8-27b" # यह Groq का इमेज पढ़ने वाला मॉडल है
            content = [
                {"type": "text", "text": f"{system}\n\nUser: {prompt}"},
                {"type": "image_url", "image_url": {"url": image_b64}}
            ]
        else:
            model = "openai/gpt-oss-20b" # टेक्स्ट के लिए तेज़ मॉडल
            content = f"{system}\n\nUser: {prompt}"

        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": content}],
                "max_completion_tokens": 1024,
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
    image: Optional[str] = None # Base64 image

@app.post("/v1/chat")
def chat(req: ChatRequest, x_api_key: Optional[str] = Header(None)):
    system = (
        "Aap Saathi-AI hain. Aapko hamesha ek bahut hi sharif aur samajhdar insaan ki tarah baat karni hai. "
        "SABSE ZAROORI NIYAM: Jab bhi aap koi Heading dein, toh use HAMESHA double star (**Heading**) ke beech mein likhein. "
        "Har heading ke baad ek khali line (\\n\\n) chhodein. Baaki normal text ko bilkul saaf likhein."
    )
    
    # image_b64 में 'data:image/jpeg;base64,' वाला हिस्सा भी होना चाहिए
    reply = call_groq(req.message, system=system, image_b64=req.image)
    return {"reply": reply}

@app.get("/")
def health(): return {"status": "Saathi backend chal raha hai"}
