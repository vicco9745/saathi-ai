p = 'app/main.py'
s = open(p, encoding='utf-8').read()
FUNC = r'''def _pdf_caption(prompt, html_body):
    system = (
        "You write the short message shown to a user right after their PDF document was created. "
        "LANGUAGE: Write in the same language and script as the user's request. If the request is Hinglish "
        "(Hindi in Roman letters) or Hindi, write in Devanagari Hindi. If English, English. Any other language: that language. "
        "FORMAT (markdown): first line is a bold sentence saying the PDF is ready, then an em dash and the document title in italics, "
        "for example: **Your PDF is ready** — *Document Title*. Then a blank line, then a bold heading meaning What is inside. "
        "Then 3 to 6 bullet lines, each starting with a dash and a space, in the form: - **Label** — short detail. "
        "Base them ONLY on the given document HTML. Then a blank line and ONE closing sentence telling the user to tap the card "
        "to preview the PDF, use Download to save it, and ask for any changes (content, headings, language or design). "
        "Do not use emojis, do not invent content, do not add any other text. Keep it between 50 and 110 words."
    )
    try:
        return _call_groq(
            "User ki request:\n" + (prompt or "").strip()[:1500] + "\n\nBane hue document ka HTML:\n" + (html_body or "").strip()[:5000],
            system=system,
        ).strip()
    except Exception:
        return ""
'''
R = [
    ('        "pdf_base64": pdf_b64,\n        "filename": "saathi.pdf",\n    }',
     '        "pdf_base64": pdf_b64,\n        "filename": "saathi.pdf",\n        "caption": _pdf_caption(body.prompt, html_body),\n    }'),
    ('"filename": "saathi.pdf",\n                "model": "saathi",\n                "kind": "pdf",',
     '"filename": "saathi.pdf",\n                "caption": _pdf_caption(body.message, html_body),\n                "model": "saathi",\n                "kind": "pdf",'),
]
if '_pdf_caption' in s:
    print('pdfcaption: pehle se laga hai')
elif all(s.count(a) == 1 for a, b in R):
    for a, b in R:
        s = s.replace(a, b, 1)
    open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n\n\n' + FUNC)
    print('pdfcaption: laga diya')
else:
    print('pdfcaption: jagah nahi mili', [s.count(a) for a, b in R])
