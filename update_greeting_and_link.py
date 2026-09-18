"""
update_greeting_and_link.py

Repo ROOT se chalao:
    python update_greeting_and_link.py

Yeh 2 cheezein fix karta hai:

1. Simple greetings ("hi", "hello", "namaste" waghera) par ab seedha
   ek friendly fixed reply aayega — web search par nahi jayega.

2. Web search wale jawab mein "(Source: url)" link ab SIRF tab
   dikhega jab user ne khud "link", "website", "url" jaisa kuch
   maanga ho. Baaki normal sawaalon par sirf jawab aayega, link nahi.
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")

OLD_START = '''    normalized_original = normalize_text(original_text)

    if normalized_original in ("मेरा नाम क्या है", "मुझे क्या नाम से जानते हो"):'''

NEW_START = '''    normalized_original = normalize_text(original_text)

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

OLD_LINK = '''        answer = snippet
        if title:
            answer = f"{title}\\n\\n{snippet}"
        if url:
            answer = f"{answer}\\n\\n(Source: {url})"
        return answer'''

NEW_LINK = '''        answer = snippet
        if title:
            answer = f"{title}\\n\\n{snippet}"
        _wants_link = any(
            word in query.lower()
            for word in ("link", "url", "website", "site do", "link do", "वेबसाइट", "लिंक")
        )
        if url and _wants_link:
            answer = f"{answer}\\n\\n(Source: {url})"
        return answer'''


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila. Repo ROOT se chalao.")

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")
    original = source
    changed_any = False

    if "_GREETINGS = {" in source:
        print("Greeting handling already lagi hai — skip.")
    elif OLD_START in source:
        source = source.replace(OLD_START, NEW_START, 1)
        changed_any = True
        print("Greeting handling add ho gaya.")
    else:
        print("Greeting anchor nahi mila — yeh step skip, file check karo.")

    if "_wants_link" in source:
        print("Link-only-on-request logic already lagi hai — skip.")
    elif OLD_LINK in source:
        source = source.replace(OLD_LINK, NEW_LINK, 1)
        changed_any = True
        print("Link-only-on-request logic add ho gayi.")
    else:
        print("Link anchor nahi mila — yeh step skip, file check karo.")

    if not changed_any or source == original:
        print("Kuch naya nahi likha gaya.")
        return

    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("Update ho gaya. OK")
    print("Ab: git add . && git commit -m 'fix greetings and link visibility' && git push")


if __name__ == "__main__":
    main()
