# iChat API — Local Starter

यह iChat के लिए अपना API gateway/starter है। एक API key से chat, image, video, voice, PDF, code और website जैसे services को route किया जा सकता है।

## अभी क्या तैयार है
- API key generation
- Owner key को free/unlimited flag
- दूसरे users के लिए paid plan/status structure
- API-key authentication
- Usage logging
- Service routing
- Chat endpoint का demo/mock response
- बाकी services के लिए साफ placeholders
- SQLite database
- FastAPI + Uvicorn

## महत्वपूर्ण
यह gateway खुद AI model नहीं है। अगर किसी external AI provider को backend में लगाया जाएगा तो उसकी pricing/limits लागू होंगी। सच में provider-independent usage के लिए बाद में अपना/open-source model server जोड़ना होगा।

## Run
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Android terminal: source .venv/bin/activate
pip install -r requirements.txt
python seed_owner.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

API docs:
http://127.0.0.1:8000/docs

Owner key .env में OWNER_API_KEY से बनाई जा सकती है।
