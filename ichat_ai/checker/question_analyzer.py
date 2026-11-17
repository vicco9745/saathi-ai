"""Sawal ko samajhna: bhasha aur prakar. Jawab nahi badalta, sirf jaankari deta hai."""


def _deva(s):
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if "\u0900" <= c <= "\u097f") / len(letters)


def analyze(question):
    q = (question or "").strip()
    return {
        "lang": "hi" if _deva(q) > 0.3 else "en",
        "words": len(q.split()),
        "short": len(q.split()) <= 4,
    }
