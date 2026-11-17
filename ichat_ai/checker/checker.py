"""Saathi Master Checker: har jaanch alag file mein hai. Koi file hata do to wo jaanch chhoot jayegi, chat nahi rukegi."""
import importlib
import time


def _load(name):
    try:
        return importlib.import_module("ichat_ai.checker." + name)
    except Exception as e:
        print(f"[checker] {name} nahi mili, wo jaanch chhodi: {type(e).__name__}")
        return None


def check_reply(question, reply, evidence, history=None, lang_pref=None):
    original = reply
    t0 = time.time()
    try:
        if not isinstance(reply, str) or not reply.strip():
            return reply
        cfg = _load("checker_config")
        if cfg is not None and not getattr(cfg, "ENABLED", True):
            return reply
        lang, comp = _load("language_checker"), _load("completeness_checker")
        fact, corr, ver = _load("fact_checker"), _load("correction_engine"), _load("verification")
        ctx = _load("context_checker") if getattr(cfg, "CONTEXT_CHECK_ON", True) else None
        logic = _load("logic_checker") if getattr(cfg, "LOGIC_CHECK_ON", True) else None
        qa = _load("question_analyzer") if getattr(cfg, "QUESTION_ANALYZER_ON", True) else None
        if qa:
            try:
                print(f"[checker] sawal: {qa.analyze(question)}")
            except Exception as e:
                print(f"[checker] question_analyzer fail: {type(e).__name__}")
        maxc = min(max(int(getattr(cfg, "MAX_CORRECTIONS", 1)), 0), 2) if cfg else 1
        if lang:
            reply = lang.clean(reply)
        fact_bad = False
        for attempt in range(maxc + 1):
            problems, fact_bad = [], False
            if lang:
                v, n = lang.check(question, reply)
                if v != "PASS":
                    problems.append(n)
            if comp:
                v, n = comp.check(question, reply)
                if v != "PASS":
                    problems.append(n)
            if ctx:
                try:
                    v, n = ctx.check(question, reply, history)
                    if v != "PASS":
                        problems.append(n)
                except Exception as e:
                    print(f"[checker] context jaanch fail: {type(e).__name__}")
            if logic:
                try:
                    v, n = logic.check(question, reply)
                    if v != "PASS":
                        problems.append(n)
                except Exception as e:
                    print(f"[checker] logic jaanch fail: {type(e).__name__}")
            if fact:
                v, n = fact.check(question, reply, evidence)
                print(f"[checker] fact verdict: {v}")
                if v == "FAIL":
                    problems.append(n or "Some claims are not supported by the search results.")
                    fact_bad = True
                elif v == "UNCERTAIN":
                    fact_bad = True
            if not problems or corr is None or attempt >= maxc:
                break
            if time.time() - t0 > getattr(cfg, "TIME_BUDGET", 20):
                print(f"[checker] samay seema paar ({time.time() - t0:.0f}s), sudhar chhoda")
                break
            print(f"[checker] sudhar prayas {attempt + 1}: {problems}")
            reply = corr.fix(question, reply, evidence, problems)
            if lang:
                reply = lang.clean(reply)
        if fact_bad and cfg is not None and lang is not None:
            note = cfg.HI_NOTE if lang.deva_ratio(reply) > 0.3 else cfg.EN_NOTE
            reply = reply.rstrip() + "\n\n" + note
        print(f"[checker] total {time.time() - t0:.1f}s")
        return ver.approve(original, reply) if ver else reply
    except Exception as e:
        print(f"[checker] CRASHED, asli jawab bhej rahe: {type(e).__name__}: {e}")
        return original
