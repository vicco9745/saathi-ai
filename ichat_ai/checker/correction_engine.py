"""Sudhar engine: galti milne par jawab ko khoj ke nateejon ke hisab se dobara likhta hai."""
import re


def fix(question, reply, evidence, problems):
    try:
        from ichat_ai.checker.fact_checker import ask
        prompt = (
            "Rewrite the ANSWER to fix the PROBLEMS below. Use ONLY the SEARCH RESULTS for facts. "
            "Do not add any fact that is not in the results. Keep the advice and the safe-alternative steps; fix only the unsupported factual claims. Keep it complete, clear and in the same language and script as the ANSWER "
            "(unless a problem says to change the language). Keep a caring, human tone. "
            "Output only the final answer, with no explanation of what you changed.\n\n"
            "PROBLEMS:\n- " + "\n- ".join(p for p in problems if p) + "\n\n"
            "SEARCH RESULTS:\n" + str(evidence or "")[:6000] + "\n\nORIGINAL QUESTION:\n" + str(question)[:500] + "\n\nANSWER:\n" + str(reply)[:4000]
        )
        out = ask(prompt)
        out = re.sub(r"^\s*(ANSWER|FINAL ANSWER)\s*:\s*", "", out or "", flags=re.I).strip()
        return out if len(out) > 20 else reply
    except Exception as e:
        print(f"[checker.fix] skipped: {type(e).__name__}: {e}")
        return reply
