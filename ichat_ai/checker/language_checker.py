"""Bhasha ki jaanch: bhatke hue chini/japani akshar hatata hai, aur maangi hui bhasha se milata hai."""
import re

_CJK = re.compile(r"[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]+")


def deva_ratio(text):
    letters = [c for c in (text or "") if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if "\u0900" <= c <= "\u097f") / len(letters)


def clean(reply):
    return _CJK.sub("", reply or "")


def check(question, reply):
    """(verdict, note). verdict: PASS ya FAIL."""
    q = (question or "").lower()
    asked_hi = re.search(r"hindi\s+mein|hindi\s+me\b|in\s+hindi|हिंदी\s+में|हिन्दी\s+में", q)
    asked_en = re.search(r"english\s+mein|english\s+me\b|in\s+english|अंग्रेज़ी\s+में|अंग्रेजी\s+में", q)
    r = deva_ratio(reply)
    if asked_hi and r < 0.3:
        return "FAIL", "The user asked for Hindi but the answer is not in Devanagari Hindi. Rewrite it fully in Devanagari Hindi."
    if asked_en and r > 0.3:
        return "FAIL", "The user asked for English but the answer is not in English. Rewrite it fully in English."
    return "PASS", ""
