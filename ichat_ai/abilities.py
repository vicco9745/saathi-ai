import json, os

_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abilities.json")


def _load():
    try:
        with open(_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def ability_down(key):
    for it in _load():
        if it.get("key") == key and it.get("status") == "broken":
            return True, it.get("note") or ""
    return False, ""


def abilities_text():
    on, down = [], []
    for it in _load():
        name = str(it.get("name", ""))
        if it.get("status") == "broken":
            down.append("- " + name + ": ABHI KHARAB HAI. Gadbadi: " + (it.get("note") or "abhi theek ho rahi hai"))
            continue
        need = it.get("needs_env") or []
        any_of = it.get("needs_any") or []
        if need and not all(os.environ.get(k) for k in need):
            continue
        if any_of and not any(os.environ.get(k) for k in any_of):
            continue
        on.append("- " + name + ": " + str(it.get("text", "")))
    out = ""
    if on:
        out += (
            "\n\nTUMHARI ABHI KI KSHAMTAYEN (yeh suchi apne aap banti hai: isme jo likha hai wahi tumhare paas hai, "
            "aur jo isme nahi hai uske baare mein mat kaho ki tumhare paas hai):\n"
            + "\n".join(on)
            + "\nJab user poochhe ki tumhare paas kya hai ya kya tum koi kaam kar sakte ho, to isi suchi ke hisaab se "
            "apne shabdon mein jawab do; koi tay vaakya mat dohrao."
        )
    if down:
        out += (
            "\n\nYEH SUVIDHAYEN ABHI KHARAB HAIN:\n" + "\n".join(down)
            + "\nAgar user inmein se koi suvidha maange, to apne shabdon mein kaho ki ismein abhi gadbadi hai, "
            "team ise theek karne mein lagi hai, jaldi theek ho jaayegi, aur abhi tum ise nahi kar sakte. "
            "Kharab ya adhoora kaam dene ki koshish mat karo aur banawati jawab mat banao."
        )
    return out
