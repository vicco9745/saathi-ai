"""Tark jaanch: jawab mein wahi vaakya baar-baar dohraya gaya ho to pakdo."""
import re


def check(question, reply):
    parts = [s.strip().lower() for s in re.split(r"[।.!?\n]+", reply or "")]
    parts = [s for s in parts if len(s) > 40]
    if len(parts) != len(set(parts)):
        return "FAIL", "The reply repeats the same sentence. Remove the repetition."
    return "PASS", ""
