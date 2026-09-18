"""
update_sources_position.py

Repo ROOT se chalao:
    python update_sources_position.py

Yeh sirf index.html mein Sources button ki JAGAH aur LOOK badalta hai:

  - Ab "Sources" ek chhota icon-button hai jo copy/like/dislike/share/
    more ke saath USI row mein, sabse aakhir mein baithta hai — alag
    se upar nahi.
  - Har source link ke saath uski website ka chhota favicon (logo)
    bhi dikhega.

Backend (response_engine.py / app/main.py) mein kuch nahi badalta —
woh already sahi hai.
"""

from pathlib import Path
import sys

INDEX_HTML = Path("index.html")

# ── 1) Revert the separate-row insertion in renderMessages ──

OLD_RENDER_BLOCK = '''                    if (m.role === 'ai' && !m.typing && Array.isArray(m.suggestions) && m.suggestions.length > 0) {
                        row.appendChild(buildSuggestionChips(m.suggestions));
                    }

                    if (m.role === 'ai' && !m.typing && Array.isArray(m.sources) && m.sources.length > 0) {
                        row.appendChild(buildSourcesButton(m.sources));
                    }

                    if (m.role === 'ai' && !m.typing) {
                        row.appendChild(buildMessageActions(m, idx, chat));
                    }'''

NEW_RENDER_BLOCK = '''                    if (m.role === 'ai' && !m.typing && Array.isArray(m.suggestions) && m.suggestions.length > 0) {
                        row.appendChild(buildSuggestionChips(m.suggestions));
                    }

                    if (m.role === 'ai' && !m.typing) {
                        row.appendChild(buildMessageActions(m, idx, chat));
                    }'''

# ── 2) Add the Sources chip inside the actions row, right before return ──

OLD_ACTIONS_END = '''                actions.appendChild(moreWrap);

                return actions;
            }'''

NEW_ACTIONS_END = '''                actions.appendChild(moreWrap);

                if (Array.isArray(message.sources) && message.sources.length > 0) {
                    actions.appendChild(buildSourcesButton(message.sources));
                }

                return actions;
            }'''

# ── 3) Replace buildSourcesButton() with an inline icon-chip + upward panel ──

OLD_SOURCES_FN = '''            function buildSourcesButton(sources) {
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
            }'''

NEW_SOURCES_FN = '''            function buildSourcesButton(sources) {
                const wrap = document.createElement('div');
                wrap.className = 'sources-inline-wrap';
                wrap.style.position = 'relative';

                const btn = document.createElement('button');
                btn.className = 'msg-action-btn sources-inline-btn';
                btn.type = 'button';
                btn.title = 'Sources';
                btn.innerHTML =
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>' +
                    '<span>Sources · ' + sources.length + '</span>';

                const panel = document.createElement('div');
                panel.className = 'sources-inline-panel';

                sources.forEach(s => {
                    const item = document.createElement('a');
                    item.className = 'source-link-item';
                    item.href = s.url;
                    item.target = '_blank';
                    item.rel = 'noopener noreferrer';
                    let domain = '';
                    try { domain = new URL(s.url).hostname.replace('www.', ''); } catch (e) { domain = s.url; }
                    const favicon = domain
                        ? 'https://www.google.com/s2/favicons?domain=' + domain + '&sz=64'
                        : '';
                    item.innerHTML =
                        (favicon ? '<img class="source-favicon" src="' + favicon + '" alt="" loading="lazy">' : '') +
                        '<span class="source-text">' +
                            '<span class="source-title">' + escapeHtml(s.title || domain) + '</span>' +
                            '<span class="source-domain">' + escapeHtml(domain) + '</span>' +
                        '</span>';
                    panel.appendChild(item);
                });

                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    document.querySelectorAll('.sources-inline-panel.open').forEach(p => {
                        if (p !== panel) p.classList.remove('open');
                    });
                    panel.classList.toggle('open');
                });
                document.addEventListener('click', (e) => {
                    if (!wrap.contains(e.target)) { panel.classList.remove('open'); }
                });

                wrap.appendChild(btn);
                wrap.appendChild(panel);
                return wrap;
            }'''

# ── 4) CSS: replace the old separate-row styles with inline-row styles ──

OLD_CSS = '''        /* ── Sources button (ChatGPT-style) ── */
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

NEW_CSS = '''        /* ── Sources button (inline in action row, ChatGPT-style) ── */
        .sources-inline-btn {
            width: auto !important;
            padding: 0 10px;
            border-radius: 15px;
            gap: 5px;
            font-size: 12px;
            font-weight: 600;
        }
        .sources-inline-btn svg {
            width: 14px;
            height: 14px;
        }
        .sources-inline-panel {
            display: none;
            flex-direction: column;
            position: absolute;
            bottom: 34px;
            left: 0;
            min-width: 240px;
            max-width: 320px;
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: var(--panel-shadow);
            padding: 6px;
            z-index: 40;
        }
        .sources-inline-panel.open {
            display: flex;
            animation: menuPop .16s ease;
        }
        .source-link-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 10px;
            border-radius: 10px;
            text-decoration: none;
            color: var(--text);
            transition: background .15s;
        }
        .source-link-item:hover {
            background: var(--icon-hover);
        }
        .source-favicon {
            width: 20px;
            height: 20px;
            border-radius: 5px;
            flex-shrink: 0;
            background: var(--icon-hover);
        }
        .source-text {
            display: flex;
            flex-direction: column;
            gap: 2px;
            min-width: 0;
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


def main():
    if not INDEX_HTML.exists():
        sys.exit(f"{INDEX_HTML} nahi mila. Repo ROOT se chalao.")

    source = INDEX_HTML.read_text(encoding="utf-8")

    if "sources-inline-btn" in source:
        print("Already inline position wali lagi hai — kuch nahi badla.")
        return

    steps = [
        (OLD_RENDER_BLOCK, NEW_RENDER_BLOCK, "renderMessages block"),
        (OLD_ACTIONS_END, NEW_ACTIONS_END, "buildMessageActions end"),
        (OLD_SOURCES_FN, NEW_SOURCES_FN, "buildSourcesButton function"),
        (OLD_CSS, NEW_CSS, "CSS block"),
    ]

    for old, new, label in steps:
        if old not in source:
            sys.exit(f"'{label}' anchor nahi mila. Mujhe fresh index.html bhejo.")

    for old, new, label in steps:
        source = source.replace(old, new, 1)

    INDEX_HTML.write_text(source, encoding="utf-8")
    print("Sources button ab action-row mein aa gaya, favicon ke saath. OK")
    print("Ab: git add . && git commit -m 'move Sources into action row with favicons' && git push")


if __name__ == "__main__":
    main()
