"""
update_sources_icon_favicon.py

Repo ROOT se chalao:
    python update_sources_icon_favicon.py

Yeh sirf ye badalta hai: "Sources" button ke saamne jo generic
🔗 (chain) icon dikhta hai, uski jagah ab pehli website ka asli
logo (favicon) dikhega. Baaki kuch nahi badalta.
"""

from pathlib import Path
import sys

INDEX_HTML = Path("index.html")

OLD_BTN_HTML = '''                const btn = document.createElement('button');
                btn.className = 'msg-action-btn sources-inline-btn';
                btn.type = 'button';
                btn.title = 'Sources';
                btn.innerHTML =
                    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>' +
                    '<span>Sources · ' + sources.length + '</span>';'''

NEW_BTN_HTML = '''                const btn = document.createElement('button');
                btn.className = 'msg-action-btn sources-inline-btn';
                btn.type = 'button';
                btn.title = 'Sources';
                let _firstDomain = '';
                try { _firstDomain = new URL(sources[0].url).hostname.replace('www.', ''); } catch (e) { _firstDomain = ''; }
                const _faviconUrl = _firstDomain
                    ? ('https://www.google.com/s2/favicons?domain=' + _firstDomain + '&sz=64')
                    : '';
                btn.innerHTML =
                    (_faviconUrl ? '<img class="sources-btn-favicon" src="' + _faviconUrl + '" alt="" loading="lazy">' : '') +
                    '<span>Sources · ' + sources.length + '</span>';'''

OLD_CSS_ANCHOR = '''        .sources-inline-btn svg {
            width: 14px;
            height: 14px;
        }'''

NEW_CSS_ANCHOR = '''        .sources-inline-btn svg {
            width: 14px;
            height: 14px;
        }
        .sources-btn-favicon {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            flex-shrink: 0;
        }'''


def main():
    if not INDEX_HTML.exists():
        sys.exit(f"{INDEX_HTML} nahi mila. Repo ROOT se chalao.")

    source = INDEX_HTML.read_text(encoding="utf-8")

    if "sources-btn-favicon" in source:
        print("Favicon icon already lagi hai — kuch nahi badla.")
        return

    if OLD_BTN_HTML not in source:
        sys.exit("Sources button ka expected HTML nahi mila. Mujhe fresh index.html bhejo.")
    source = source.replace(OLD_BTN_HTML, NEW_BTN_HTML, 1)

    if OLD_CSS_ANCHOR not in source:
        sys.exit("CSS anchor nahi mila. Mujhe fresh index.html bhejo.")
    source = source.replace(OLD_CSS_ANCHOR, NEW_CSS_ANCHOR, 1)

    INDEX_HTML.write_text(source, encoding="utf-8")
    print("Sources button ka icon ab website ka logo hai. OK")
    print("Ab: git add . && git commit -m 'use website favicon as Sources icon' && git push")


if __name__ == "__main__":
    main()
