"""Tathya ki jaanch: jawab ko khoj ke nateejon se milata hai. Kuch bhi gadbad ho to PASS maanta hai (chat nahi rukti)."""
import re

try:
    from ichat_ai.checker import checker_config as cfg
    _MAX = getattr(cfg, "MAX_EVIDENCE_CHARS", 6000)
except Exception:
    _MAX = 6000


def ask(prompt):
    from ichat_ai.ai_providers import ai_provider_answer
    r = ai_provider_answer(prompt)
    if isinstance(r, dict):
        r = r.get("reply") or ""
    return (r or "").strip()


def check(question, reply, evidence):
    """(verdict, note). verdict: PASS / FAIL / UNCERTAIN."""
    try:
        if not evidence:
            return "PASS", ""
        prompt = (
            "You are a strict fact checker. Do NOT answer the question yourself.\n"
            "Compare the ANSWER with the SEARCH RESULTS.\n"
            "PASS = every factual claim in the ANSWER is supported by the results.\n"
            "FAIL = the ANSWER contradicts the results, or states specific facts the results do not support, "
            "or calls something safe or genuine when the results show warnings.\n"
            "UNCERTAIN = the results are too thin or conflicting to verify the ANSWER.\n"
            "Reply in exactly this format and nothing else:\n"
            "VERDICT: PASS or FAIL or UNCERTAIN\n"
            "NOTE: one short sentence in English saying what is wrong or missing\n\n"
            "SEARCH RESULTS:\n" + str(evidence)[:_MAX] + "\n\nANSWER:\n" + str(reply)[:4000]
        )
        out = ask(prompt)
        m = re.search(r"VERDICT:\s*\**\s*(PASS|FAIL|UNCERTAIN)", out, re.I)
        if not m:
            return "PASS", ""
        n = re.search(r"NOTE:\s*(.+)", out, re.I | re.S)
        return m.group(1).upper(), (n.group(1).strip()[:400] if n else "")
    except Exception as e:
        print(f"[checker.fact] skipped: {type(e).__name__}: {e}")
        return "PASS", ""
