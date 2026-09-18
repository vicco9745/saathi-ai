"""
update_web_search_v2.py

Repo ke ROOT folder mein rakho (jahan update_saathi.py hai) aur chalao:

    python update_web_search_v2.py

Yeh khud detect kar lega ki pehle wala update_web_search.py already chal
chuka hai ya nahi — dono case handle karta hai. Sirf itna karta hai:

  - Web search ke jawab wale case mein "मैं अभी यह जवाब सीख रहा हूँ।"
    KABHI nahi dikhega.
  - Agar dataset mein match nahi mila, web search se jawab mil gaya
    -> wahi jawab Saathi ki taraf se dikhega.
  - Agar web search se bhi kuch reliable nahi mila
    -> "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"

Kuch aur nahi tootega — memory, learning queue, dataset matching sab
waisa hi rahega.
"""

from pathlib import Path
import re
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")
REQUIREMENTS = Path("requirements.txt")

OLD_FALLBACK_TEXT = "मैं अभी यह जवाब सीख रहा हूँ।"
NEW_FALLBACK_TEXT = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"

WEB_SEARCH_FUNCTION = '''
def web_search_answer(query):
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

    return None

'''


def ensure_requests_imported(source: str) -> str:
    if re.search(r"^import requests$", source, re.MULTILINE):
        return source
    anchor = "from pathlib import Path"
    if anchor in source:
        return source.replace(anchor, anchor + "\nimport requests", 1)
    return "import requests\n" + source


def insert_web_search_function(source: str) -> str:
    if "def web_search_answer(" in source:
        return source
    marker = "def get_response(user_text):"
    if marker not in source:
        raise SystemExit(
            "'def get_response(user_text):' nahi mila. "
            "response_engine.py ka structure alag hai — mujhe file bhejo."
        )
    return source.replace(marker, WEB_SEARCH_FUNCTION + marker, 1)


def build_replacement(indent, with_context):
    if with_context:
        return (
            f'{indent}web_answer = web_search_answer(original_text)\n'
            f'{indent}if web_answer:\n'
            f'{indent}    reply = web_answer\n'
            f'{indent}    add_conversation(original_text, reply)\n'
            f'{indent}    return reply\n'
            f'{indent}save_to_learning_queue(original_text)\n'
            f'{indent}reply = "{NEW_FALLBACK_TEXT}"\n'
            f'{indent}add_conversation(original_text, reply)\n'
            f'{indent}return reply'
        )
    return (
        f'{indent}web_answer = web_search_answer(original_text)\n'
        f'{indent}if web_answer:\n'
        f'{indent}    return web_answer\n'
        f'{indent}save_to_learning_queue(original_text)\n'
        f'{indent}return "{NEW_FALLBACK_TEXT}"'
    )


def patch_fallback(source: str):
    # Case: already patched earlier (has web_answer logic), context variant
    pattern_v1_context = re.compile(
        r'^([ \t]*)web_answer = web_search_answer\(original_text\)\n'
        r'[ \t]*if web_answer:\n'
        r'[ \t]*reply = web_answer\n'
        r'[ \t]*add_conversation\(original_text, reply\)\n'
        r'[ \t]*return reply\n'
        r'[ \t]*save_to_learning_queue\(original_text\)\n'
        r'[ \t]*reply = "(?:' + re.escape(OLD_FALLBACK_TEXT) + r'|' + re.escape(NEW_FALLBACK_TEXT) + r')"\n'
        r'[ \t]*add_conversation\(original_text, reply\)\n'
        r'[ \t]*return reply\s*$',
        re.MULTILINE,
    )
    # Case: already patched earlier, simple variant
    pattern_v1_simple = re.compile(
        r'^([ \t]*)web_answer = web_search_answer\(original_text\)\n'
        r'[ \t]*if web_answer:\n'
        r'[ \t]*return web_answer\n'
        r'[ \t]*save_to_learning_queue\(original_text\)\n'
        r'[ \t]*return "(?:' + re.escape(OLD_FALLBACK_TEXT) + r'|' + re.escape(NEW_FALLBACK_TEXT) + r')"\s*$',
        re.MULTILINE,
    )
    # Case: never patched, context variant
    pattern_a_context = re.compile(
        r'^([ \t]*)save_to_learning_queue\(original_text\)\n'
        r'[ \t]*reply = "' + re.escape(OLD_FALLBACK_TEXT) + r'"\n'
        r'[ \t]*add_conversation\(original_text, reply\)\n'
        r'[ \t]*return reply\s*$',
        re.MULTILINE,
    )
    # Case: never patched, simple variant
    pattern_a_simple = re.compile(
        r'^([ \t]*)save_to_learning_queue\(original_text\)\n'
        r'[ \t]*return "' + re.escape(OLD_FALLBACK_TEXT) + r'"\s*$',
        re.MULTILINE,
    )

    for pattern, with_context in (
        (pattern_v1_context, True),
        (pattern_v1_simple, False),
        (pattern_a_context, True),
        (pattern_a_simple, False),
    ):
        m = pattern.search(source)
        if m:
            indent = m.group(1)
            replacement = build_replacement(indent, with_context)
            return pattern.sub(replacement, source, count=1)

    raise SystemExit(
        "Expected fallback block nahi mila. Ho sakta hai response_engine.py "
        "already alag tarah se likha ho — file ka content mujhe bhej do."
    )


def add_requests_to_requirements():
    if not REQUIREMENTS.exists():
        return
    text = REQUIREMENTS.read_text(encoding="utf-8")
    lines = [l.strip() for l in text.splitlines()]
    if any(l.lower().startswith("requests") for l in lines):
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += "requests\n"
    REQUIREMENTS.write_text(text, encoding="utf-8")


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(
            f"{RESPONSE_ENGINE} nahi mila. Yeh script repo ke ROOT folder se "
            "chalao (jahan update_saathi.py bhi hai)."
        )

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")
    original = source

    source = ensure_requests_imported(source)
    source = insert_web_search_function(source)
    source = patch_fallback(source)

    if source == original:
        print("Kuch badla nahi — pehle se sahi state mein tha.")
        return

    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    add_requests_to_requirements()
    print("Update ho gaya. OK")
    print("Ab chalao: pip install -r requirements.txt")
    print("Fir server restart karo: uvicorn app.main:app --reload --port 8000")


if __name__ == "__main__":
    main()
