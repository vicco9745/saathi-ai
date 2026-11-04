p = 'app/main.py'
s = open(p, encoding='utf-8').read()
BLOCK = r'''@app.post("/v1/describe")
def describe_site(body: GenericRequest, key=Depends(require_api_key)):
    raw = (body.prompt or "").strip()
    if not raw:
        raise HTTPException(400, "Prompt khaali nahi ho sakta")
    req, _, html = raw.partition("=====HTML=====")
    system = (
        "You write the short message shown to a user right after their website was built. "
        "LANGUAGE: Write in the same language and script as the user's request. If the request is Hinglish "
        "(Hindi in Roman letters) or Hindi, write in Devanagari Hindi. If English, English. Any other language: that language. "
        "FORMAT (markdown): first line is a bold sentence saying the website is ready, then an em dash and the site name in italics, "
        "for example: **Your website is ready** — *Site Name*. Then a blank line, then a bold heading meaning 'What is included'. "
        "Then 5 to 8 bullet lines, each starting with '- ' in the form '- **Label** — short detail'. "
        "Then a blank line and ONE closing sentence telling the user to tap the card to preview the live site, "
        "copy or download the code, and ask for any changes. "
        "CONTENT: Mention only things that really exist in the given HTML (sections, menu links, forms, buttons, animations, "
        "responsive layout, interactive features). Do not invent features, do not mention code details, do not use emojis, "
        "do not add any other text. Keep it under 130 words."
    )
    try:
        text = _call_groq(
            "User ki request:\n" + req.strip()[:1500] + "\n\nBani hui website ka HTML:\n" + html.strip()[:6000],
            system=system,
        ).strip()
    except Exception:
        text = ""
    return {"service": "describe", "reply": text}
'''
if '"/v1/describe"' in s:
    print('describe: pehle se laga hai')
else:
    open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n\n\n' + BLOCK)
    print('describe: laga diya')
