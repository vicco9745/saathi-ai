p = "app/main.py"
s = open(p, encoding="utf-8").read()
if "SITECHECK" in s:
    print("sitecheck: pehle se laga hai")
    raise SystemExit
old = '"reply": "Yeh raha aapki website ka code.",'
new = '"reply": "Yeh raha aapki website ka code." + _site_check_report(html),  # SITECHECK'
helper = r'''

# SITECHECK: website banne ke baad Saathi Private Chrome se jaanch
def _site_check_report(html):
    url = os.environ.get("CHROME_URL", "").rstrip("/")
    key = os.environ.get("CHROME_KEY", "")
    if not url or not key:
        return ""
    import requests
    try:
        r = requests.post(url + "/check", json={"html": html, "shots": False}, headers={"X-Chrome-Key": key}, timeout=90)
        if r.status_code != 200:
            return "\n\n(Chrome jaanch nahi ho paayi: server ne %d diya.)" % r.status_code
        d = r.json()
        if d.get("summary") == "ERROR":
            return "\n\n(Chrome jaanch nahi ho paayi.)"
        lines = (d.get("text") or "").strip().split("\n")
        out = "\n\n**Chrome jaanch:** " + lines[0]
        if len(lines) > 1:
            out += "\n\n" + "\n".join("- " + x for x in lines[1:])
        return out
    except Exception:
        return "\n\n(Chrome jaanch nahi ho paayi: Chrome server abhi jaag raha hai ya vyast hai.)"
'''
if s.count(old) == 1:
    open(p, "w", encoding="utf-8").write(s.replace(old, new).rstrip("\n") + helper)
    print("sitecheck: patch lag gaya")
else:
    print("sitecheck: line nahi mili, kuch nahi badla", s.count(old))
