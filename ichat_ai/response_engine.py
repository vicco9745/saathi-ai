import json
from pathlib import Path
import requests
from ichat_ai.memory.memory import add_conversation, get_conversation_history

BASE_DIR = Path(__file__).resolve().parent.parent
APPROVED_FILE = BASE_DIR / "ichat_ai" / "dataset" / "approved.jsonl"
LEARNING_FILE = BASE_DIR / "ichat_ai" / "dataset" / "learning_queue.jsonl"


def load_responses():
    responses = []

    if not APPROVED_FILE.exists():
        return responses

    with open(APPROVED_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if "user" in data and "assistant" in data:
                    responses.append(data)
            except json.JSONDecodeError:
                pass

    return responses


def save_to_learning_queue(user_text):
    text = user_text.strip()
    if not text:
        return

    sensitive_words = (
        "password", "passwd", "api key", "apikey",
        "secret", "token", "otp", "पासवर्ड",
        "एपीआई की", "ओटीपी"
    )

    lower_text = text.lower()

    if any(word in lower_text for word in sensitive_words):
        return

    normalized = normalize_text(text)
    existing = set()

    if LEARNING_FILE.exists():
        with open(LEARNING_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    existing.add(normalize_text(data.get("user", "")))
                except json.JSONDecodeError:
                    pass

    if normalized in existing:
        return

    with open(LEARNING_FILE, "a", encoding="utf-8") as f:
        json.dump({"user": text}, f, ensure_ascii=False)
        f.write("\n")


def normalize_text(text):
    return text.strip().lower().rstrip("?!।,").replace("  ", " ")

def similarity_score(text1, text2):
    words1 = set(normalize_text(text1).split())
    words2 = set(normalize_text(text2).split())

    if not words1 or not words2:
        return 0.0

    common = words1.intersection(words2)
    return len(common) / max(len(words1), len(words2))


def find_context_response(user_text):
    text = normalize_text(user_text)

    followups = {
        "और बताओ",
        "थोड़ा और बताओ",
        "फिर क्या",
        "आगे क्या",
        "और"
    }

    if text in followups:
        history = get_recent_context(3)

        for item in reversed(history):
            previous_answer = item.get("assistant", "").strip()
            if previous_answer:
                return previous_answer

    return None


def find_similar_response(user_text):
    best_answer = None
    best_score = 0.0

    for item in load_responses():
        score = similarity_score(user_text, item["user"])

        if score > best_score:
            best_score = score
            best_answer = item["assistant"]

    if best_score >= 0.5:
        return best_answer

    return None


def get_recent_context(limit=5):
    history = get_conversation_history()
    return history[-limit:]




import re as _re_web_search

_HINDI_FILLER_WORDS = [
    "kya hai", "kya h", "kya tha", "kya thi",
    "kahan hai", "kaha hai", "kahan h", "kaha h",
    "kitna hai", "kitni hai", "kitne hai", "kitna h",
    "kaun hai", "kaun tha", "kaun h",
    "kab hai", "kab tha", "kab h",
    "kyun hai", "kyu hai", "kyun h",
    "kaise hai", "kaise h",
    "hai kya", "hai kaha", "hai kitna",
    "क्या है", "कहाँ है", "कहां है", "कितना है", "कितनी है",
    "कौन है", "कब है", "क्यों है", "कैसे है",
    "kya", "kaha", "kahan", "kitna", "kitni", "kaun",
    "kab", "kyun", "kyu", "kaise", "hai", "h", "tha", "thi", "the",
]


def _clean_query_for_search(text):
    """Hindi filler/question words hata ke sirf topic nikaalta hai."""
    words = text.strip().split()
    if not words:
        return text

    lowered_words = [w.lower().strip("?!।,.") for w in words]

    kept = []
    for original, lowered in zip(words, lowered_words):
        if lowered in _HINDI_FILLER_WORDS:
            continue
        kept.append(original)

    cleaned = " ".join(kept).strip()
    return cleaned if cleaned else text

def web_search_answer(query):
    """
    ichat_ai/web_search.py ke Bing scraper (search_web) se jawab banata hai.
    Return: (answer_text, sources) tuple.
    sources ek list hai: [{"title": .., "url": ..}, ...]
    Kuch na mile ya request fail ho jaye to (None, []) milta hai.
    """
    query = (query or "").strip()
    if not query:
        return None, []

    try:
        from ichat_ai.web_search import search_web
        cleaned_query = _clean_query_for_search(query)
        results = search_web(cleaned_query, limit=3)
        print(f"[web_search_answer] cleaned query={cleaned_query!r} (original={query!r})")
        print(f"[web_search_answer] query={query!r} got {len(results)} results")
    except Exception as e:
        print(f"[web_search_answer] search_web CRASHED: {type(e).__name__}: {e}")
        return None, []

    answer = None
    sources = []

    for result in results:
        title = (result.get("title") or "").strip()
        description = (result.get("description") or "").strip()
        content = (result.get("content") or "").strip()
        url = (result.get("url") or "").strip()

        if url and title and len(sources) < 3:
            sources.append({"title": title, "url": url})

        if answer is None:
            snippet = description or content[:500]
            if snippet:
                answer = f"{title}\n\n{snippet}" if title else snippet

    if answer is None:
        print("[web_search_answer] no usable snippet in any result")
        return None, []

    return answer, sources


def _detect_lang(text):
    """Devanagari characters ke ratio se Hindi/English tay karta hai."""
    devanagari = sum(1 for ch in text if "\u0900" <= ch <= "\u097F")
    letters = sum(1 for ch in text if ch.isalpha())
    if letters == 0:
        return "hi"
    return "hi" if (devanagari / letters) > 0.3 else "en"


_IDENTITY_PATTERNS = [
    "tumhara naam", "aapka naam", "tumhara name", "aapka name",
    "your name", "what is your name", "whats your name",
    "who are you", "tum kaun ho", "aap kaun ho", "tu kaun hai",
    "naam batao", "naam kya hai",
    "आपका नाम", "तुम्हारा नाम", "तुम कौन हो", "आप कौन हो", "नाम बताओ",
]

_CREATOR_PATTERNS = [
    "tumhe kisne banaya", "aapko kisne banaya", "tumko kisne banaya",
    "who created you", "who made you", "kisne banaya hai", "kisne banaya",
    "आपको किसने बनाया", "तुम्हें किसने बनाया", "तुझे किसने बनाया", "किसने बनाया",
]

_HOWAREYOU_PATTERNS = [
    "kaise ho", "kaise hain", "kaisi ho", "how are you", "hows it going",
    "कैसे हो", "कैसे हैं", "कैसी हो",
]

_WHATDOING_PATTERNS = [
    "kya kar rahe ho", "kya kar rahi ho", "kya kar rha ho",
    "what are you doing", "whatcha doing",
    "क्या कर रहे हो", "क्या कर रही हो",
]


def _matches_any(normalized_text, patterns):
    return any(p in normalized_text for p in patterns)


def get_response(user_text):
    from ichat_ai.memory.memory import remember, recall

    original_text = user_text.strip()
    normalized_original = normalize_text(original_text)
    _lang = _detect_lang(original_text)

    _GREETINGS_EN = {"hi", "hii", "hiii", "hello", "hey", "heya", "hlo", "helo",
                      "hi saathi", "hello saathi", "hey saathi"}
    _GREETINGS_HI = {"namaste", "namaskar", "namaskaar"}

    if normalized_original in _GREETINGS_EN or normalized_original in _GREETINGS_HI:
        if normalized_original in _GREETINGS_HI or _lang == "hi":
            reply = "नमस्ते! मैं Saathi हूँ, बताइए क्या मदद कर सकता हूँ?"
        else:
            reply = "Hi! I'm Saathi. How can I help you?"
        add_conversation(original_text, reply)
        return reply

    if _matches_any(normalized_original, _IDENTITY_PATTERNS):
        if _lang == "hi":
            reply = "मेरा नाम Saathi है। मैं आपका AI असिस्टेंट हूँ। मैं आपकी कैसे मदद कर सकता हूँ?"
        else:
            reply = "My name is Saathi. I'm your AI assistant. How can I help you?"
        add_conversation(original_text, reply)
        return reply

    if _matches_any(normalized_original, _CREATOR_PATTERNS):
        reply = "मुझे Vikas ने बनाया है।" if _lang == "hi" else "I was created by Vikas."
        add_conversation(original_text, reply)
        return reply

    if _matches_any(normalized_original, _HOWAREYOU_PATTERNS):
        reply = "मैं ठीक हूँ 😊 आप बताइए, आप कैसे हैं?" if _lang == "hi" else "I'm doing well 😊 How about you?"
        add_conversation(original_text, reply)
        return reply

    if _matches_any(normalized_original, _WHATDOING_PATTERNS):
        reply = ("मैं यहाँ आपकी मदद के लिए तैयार हूँ! बताइए क्या करना है।" if _lang == "hi"
                  else "I'm here, ready to help! What would you like to do?")
        add_conversation(original_text, reply)
        return reply

    if normalized_original in ("मेरा नाम क्या है", "मुझे क्या नाम से जानते हो"):
        name = recall("user_name")
        if name:
            reply = f"आपका नाम {name} है।"
        else:
            reply = "मुझे अभी आपका नाम याद नहीं है।"
        add_conversation(original_text, reply)
        return reply

    if normalized_original.startswith("मेरा नाम है "):
        name = original_text[11:].strip()
        if name.endswith(" है"):
            name = name[:-3].strip()
        if name:
            remember("user_name", name)
            return f"ठीक है, मैं याद रखूँगा कि आपका नाम {name} है।"

    if normalized_original.startswith("मेरा नाम "):
        name = original_text[8:].strip()
        if name.endswith(" है"):
            name = name[:-3].strip()
        if name:
            remember("user_name", name)
            return f"ठीक है, मैं याद रखूँगा कि आपका नाम {name} है।"

    user_text = normalize_text(user_text)

    for item in load_responses():
        if user_text == normalize_text(item["user"]):
            reply = item["assistant"]
            add_conversation(original_text, reply)
            return reply

    context_answer = find_context_response(original_text)
    if context_answer:
        reply = context_answer
        add_conversation(original_text, reply)
        return reply

    similar_answer = find_similar_response(original_text)
    if similar_answer:
        reply = similar_answer
        add_conversation(original_text, reply)
        return reply

    try:
        from ichat_ai.ai_providers import ai_provider_answer
        ai_answer = ai_provider_answer(original_text)
    except Exception as e:
        print(f"[get_response] ai_provider_answer CRASHED: {type(e).__name__}: {e}")
        ai_answer = None

    if ai_answer:
        reply = ai_answer
        add_conversation(original_text, reply)
        return reply

    web_answer, web_sources = web_search_answer(original_text)
    if web_answer:
        reply = web_answer
        add_conversation(original_text, reply)
        if web_sources:
            return {"reply": reply, "sources": web_sources}
        return reply
    save_to_learning_queue(original_text)
    if _lang == "hi":
        reply = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"
    else:
        reply = "I tried searching the internet, but couldn't find reliable information."
    add_conversation(original_text, reply)
    return reply