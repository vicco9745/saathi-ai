"""
update_web_search_debug.py

Repo ROOT se chalao:
    python update_web_search_debug.py

Yeh web_search_answer() mein print() statements daal deta hai, taaki
Render ke "Logs" tab mein saaf dikhe ki search_web() fail kyun ho raha
hai (timeout, blocked, ya results khaali).

Baaki behavior kuch nahi badalta.
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")

OLD = '''    try:
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

NEW = '''    try:
        from ichat_ai.web_search import search_web
        results = search_web(query, limit=3)
        print(f"[web_search_answer] query={query!r} got {len(results)} results")
    except Exception as e:
        print(f"[web_search_answer] search_web CRASHED: {type(e).__name__}: {e}")
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

    print("[web_search_answer] no usable snippet in any result")
    return None'''


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila. Repo ROOT se chalao.")

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")

    if "search_web CRASHED" in source:
        print("Debug logging already lagi hai — kuch nahi badla.")
        return

    if OLD not in source:
        sys.exit(
            "Expected block nahi mila. Pehle update_web_search_v3.py chal chuka "
            "hona chahiye. Agar chal chuka hai to mujhe response_engine.py ka "
            "content dobara bhejo."
        )

    source = source.replace(OLD, NEW, 1)
    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("Debug logging add ho gaya. OK")
    print("Ab: git add . && git commit -m 'debug logging' && git push")


if __name__ == "__main__":
    main()
