"""
update_sources_ui.py

Repo ROOT se chalao:
    python update_sources_ui.py

Yeh 3 files patch karta hai:

1. ichat_ai/response_engine.py
   - web_search_answer() ab (answer_text, sources_list) tuple deta hai.
     Text ke andar link nahi hoga — sources alag se milenge.
   - get_response() web-search wale case mein, agar sources hain, to
     {"reply": ..., "sources": [...]} dict return karta hai (warna
     pehle jaisa plain string).

2. app/main.py
   - /v1/chat handler ab dict-wala response bhi handle karta hai aur
     JSON mein "sources" field add karta hai.

3. index.html
   - Jawab ke saath agar sources aayen, ek chhota "Sources · N" button
     dikhega (jaise ChatGPT). Click karne par links ki list khulti hai.

Sab kuch backward-compatible hai — koi purana feature nahi tootega.
"""

from pathlib import Path
import sys

RESPONSE_ENGINE = Path("ichat_ai/response_engine.py")
MAIN_PY = Path("app/main.py")
INDEX_HTML = Path("index.html")


# ─────────────────────────────────────────────────────────────
# 1) response_engine.py
# ─────────────────────────────────────────────────────────────

OLD_WEB_SEARCH_ANSWER = '''def web_search_answer(query):
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
        cleaned_query = _clean_query_for_search(query)
        results = search_web(cleaned_query, limit=3)
        print(f"[web_search_answer] cleaned query={cleaned_query!r} (original={query!r})")
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
        _wants_link = any(
            word in query.lower()
            for word in ("link", "url", "website", "site do", "link do", "वेबसाइट", "लिंक")
        )
        if url and _wants_link:
            answer = f"{answer}\\n\\n(Source: {url})"
        return answer

    print("[web_search_answer] no usable snippet in any result")
    return None'''

NEW_WEB_SEARCH_ANSWER = '''def web_search_answer(query):
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
                answer = f"{title}\\n\\n{snippet}" if title else snippet

    if answer is None:
        print("[web_search_answer] no usable snippet in any result")
        return None, []

    return answer, sources'''

OLD_GET_RESPONSE_WEB_BLOCK = '''    web_answer = web_search_answer(original_text)
    if web_answer:
        reply = web_answer
        add_conversation(original_text, reply)
        return reply
    save_to_learning_queue(original_text)
    reply = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"
    add_conversation(original_text, reply)
    return reply'''

NEW_GET_RESPONSE_WEB_BLOCK = '''    web_answer, web_sources = web_search_answer(original_text)
    if web_answer:
        reply = web_answer
        add_conversation(original_text, reply)
        if web_sources:
            return {"reply": reply, "sources": web_sources}
        return reply
    save_to_learning_queue(original_text)
    reply = "मैंने इंटरनेट पर ढूँढने की कोशिश की, लेकिन विश्वसनीय जानकारी नहीं मिली।"
    add_conversation(original_text, reply)
    return reply'''


def patch_response_engine():
    if not RESPONSE_ENGINE.exists():
        sys.exit(f"{RESPONSE_ENGINE} nahi mila.")

    source = RESPONSE_ENGINE.read_text(encoding="utf-8")

    if "sources.append(" in source:
        print("[response_engine.py] Sources logic already lagi hai — skip.")
        return

    if OLD_WEB_SEARCH_ANSWER not in source:
        sys.exit(
            "[response_engine.py] web_search_answer() ka expected block nahi mila. "
            "File shayad alag hai — mujhe fresh cat bhejo."
        )
    source = source.replace(OLD_WEB_SEARCH_ANSWER, NEW_WEB_SEARCH_ANSWER, 1)

    if OLD_GET_RESPONSE_WEB_BLOCK not in source:
        sys.exit(
            "[response_engine.py] get_response() ka web-search block nahi mila. "
            "Mujhe fresh cat bhejo."
        )
    source = source.replace(OLD_GET_RESPONSE_WEB_BLOCK, NEW_GET_RESPONSE_WEB_BLOCK, 1)

    RESPONSE_ENGINE.write_text(source, encoding="utf-8")
    print("[response_engine.py] Sources logic add ho gayi.")


# ─────────────────────────────────────────────────────────────
# 2) app/main.py
# ─────────────────────────────────────────────────────────────

OLD_CHAT_HANDLER = '''@app.post("/v1/chat")
def chat(body: ChatRequest, key=Depends(require_api_key)):
    record_usage(key, "chat")
    reply = get_response(body.message)
    return {
        "service": "chat",
        "reply": reply,
        "model": "saathi"
    }'''

NEW_CHAT_HANDLER = '''@app.post("/v1/chat")
def chat(body: ChatRequest, key=Depends(require_api_key)):
    record_usage(key, "chat")
    result = get_response(body.message)
    if isinstance(result, dict):
        return {
            "service": "chat",
            "reply": result.get("reply"),
            "sources": result.get("sources", []),
            "model": "saathi"
        }
    return {
        "service": "chat",
        "reply": result,
        "model": "saathi"
    }'''


def patch_main_py():
    if not MAIN_PY.exists():
        sys.exit(f"{MAIN_PY} nahi mila.")

    source = MAIN_PY.read_text(encoding="utf-8")

    if "result.get(\"sources\"" in source:
        print("[app/main.py] Sources handling already lagi hai — skip.")
        return

    if OLD_CHAT_HANDLER not in source:
        sys.exit(
            "[app/main.py] /v1/chat handler ka expected block nahi mila. "
            "File shayad alag hai — mujhe fresh cat bhejo."
        )
    source = source.replace(OLD_CHAT_HANDLER, NEW_CHAT_HANDLER, 1)
    MAIN_PY.write_text(source, encoding="utf-8")
    print("[app/main.py] Sources handling add ho gayi.")


# ─────────────────────────────────────────────────────────────
# 3) index.html
# ─────────────────────────────────────────────────────────────

OLD_CSS_ANCHOR = '''        .suggestion-chip:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            color: var(--accent);
        }

        /* ── Message Actions ── */'''

NEW_CSS_ANCHOR = '''        .suggestion-chip:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            color: var(--accent);
        }

        /* ── Sources button (ChatGPT-style) ── */
        .sources-wrap {
            position: relative;
            margin-top: 8px;
        }
        .sources-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--text-soft);
            padding: 6px 12px;
            border-radius: 14px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: background .15s, border-color .15s, color .15s;
        }
        .sources-btn svg {
            width: 14px;
            height: 14px;
        }
        .sources-btn:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            color: var(--accent);
        }
        .sources-panel {
            display: none;
            flex-direction: column;
            position: absolute;
            top: calc(100% + 6px);
            left: 0;
            min-width: 230px;
            max-width: 320px;
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: var(--panel-shadow);
            padding: 6px;
            z-index: 40;
        }
        .sources-panel.open {
            display: flex;
            animation: menuPop .16s ease;
        }
        .source-link-item {
            display: flex;
            flex-direction: column;
            gap: 2px;
            padding: 8px 10px;
            border-radius: 10px;
            text-decoration: none;
            color: var(--text);
            transition: background .15s;
        }
        .source-link-item:hover {
            background: var(--icon-hover);
        }
        .source-title {
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .source-domain {
            font-size: 11.5px;
            color: var(--text-muted);
        }

        /* ── Message Actions ── */'''

OLD_JS_FETCH_THEN = '''                    .then(data => {
                        const replyText = data.reply || 'Saathi से जवाब नहीं मिला।';
                        pendingReply.text = replyText;
                        if (Array.isArray(data.suggestions) && data.suggestions.length > 0) {
                            pendingReply.suggestions = data.suggestions.slice(0, 4);
                        }
                        saveChats();
                        renderMessages();
                    })'''

NEW_JS_FETCH_THEN = '''                    .then(data => {
                        const replyText = data.reply || 'Saathi से जवाब नहीं मिला।';
                        pendingReply.text = replyText;
                        if (Array.isArray(data.suggestions) && data.suggestions.length > 0) {
                            pendingReply.suggestions = data.suggestions.slice(0, 4);
                        }
                        if (Array.isArray(data.sources) && data.sources.length > 0) {
                            pendingReply.sources = data.sources.slice(0, 3);
                        }
                        saveChats();
                        renderMessages();
                    })'''

OLD_JS_RENDER_BLOCK = '''                    if (m.role === 'ai' && !m.typing && Array.isArray(m.suggestions) && m.suggestions.length > 0) {
                        row.appendChild(buildSuggestionChips(m.suggestions));
                    }

                    if (m.role === 'ai' && !m.typing) {
                        row.appendChild(buildMessageActions(m, idx, chat));
                    }'''

NEW_JS_RENDER_BLOCK = '''                    if (m.role === 'ai' && !m.typing && Array.isArray(m.suggestions) && m.suggestions.length > 0) {
                        row.appendChild(buildSuggestionChips(m.suggestions));
                    }

                    if (m.role === 'ai' && !m.typing && Array.isArray(m.sources) && m.sources.length > 0) {
                        row.appendChild(buildSourcesButton(m.sources));
                    }

                    if (m.role === 'ai' && !m.typing) {
                        row.appendChild(buildMessageActions(m, idx, chat));
                    }'''

OLD_JS_SUGGESTION_FN_END = '''                    wrap.appendChild(chip);
                });
                return wrap;
            }

            // ── Message actions ──'''

NEW_JS_SUGGESTION_FN_END = '''                    wrap.appendChild(chip);
                });
                return wrap;
            }

            function buildSourcesButton(sources) {
                const wrap = document.createElement('div');
                wrap.className = 'sources-wrap';

                const btn = document.createElement('button');
                btn.className = 'sources-btn';
                btn.type = 'button';
                btn.innerHTML =
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>' +
                    '<span>Sources · ' + sources.length + '</span>';

                const panel = document.createElement('div');
                panel.className = 'sources-panel';

                sources.forEach(s => {
                    const item = document.createElement('a');
                    item.className = 'source-link-item';
                    item.href = s.url;
                    item.target = '_blank';
                    item.rel = 'noopener noreferrer';
                    let domain = '';
                    try { domain = new URL(s.url).hostname.replace('www.', ''); } catch (e) { domain = s.url; }
                    item.innerHTML =
                        '<span class="source-title">' + escapeHtml(s.title || domain) + '</span>' +
                        '<span class="source-domain">' + escapeHtml(domain) + '</span>';
                    panel.appendChild(item);
                });

                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    panel.classList.toggle('open');
                });
                document.addEventListener('click', (e) => {
                    if (!wrap.contains(e.target)) { panel.classList.remove('open'); }
                });

                wrap.appendChild(btn);
                wrap.appendChild(panel);
                return wrap;
            }

            // ── Message actions ──'''


def patch_index_html():
    if not INDEX_HTML.exists():
        sys.exit(f"{INDEX_HTML} nahi mila.")

    source = INDEX_HTML.read_text(encoding="utf-8")

    if "buildSourcesButton" in source:
        print("[index.html] Sources button already lagi hai — skip.")
        return

    checks = [
        (OLD_CSS_ANCHOR, NEW_CSS_ANCHOR, "CSS"),
        (OLD_JS_FETCH_THEN, NEW_JS_FETCH_THEN, "fetch handler"),
        (OLD_JS_RENDER_BLOCK, NEW_JS_RENDER_BLOCK, "renderMessages block"),
        (OLD_JS_SUGGESTION_FN_END, NEW_JS_SUGGESTION_FN_END, "buildSourcesButton function"),
    ]

    for old, new, label in checks:
        if old not in source:
            sys.exit(f"[index.html] '{label}' anchor nahi mila. Mujhe fresh HTML bhejo.")

    for old, new, label in checks:
        source = source.replace(old, new, 1)

    INDEX_HTML.write_text(source, encoding="utf-8")
    print("[index.html] Sources button UI add ho gayi.")


def main():
    patch_response_engine()
    patch_main_py()
    patch_index_html()
    print("Sab update ho gaya. OK")
    print("Ab: git add . && git commit -m 'Add ChatGPT-style Sources button' && git push")


if __name__ == "__main__":
    main()
