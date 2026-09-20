"""
update_ai_providers.py

Repo ROOT se chalao:
    python update_ai_providers.py

Yeh get_response() mein AI providers (Gemini -> DeepSeek) ko jodta hai:

  dataset match -> context -> similar match -> AI providers (naya) ->
  web search (purana) -> "nahi mila" fallback

Agar ichat_ai/ai_providers.py na mile, ya dono providers fail ho jaayen
(limit khatam, key galat, ya koi bhi error), to bina crash hue seedha
web search wale purane rasty par chala jayega — kuch nahi tootega.
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")
AI_PROVIDERS_FILE = Path("ichat_ai/ai_providers.py")

OLD_BLOCK = '''    similar_answer = find_similar_response(original_text)
    if similar_answer:
        reply = similar_answer
        add_conversation(original_text, reply)
        return reply

    web_answer, web_sources = web_search_answer(original_text)'''

NEW_BLOCK = '''    similar_answer = find_similar_response(original_text)
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

    web_answer, web_sources = web_search_answer(original_text)'''


def main():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila. Repo ROOT se chalao.")

    if not AI_PROVIDERS_FILE.exists():
        print(
            f"WARNING: {AI_PROVIDERS_FILE} abhi nahi mili. Patch phir bhi lagega "
            "(safe hai), lekin AI providers tab tak kaam nahi karenge jab tak "
            "ai_providers.py ichat_ai/ folder mein na ho."
        )

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")

    if "ai_provider_answer" in source:
        print("AI providers already jude hain — kuch nahi badla.")
        return

    if OLD_BLOCK not in source:
        sys.exit("Expected block nahi mila. Fresh cat bhejo.")

    source = source.replace(OLD_BLOCK, NEW_BLOCK, 1)
    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("AI providers (Gemini -> DeepSeek) jud gaye. OK")
    print("Ab: git add . && git commit -m 'wire Gemini/DeepSeek providers' && git push")


if __name__ == "__main__":
    main()
