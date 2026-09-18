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

class ChatRequest(BaseModel):
    message: str
    model: str = "auto"

class GenericRequest(BaseModel):
    prompt: str

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

@app.post("/v1/chat")
def chat(body: ChatRequest, key=Depends(require_api_key)):
    record_usage(key, "chat")
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

@app.post("/v1/image")
def image(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "image")
    raise HTTPException(501, "Image model/provider अभी connect नहीं है")

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
    raise HTTPException(501, "PDF generator अभी connect नहीं है")

@app.post("/v1/code")
def code(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "code")
    raise HTTPException(501, "Coding model अभी connect नहीं है")

@app.post("/v1/website")
def website(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "website")
    raise HTTPException(501, "Website builder अभी connect नहीं है")
