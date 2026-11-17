"""Sandarbh jaanch: jawab sawal ko dohra raha hai ya seedha jawab de raha hai."""
RESTATE = (
    "आपने पूछा है", "आपने पूछा", "आप पूछ रहे हैं", "आपका सवाल है",
    "you asked", "you are asking", "your question is",
)


def check(question, reply, history=None):
    head = (reply or "").strip()[:60].lower()
    for p in RESTATE:
        if head.startswith(p.lower()):
            return "FAIL", "The reply restates the question. Answer it directly, do not repeat it."
    return "PASS", ""
