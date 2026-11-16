"""Poorepan ki jaanch: bahut chhota ya beech mein kata hua jawab pakadta hai."""
import re

try:
    from ichat_ai.checker import checker_config as cfg
    _MIN = getattr(cfg, "MIN_REPLY_CHARS", 40)
except Exception:
    _MIN = 40


def check(question, reply):
    """(verdict, note). verdict: PASS ya INCOMPLETE."""
    t = (reply or "").strip()
    if len(t) < _MIN:
        return "INCOMPLETE", "The answer is too short. Give a complete answer using the search results."
    if re.search(r"[,:;]\s*$|\b(and|or|but|aur|और|या)\s*$", t):
        return "INCOMPLETE", "The answer looks cut off in the middle. Complete it."
    return "PASS", ""
