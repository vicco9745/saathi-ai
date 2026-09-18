"""
update_web_search_clean_query.py

Repo ROOT se chalao:
    python update_web_search_clean_query.py

Yeh web_search_answer() mein Bing ko bhejne se pehle query ko clean
karta hai — common Hindi filler/question words (kahan hai, kya hai,
kitna, kaun, kab, kyun, waghera) hata deta hai, taaki sirf asli topic
(jaise "Taj Mahal") Bing ko jaye aur behtar result mile.

Agar cleaning ke baad query khaali ho jaye, to original query hi
use hoga (safety fallback).
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")

CLEANER_FUNCTION = '''
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

'''

OLD_ANCHOR = "def web_search_answer(query):"

OLD_CALL = "        results = search_web(query, limit=3)"
NEW_CALL = (
    "        cleaned_query = _clean_query_for_search(query)\n"
    "        results = search_web(cleaned_query, limit=3)\n"
    "        print(f\"[web_search_answer] cleaned query={cleaned_query!r} "
    "(original={query!r})\")"
)


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila. Repo ROOT se chalao.")

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")
    original = source

    if "_clean_query_for_search" in source:
        print("Query cleaner already lagi hai — kuch nahi badla.")
        return

    if OLD_ANCHOR not in source:
        sys.exit("'def web_search_answer(query):' nahi mila.")
    source = source.replace(OLD_ANCHOR, CLEANER_FUNCTION + OLD_ANCHOR, 1)

    if OLD_CALL not in source:
        sys.exit(
            "search_web(query, limit=3) wali line nahi mili — "
            "response_engine.py ka content mujhe bhejo, main manually patch kar dunga."
        )
    source = source.replace(OLD_CALL, NEW_CALL, 1)

    if source == original:
        print("Kuch badla nahi.")
        return

    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("Query cleaner add ho gaya. OK")
    print("Ab: git add . && git commit -m 'clean hindi filler words before search' && git push")


if __name__ == "__main__":
    main()
