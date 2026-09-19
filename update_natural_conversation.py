"""
update_natural_conversation.py

Repo ROOT se chalao:
    python update_natural_conversation.py

Yeh add karta hai (bina kuch purana todhe):

1. Language detection — Hindi sawaal ka Hindi jawab, English ka English.
2. "Tumhara naam kya hai / who are you / tum kaun ho" jaise
   alag-alag phrasing wale sawaal pehchanta hai (exact match nahi,
   keyword-based fuzzy match).
3. "Tumhe kisne banaya / who created you" -> "Mujhe Vikas ne banaya hai."
4. Casual chat: "kaise ho / how are you", "kya kar rahe ho / what are
   you doing" -> natural jawab.
5. In sab sawaalon par Web Search nahi chalega (jaisa maanga gaya tha).
6. "Kuch nahi mila" wala fallback bhi ab language ke hisaab se aata hai.

Web Search, Memory, Learning Queue, dataset matching — sab waisa hi
chalta rahega.
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")

# ── 1) Helper functions: language detection + intent matching ──

HELPERS_BLOCK = '''
def _detect_lang(text):
    """Devanagari characters ke ratio se Hindi/English tay karta hai."""
    devanagari = sum(1 for ch in text if "\\u0900" <= ch <= "\\u097F")
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


'''

OLD_HELPERS_ANCHOR = "def get_response(user_text):"
NEW_HELPERS_ANCHOR = HELPERS_BLOCK + "def get_response(user_text):"


# ── 2) Replace the greeting + old narrow name-check with the fuller version ──

OLD_START = '''    normalized_original = normalize_text(original_text)

    _GREETINGS = {
        "hi", "hii", "hiii", "hello", "hey", "heya", "hlo", "helo",
        "namaste", "namaskar", "namaskaar",
        "hi saathi", "hello saathi", "hey saathi",
    }
    if normalized_original in _GREETINGS:
        reply = "नमस्ते! मैं Saathi हूँ, बताइए क्या मदद कर सकता हूँ?"
        add_conversation(original_text, reply)
        return reply

    if normalized_original in ("मेरा नाम क्या है", "मुझे क्या नाम से जानते हो"):'''

NEW_START = '''    normalized_original = normalize_text(original_text)
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

    if normalized_original in ("मेरा नाम क्या है", "मुझे क्या नाम से जानते हो"):'''


# ── 3) Language-aware "nothing found" fallback ──

OLD_FALLBACK = '''    save_to_learning_queue(original_text)
    reply = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"
    add_conversation(original_text, reply)
    return reply'''

NEW_FALLBACK = '''    save_to_learning_queue(original_text)
    if _lang == "hi":
        reply = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"
    else:
        reply = "I tried searching the internet, but couldn't find reliable information."
    add_conversation(original_text, reply)
    return reply'''


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila. Repo ROOT se chalao.")

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")

    if "_detect_lang" in source:
        print("Natural conversation logic already lagi hai — kuch nahi badla.")
        return

    if OLD_HELPERS_ANCHOR not in source:
        sys.exit("'def get_response(user_text):' anchor nahi mila.")
    source = source.replace(OLD_HELPERS_ANCHOR, NEW_HELPERS_ANCHOR, 1)

    if OLD_START not in source:
        sys.exit("Greeting/name block ka expected text nahi mila. Fresh cat bhejo.")
    source = source.replace(OLD_START, NEW_START, 1)

    if OLD_FALLBACK not in source:
        sys.exit("Fallback block ka expected text nahi mila. Fresh cat bhejo.")
    source = source.replace(OLD_FALLBACK, NEW_FALLBACK, 1)

    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("Natural conversation logic add ho gayi. OK")
    print("Ab: git add . && git commit -m 'add language-aware identity and small talk' && git push")


if __name__ == "__main__":
    main()
