import os, time, hmac, base64, socket, ipaddress, threading
from urllib.parse import urlparse
from fastapi import FastAPI, Request, Body, HTTPException
from playwright.sync_api import sync_playwright

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
LOCK = threading.Lock()
KEY = os.environ.get("CHROME_KEY", "")
VIEWPORTS = [("desktop", 1920, 1080), ("tablet", 768, 1024), ("mobile", 360, 640)]
ARGS = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", "--disable-extensions", "--mute-audio", "--js-flags=--max-old-space-size=192"]
RES_TYPES = ("image", "script", "stylesheet", "font", "fetch", "xhr")
BTN_SEL = "button, [role=button], input[type=submit], input[type=button]"
STATE_JS = "() => document.body.innerHTML.length + '|' + location.href + '|' + document.title"
INFO_JS = """() => {
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src).map(i => i.src.slice(0, 80));
  const anchors = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.getElementById(h.slice(1)) && !document.getElementsByName(h.slice(1)).length).slice(0, 10);
  const over = document.documentElement.scrollWidth - window.innerWidth;
  return {broken: broken, anchors: anchors, over: over};
}"""
_OK = {}


def need_key(request):
    got = request.headers.get("x-chrome-key", "")
    if len(KEY) < 24 or not hmac.compare_digest(got.encode("utf-8"), KEY.encode("utf-8")):
        time.sleep(1)
        raise HTTPException(404, "Not Found")


def public_host(host):
    if not host:
        return False
    if host in _OK:
        return _OK[host]
    ok = True
    try:
        for info in socket.getaddrinfo(host, None):
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
                ok = False
    except Exception:
        ok = False
    _OK[host] = ok
    return ok


def rss_mb():
    tot = 0
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                with open("/proc/%s/status" % pid) as f:
                    for l in f:
                        if l.startswith("VmRSS:"):
                            tot += int(l.split()[1])
                            break
            except Exception:
                pass
    return round(tot / 1024)


def run_check(url, html, shots):
    t0 = time.time()
    peak = 0
    vps = {}
    err_map, warn_map = {}, {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS)
        try:
            for name, w, h in VIEWPORTS:
                if time.time() - t0 > 100:
                    warn_map.setdefault("samay khatam, yeh size nahi jaancha", []).append(name)
                    continue
                errs, warns, shot = [], [], ""
                ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=(name == "mobile"), has_touch=(name != "desktop"))

                def guard(route, request, errs=errs):
                    u = urlparse(request.url)
                    if u.scheme in ("data", "blob", "about"):
                        return route.continue_()
                    if u.scheme not in ("http", "https") or not public_host(u.hostname):
                        errs.append("rok diya (galat ya private pata): " + request.url[:80])
                        return route.abort()
                    return route.continue_()

                ctx.route("**/*", guard)
                pg = ctx.new_page()
                pg.set_default_timeout(8000)
                pg.on("dialog", lambda d: d.dismiss())
                pg.on("pageerror", lambda e, errs=errs: errs.append("JS galti: " + str(e)[:140]))

                def on_console(m, errs=errs):
                    if m.type == "error" and not m.text.startswith("Failed to load resource"):
                        errs.append("console: " + m.text[:120])

                def on_fail(r, errs=errs):
                    if r.resource_type in RES_TYPES:
                        errs.append("load nahi hua: " + r.url[:90])

                def on_resp(r, errs=errs):
                    if r.status >= 400 and r.request.resource_type in RES_TYPES and "favicon" not in r.url:
                        errs.append("HTTP %d: %s" % (r.status, r.url[:90]))

                pg.on("console", on_console)
                pg.on("requestfailed", on_fail)
                pg.on("response", on_resp)
                loaded = True
                try:
                    if html is not None:
                        pg.set_content(html, wait_until="load", timeout=20000)
                    else:
                        pg.goto(url, wait_until="load", timeout=25000)
                except Exception as e:
                    loaded = False
                    errs.append("page khula nahi: " + str(e)[:140])
                if loaded:
                    pg.wait_for_timeout(800)
                    try:
                        info = pg.evaluate(INFO_JS)
                        for s in info["broken"]:
                            errs.append("tuti image: " + s)
                        for a in info["anchors"]:
                            errs.append("tuta link: " + a + " ka thikana nahi mila")
                        if info["over"] > 2:
                            warns.append("page chaudai se %dpx bahar jaata hai" % info["over"])
                    except Exception:
                        pass
                    if html is not None and name == "desktop":
                        for hnd in pg.query_selector_all(BTN_SEL)[:10]:
                            try:
                                if not hnd.is_visible():
                                    continue
                                label = ((hnd.inner_text() or hnd.get_attribute("value") or "").strip())[:30]
                                before = pg.evaluate(STATE_JS)
                                hnd.click(timeout=1500)
                                pg.wait_for_timeout(250)
                                if pg.evaluate(STATE_JS) == before:
                                    warns.append("shayad bekaar button: '" + label + "'")
                            except Exception:
                                pass
                    if shots:
                        try:
                            shot = base64.b64encode(pg.screenshot(type="jpeg", quality=55)).decode()
                        except Exception:
                            pass
                peak = max(peak, rss_mb())
                ctx.close()
                for m in dict.fromkeys(errs):
                    err_map.setdefault(m, []).append(name)
                for m in dict.fromkeys(warns):
                    warn_map.setdefault(m, []).append(name)
                vps[name] = {"errors": list(dict.fromkeys(errs))[:15], "warnings": list(dict.fromkeys(warns))[:15], "shot_b64": shot}
        finally:
            b.close()

    def fmt(d):
        return [m + " [" + ", ".join(v) + "]" for m, v in d.items()][:30]

    errors, warnings = fmt(err_map), fmt(warn_map)
    summary = "FAIL" if errors else ("WARN" if warnings else "PASS")
    head = {"PASS": "Jaanch pass: koi galti nahi mili", "WARN": "Jaanch mein chetavaniyan mili", "FAIL": "Jaanch mein galtiyan mili"}[summary]
    lines = [head] + ["GALTI: " + e for e in errors] + ["CHETAVANI: " + x for x in warnings]
    return {"summary": summary, "text": "\n".join(lines), "errors": errors, "warnings": warnings,
            "viewports": vps, "peak_rss_mb": peak, "seconds": round(time.time() - t0, 1)}


@app.get("/")
def root():
    return {"ok": True}


@app.post("/check")
def check(request: Request, body: dict = Body(...)):
    need_key(request)
    url, html = body.get("url"), body.get("html")
    shots = bool(body.get("shots", True))
    if html is None and not url:
        raise HTTPException(400, "url ya html do")
    if html is not None:
        html = str(html)[:900000]
        url = None
    else:
        u = urlparse(str(url))
        if u.scheme not in ("http", "https") or not public_host(u.hostname):
            raise HTTPException(400, "sirf public http/https pata chalega")
    if not LOCK.acquire(blocking=False):
        raise HTTPException(429, "ek jaanch chal rahi hai, thodi der baad try karo")
    try:
        return run_check(url, html, shots)
    except Exception as e:
        return {"summary": "ERROR", "text": "jaanch chal nahi paayi: " + repr(e)[:300], "peak_rss_mb": rss_mb()}
    finally:
        LOCK.release()
