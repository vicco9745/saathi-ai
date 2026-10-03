"""
ichat_ai/ai_providers.py

Gemini aur DeepSeek ko try karta hai (is order mein). Jo bhi pehle kaam
kar jaye (limit khatam na ho, error na aaye), uska jawab use hota hai.
Dono fail ho jaayen to None deta hai (response_engine.py phir web
search ya "nahi mila" wale fallback par chala jaata hai).

Keys sirf environment variables se aati hain (.env se, python-dotenv
ke zariye) — kahin bhi hardcode nahi hain.
"""

import os
import requests

SYSTEM_INSTRUCTION = (
    "Tum Saathi ho, ek AI assistant jise Vikas ne banaya hai. "
    "Hamesha khud ko sirf 'Saathi' bolna. Kabhi bhi apna asli model, "
    "company ya provider ka naam mat batana. "
    "Agar koi pooche 'tumhe kisne banaya' ya 'who made you', to hamesha "
    "bolna: 'Mujhe Vikas ne banaya hai.' "
    "\n\nSABSE ZAROORI RULE — BHASHA (LANGUAGE):\n"
    "User JIS bhasha mein likhe, tum BILKUL USI bhasha mein jawab dena. "
    "Kabhi bhi bhasha mat badalna. Ye rules follow karo:\n"
    "- User Hindi (Devanagari — अ आ इ) mein likhe -> jawab Hindi (Devanagari) mein.\n"
    "- User Hinglish (Roman Hindi — 'kaise ho') mein likhe -> jawab Devanagari Hindi mein.\n"
    "- User English mein likhe -> jawab English mein.\n"
    "- User Chinese mein likhe -> jawab Chinese mein.\n"
    "- User Tamil mein likhe -> jawab Tamil mein.\n"
    "- User Telugu mein likhe -> jawab Telugu mein.\n"
    "- User Marathi mein likhe -> jawab Marathi mein.\n"
    "- User jis bhi bhasha mein likhe, usi mein jawab.\n"
    "- Agar user bole 'Hindi mein batao' ya 'in Hindi' -> SIRF Hindi mein jawab.\n"
    "- Agar user bole 'English mein batao' -> SIRF English mein jawab.\n"
    "Kabhi Hindi wale ko English mein, ya English wale ko Hindi mein reply mat do. "
    "Jawab chhota, saaf, natural aur seedha point par rakhna."
)


def _call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.5-flash:generateContent"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        }
        resp = requests.post(
            url,
            headers={"x-goog-api-key": api_key},
            json=payload,
            timeout=20,
        )
        if resp.status_code == 429:
            print("[ai_providers/gemini] rate limit hit")
            return None
        if resp.status_code != 200:
            print(f"[ai_providers/gemini] HTTP {resp.status_code}: {resp.text[:300]}")
            return None
        data = resp.json()
        candidates = data.get("candidates") or []
        if not candidates:
            print("[ai_providers/gemini] no candidates in response")
            return None
        parts = candidates[0].get("content", {}).get("parts") or []
        text = "".join(p.get("text", "") for p in parts).strip()
        return text or None
    except Exception as e:
        print(f"[ai_providers/gemini] CRASHED: {type(e).__name__}: {e}")
        return None


def _call_deepseek(prompt):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return None
    try:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        if resp.status_code == 429:
            print("[ai_providers/deepseek] rate limit hit")
            return None
        if resp.status_code != 200:
            print(f"[ai_providers/deepseek] HTTP {resp.status_code}: {resp.text[:300]}")
            return None
        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            print("[ai_providers/deepseek] no choices in response")
            return None
        text = (choices[0].get("message", {}).get("content") or "").strip()
        return text or None
    except Exception as e:
        print(f"[ai_providers/deepseek] CRASHED: {type(e).__name__}: {e}")
        return None


def _call_groq(prompt):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "openai/gpt-oss-20b", "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": prompt},
        ]}
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            print(f"[groq] HTTP {resp.status_code}")
            return None
        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            return None
        return (choices[0].get("message", {}).get("content") or "").strip() or None
    except Exception as e:
        print(f"[groq] CRASHED: {e}")
        return None


def _call_openrouter(prompt):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "openrouter/free",
            "messages": [
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            print(f"[openrouter] HTTP {resp.status_code}: {resp.text[:200]}")
            return None
        data = resp.json()
        choices = data.get("choices") or []
        if not choices:
            return None
        return (choices[0].get("message", {}).get("content") or "").strip() or None
    except Exception as e:
        print(f"[openrouter] CRASHED: {e}")
        return None


_PROVIDERS = [
    ("openrouter", _call_openrouter),
    ("groq", _call_groq),
    ("gemini", _call_gemini),
    ("deepseek", _call_deepseek),
]


def ai_provider_answer(user_text):
    """Har provider ko baari-baari try karta hai. Pehla jo kaam kare,
    uska jawab return karta hai. Sab fail ho to None."""
    for name, fn in _PROVIDERS:
        result = fn(user_text)
        if result:
            print(f"[ai_providers] answered via {name}")
            return result
    print("[ai_providers] all providers failed/unavailable")
    return None
