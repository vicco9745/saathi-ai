"""
update_web_search_v3.py

Repo ke ROOT folder se chalao:

    python update_web_search_v3.py

Yeh karta hai:
  1. web_search_answer() ko DuckDuckGo ki jagah aapke already-bane hue
     ichat_ai/web_search.py (Bing scraper, jo title/description/page
     content nikalta hai) se jawab banane ke liye badal deta hai.
  2. get_response() ke aakhri hisse mein agar "return reply" chhoot gaya
     ho (missing), to use safely add kar deta hai.

Kuch aur nahi tootega.
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")

OLD_FUNCTION = '''def web_search_answer(query):
    """
    DuckDuckGo Instant Answer API se seedha jawab dhoondhta hai.
    Koi API key nahi chahiye. Kuch na mile ya request fail ho jaye
    to None deta hai.
    """
    query = (query or "").strip()
    if not query:
        return None
    try:
        import requests
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,
                "format": "json",
                "no_redirect": "1",
                "no_html": "1",
                "skip_disambig": "1",
            },
            timeout=6,
            headers={"User-Agent": "SaathiAI/1.0"},
        )
        data = resp.json()
    except Exception:
        return None

    answer = data.get("AbstractText") or data.get("Answer")
    if answer:
        source = data.get("AbstractURL") or ""
        if source:
            return f"{answer}\\n\\n(Source: {source})"
        return answer

    for topic in data.get("RelatedTopics", []):
        if isinstance(topic, dict) and topic.get("Text"):
            return topic["Text"]
        if isinstance(topic, dict) and topic.get("Topics"):
            for sub in topic["Topics"]:
                if isinstance(sub, dict) and sub.get("Text"):
                    return sub["Text"]

    return None'''

NEW_FUNCTION = '''def web_search_answer(query):
    """
    ichat_ai/web_search.py ke Bing scraper (search_web) se jawab banata hai.
    Pehle result ka description ya page content use karta hai. Kuch na
    mile ya request fail ho jaye to None deta hai.
    """
    query = (query or "").strip()
    if not query:
        return None

    try:
        from ichat_ai.web_search import search_web
        results = search_web(query, limit=3)
    except Exception:
        return None

    for result in results:
        title = (result.get("title") or "").strip()
        description = (result.get("description") or "").strip()
        content = (result.get("content") or "").strip()
        url = (result.get("url") or "").strip()

        snippet = description or content[:500]
        if not snippet:
            continue

        answer = snippet
        if title:
            answer = f"{title}\\n\\n{snippet}"
        if url:
            answer = f"{answer}\\n\\n(Source: {url})"
        return answer

    return None'''

OLD_TAIL = '''    save_to_learning_queue(original_text)
    reply = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"
    add_conversation(original_text, reply)'''

NEW_TAIL = OLD_TAIL + "\n    return reply"


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila. Repo ke ROOT folder se chalao.")

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")
    original = source

    if OLD_FUNCTION in source:
        source = source.replace(OLD_FUNCTION, NEW_FUNCTION, 1)
        print("web_search_answer() ko Bing scraper se jod diya.")
    elif "from ichat_ai.web_search import search_web" in source:
        print("web_search_answer() already Bing scraper use kar raha hai — skip.")
    else:
        print(
            "OLD DuckDuckGo function exact match nahi hua — "
            "shayad file thodi alag hai. Yeh step skip kiya, baaki check karta hoon."
        )

    # Fix missing "return reply" at the very end, if it's actually missing
    stripped = source.rstrip()
    if stripped.endswith('add_conversation(original_text, reply)') and OLD_TAIL in source:
        source = source.replace(OLD_TAIL, NEW_TAIL, 1)
        print("Missing 'return reply' add kar diya.")

    if source == original:
        print("Kuch badla nahi.")
        return

    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("Update ho gaya. OK")
    print("Server restart karo: uvicorn app.main:app --reload --port 8000")


if __name__ == "__main__":
    main()
