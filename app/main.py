import os
import requests as _req
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.db import init_db
from app.auth import require_api_key, record_usage
from ichat_ai.response_engine import get_response

app = FastAPI(
    title="iChat API",
    version="1.0.0",
    description="One API gateway for iChat services."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

class ChatAttachment(BaseModel):
    kind: Optional[str] = None
    dataUrl: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    model: str = "auto"
    memory: Optional[List[str]] = []
    history: Optional[List[dict]] = []
    lang_pref: Optional[str] = None
    allow_web_search: Optional[bool] = False
    attachments: Optional[List[ChatAttachment]] = []

# ═══════════════════════════════════════════════════════════════════
# PDF GENERATION — Multi-language (Hindi, Tamil, Telugu, Bengali, etc.)
# Uses fpdf2 with Noto Sans fonts (auto-downloaded and cached)
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# UNIVERSAL PDF — Chart & Image Helpers (matplotlib + Pillow)
# ═══════════════════════════════════════════════════════════════
def _draw_native_chart(pdf, data, x, y, w, h, chart_type="candlestick", title="", entry=None, stop=None, target=None):
    """Direct PDF me chart draw karo (bina matplotlib ke, pure python)."""
    import json as _json
    if isinstance(data, str):
        try: data = _json.loads(data)
        except Exception: data = []
    if not data: return

    # Background box
    pdf.set_fill_color(250, 250, 252)
    pdf.rect(x, y, w, h, 'F')
    pdf.set_draw_color(200, 200, 210)
    pdf.rect(x, y, w, h, 'D')

    # Title
    if title:
        pdf.set_xy(x, y + 2)
        pdf.set_text_color(50, 50, 60)
        try: pdf.set_font(pdf.font_family, "B", 10)
        except Exception: pdf.set_font("Helvetica", "B", 10)
        pdf.cell(w, 6, title, align='C')

    if chart_type == "candlestick":
        closes = [float(d.get('close', 0)) for d in data]
        highs = [float(d.get('high', 0)) for d in data]
        lows = [float(d.get('low', 0)) for d in data]
        if not closes: return
        
        min_p, max_p = min(lows), max(highs)
        if max_p == min_p: max_p += 1
        range_p = max_p - min_p

        chart_y = y + 10
        chart_h = h - 15
        chart_x = x + 10
        chart_w = w - 20

        candle_w = chart_w / len(data)
        body_w = candle_w * 0.6

        for i, d in enumerate(data):
            o = float(d.get('open', 0))
            c = float(d.get('close', 0))
            hi = float(d.get('high', 0))
            lo = float(d.get('low', 0))
            
            def to_y(p): return chart_y + chart_h - ((p - min_p) / range_p * chart_h)
            
            y_hi = to_y(hi); y_lo = to_y(lo); y_o = to_y(o); y_c = to_y(c)
            cx = chart_x + (i * candle_w) + (candle_w / 2)
            
            if c >= o:
                pdf.set_draw_color(38, 166, 154)
                pdf.set_fill_color(38, 166, 154)
            else:
                pdf.set_draw_color(239, 83, 80)
                pdf.set_fill_color(239, 83, 80)

            pdf.line(cx, y_hi, cx, y_lo)
            body_top = min(y_o, y_c)
            body_h = abs(y_o - y_c)
            if body_h < 1: body_h = 1
            pdf.rect(cx - body_w/2, body_top, body_w, body_h, 'F')

        def draw_line(price, color, label):
            if not price: return
            try: p_y = to_y(float(price))
            except: return
            pdf.set_draw_color(*color)
            pdf.set_line_width(0.5)
            pdf.line(chart_x, p_y, chart_x + chart_w, p_y)
            pdf.set_xy(chart_x + chart_w + 2, p_y - 3)
            pdf.set_text_color(*color)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(20, 6, label)

        draw_line(entry, (30, 100, 200), "Entry")
        draw_line(stop, (200, 50, 50), "Stop")
        draw_line(target, (50, 150, 50), "Target")



def _download_image_bytes(url, timeout=8):
    """URL ya data-URL se image bytes laao. Returns bytes ya None."""
    try:
        if not url:
            return None
        if url.startswith('data:image'):
            import base64 as _b64
            _header, _data = url.split(',', 1)
            return _b64.b64decode(_data)
        import requests as _r
        _resp = _r.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0'})
        if _resp.status_code == 200:
            return _resp.content
    except Exception as _e:
        print("[img] error: " + str(_e))
    return None


def _build_pdf_multilang(html_body: str, theme: str = "auto") -> bytes:
    """Universal PDF — text + charts + images + tables + boxes + pagebreak."""
    import re as _re
    import os as _os
    import urllib.request as _url
    from fpdf import FPDF as _FPDF
    from html.parser import HTMLParser as _HP

    THEMES = {
        "premium": {"bg": (15,23,42), "text": (230,230,240), "accent": (212,175,55), "accent2": (245,215,110), "muted": (150,160,180), "header_band": (15,23,42), "header_text": (212,175,55), "light": False},
        "colorful": {"bg": (255,255,255), "text": (30,30,50), "accent": (255,87,87), "accent2": (255,152,0), "muted": (130,130,150), "header_band": (255,87,87), "header_text": (255,255,255), "light": True},
        "business": {"bg": (255,255,255), "text": (26,26,46), "accent": (30,58,138), "accent2": (59,130,246), "muted": (110,110,130), "header_band": (30,58,138), "header_text": (255,255,255), "light": True},
        "book": {"bg": (253,248,240), "text": (60,40,20), "accent": (139,69,19), "accent2": (160,82,45), "muted": (140,120,100), "header_band": (253,248,240), "header_text": (139,69,19), "light": True},
        "auto": {"bg": (255,255,255), "text": (26,26,46), "accent": (16,163,127), "accent2": (13,139,108), "muted": (110,110,130), "header_band": (16,163,127), "header_text": (255,255,255), "light": True},
    }

    html = html_body or ""

    if theme == "auto" or theme not in THEMES:
        tl = html.lower()
        if any(x in tl for x in ["premium","gold","black"]): theme = "premium"
        elif any(x in tl for x in ["colorful","rainbow","kids"]): theme = "colorful"
        elif any(x in tl for x in ["business","report"]): theme = "business"
        elif any(x in tl for x in ["book","ebook","chapter"]): theme = "book"
        else: theme = "auto"
    T = THEMES[theme]

    # Extract chart/img/pagebreak/box tags
    chart_blocks = []
    img_blocks = []
    box_blocks = []

    def _extract(name, store):
        nonlocal html
        pat = r'<' + name + r'\b([^>]*)/?>'
        def _r(m):
            a = m.group(1)
            attrs = dict(_re.findall(r'(\w+)\s*=\s*"([^"]*)"', a))
            attrs.update(dict(_re.findall(r"(\w+)\s*=\s*'([^']*)'", a)))
            store.append(attrs)
            return '\n\n<p>&lt;&lt;' + name.upper() + '_B_' + str(len(store)-1) + '&gt;&gt;</p>\n\n'
        html = _re.sub(pat, _r, html, flags=_re.I|_re.S)

    _extract('chart', chart_blocks)
    _extract('img', img_blocks)
    _extract('box', box_blocks)

    # Extract pagebreak
    html = _re.sub(r'<pagebreak\s*/?>', '<p>&lt;&lt;PAGEBREAK_B&gt;&gt;</p>', html, flags=_re.I)

    # Extract tables
    tables = []
    def _tbl(m):
        inner = m.group(1)
        rows = _re.findall(r'<tr[^>]*>(.*?)</tr>', inner, flags=_re.I|_re.S)
        parsed = []
        for r in rows:
            cells = _re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=_re.I|_re.S)
            cells = [_re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            if cells: parsed.append(cells)
        tables.append(parsed)
        return '\n\n<p>&lt;&lt;TABLE_B_' + str(len(tables)-1) + '&gt;&gt;</p>\n\n'
    html = _re.sub(r'<table[^>]*>(.*?)</table>', _tbl, html, flags=_re.I|_re.S)

    # Parse text
    class _P(_HP):
        def __init__(self):
            super().__init__()
            self.blocks = []; self.tag = None; self.txt = []
        def _f(self):
            if self.tag:
                t = ''.join(self.txt).strip()
                if t: self.blocks.append((self.tag, t))
            self.tag = None; self.txt = []
        def handle_starttag(self, tag, attrs):
            tag = tag.lower()
            if tag in ('h1','h2','h3','h4','p','blockquote'):
                self._f(); self.tag = tag
            elif tag == 'li':
                self._f(); self.tag = 'li'
            elif tag == 'br':
                if self.tag: self.txt.append('\n')
            elif tag == 'hr':
                self._f(); self.blocks.append(('hr',''))
        def handle_endtag(self, tag):
            if tag.lower() in ('h1','h2','h3','h4','p','blockquote','li'):
                self._f()
        def handle_data(self, data):
            if self.tag: self.txt.append(data)

    parser = _P()
    try: parser.feed(html)
    except Exception as _e: print('[pdf] parse: ' + str(_e))
    parser._f()
    raw = parser.blocks

    # Expand placeholders
    final = []
    for bt, bx in raw:
        if bt == 'p':
            s = bx.strip()
            m = _re.match(r'<<(CHART|IMG|BOX)_B_(\d+)>>', s)
            if m:
                k = m.group(1).lower(); i = int(m.group(2))
                if k == 'chart' and i < len(chart_blocks): final.append(('chart', chart_blocks[i]))
                elif k == 'img' and i < len(img_blocks): final.append(('img', img_blocks[i]))
                elif k == 'box' and i < len(box_blocks): final.append(('box', box_blocks[i]))
                continue
            if s == '<<PAGEBREAK_B>>':
                final.append(('pagebreak', None))
                continue
            m = _re.match(r'<<TABLE_B_(\d+)>>', s)
            if m:
                i = int(m.group(1))
                if i < len(tables): final.append(('table', tables[i]))
                continue
        final.append((bt, bx))

    if not final:
        tt = _re.sub(r'<[^>]+>', '', html).strip()
        if tt: final = [('p', tt)]

    full = '\n'.join(str(b[1]) for b in final if isinstance(b[1], str))

    def _det(s):
        for name, pat in [('devanagari', r'[\u0900-\u097F]'), ('bengali', r'[\u0980-\u09FF]'),
                          ('gurmukhi', r'[\u0A00-\u0A7F]'), ('gujarati', r'[\u0A80-\u0AFF]'),
                          ('tamil', r'[\u0B80-\u0BFF]'), ('telugu', r'[\u0C00-\u0C7F]'),
                          ('kannada', r'[\u0C80-\u0CFF]'), ('malayalam', r'[\u0D00-\u0D7F]'),
                          ('arabic', r'[\u0600-\u06FF]'), ('chinese', r'[\u4E00-\u9FFF]'),
                          ('korean', r'[\uAC00-\uD7AF]'), ('japanese', r'[\u3040-\u30FF]'),
                          ('cyrillic', r'[\u0400-\u04FF]'), ('thai', r'[\u0E00-\u0E7F]')]:
            if _re.search(pat, s): return name
        return 'latin'
    script = _det(full)

    _BASE = "https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io@main/fonts/"
    FM = {
        'devanagari': (_BASE + "NotoSansDevanagari/hinted/ttf/NotoSansDevanagari-Regular.ttf", "NotoSansDevanagari-Regular.ttf"),
        'bengali':    (_BASE + "NotoSansBengali/hinted/ttf/NotoSansBengali-Regular.ttf",       "NotoSansBengali-Regular.ttf"),
        'gurmukhi':   (_BASE + "NotoSansGurmukhi/hinted/ttf/NotoSansGurmukhi-Regular.ttf",     "NotoSansGurmukhi-Regular.ttf"),
        'gujarati':   (_BASE + "NotoSansGujarati/hinted/ttf/NotoSansGujarati-Regular.ttf",     "NotoSansGujarati-Regular.ttf"),
        'tamil':      (_BASE + "NotoSansTamil/hinted/ttf/NotoSansTamil-Regular.ttf",           "NotoSansTamil-Regular.ttf"),
        'telugu':     (_BASE + "NotoSansTelugu/hinted/ttf/NotoSansTelugu-Regular.ttf",         "NotoSansTelugu-Regular.ttf"),
        'kannada':    (_BASE + "NotoSansKannada/hinted/ttf/NotoSansKannada-Regular.ttf",       "NotoSansKannada-Regular.ttf"),
        'malayalam':  (_BASE + "NotoSansMalayalam/hinted/ttf/NotoSansMalayalam-Regular.ttf",   "NotoSansMalayalam-Regular.ttf"),
        'arabic':     (_BASE + "NotoSansArabic/hinted/ttf/NotoSansArabic-Regular.ttf",         "NotoSansArabic-Regular.ttf"),
        'thai':       (_BASE + "NotoSansThai/hinted/ttf/NotoSansThai-Regular.ttf",             "NotoSansThai-Regular.ttf"),
        'cyrillic':   (_BASE + "NotoSans/hinted/ttf/NotoSans-Regular.ttf",                     "NotoSans-Regular.ttf"),
        'latin':      (_BASE + "NotoSans/hinted/ttf/NotoSans-Regular.ttf",                     "NotoSans-Regular.ttf"),
        'chinese':    ("https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Regular.otf"),
        'korean':     ("https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/Korean/NotoSansCJKkr-Regular.otf",            "NotoSansCJKkr-Regular.otf"),
        'japanese':   ("https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf",          "NotoSansCJKjp-Regular.otf"),
    }
    cd = _os.path.join(_os.getcwd(), ".saathi_fonts_cache")
    _os.makedirs(cd, exist_ok=True)

    def _dl(sn, bold=False):
        if sn not in FM: sn = 'latin'
        u, f = FM[sn]
        if bold:
            u = u.replace('-Regular', '-Bold'); f = f.replace('-Regular', '-Bold')
        p = _os.path.join(cd, f)
        if not _os.path.exists(p):
            try: _url.urlretrieve(u, p)
            except Exception as e: print('[pdf] font ' + str(e)); return None
        return p

    pp = _dl(script, False)
    bp = _dl(script, True) or pp

    pdf = _FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()
    pdf.set_fill_color(*T['bg']); pdf.rect(0, 0, pdf.w, pdf.h, 'F')
    pdf.set_text_color(*T['text'])

    ff = 'Helvetica'
    if pp:
        try:
            pdf.add_font('MF', '', pp)
            pdf.add_font('MF', 'B', bp if bp != pp else pp)
            ff = 'MF'
        except Exception as e: print('[pdf] fontload ' + str(e))

    def SF(style='', size=11, color=None):
        try: pdf.set_font(ff, style, size)
        except Exception: pdf.set_font('Helvetica', size=size)
        if color: pdf.set_text_color(*color)

    def _np(need=25):
        if pdf.get_y() + need > pdf.h - 25:
            pdf.add_page()
            pdf.set_fill_color(*T['bg']); pdf.rect(0, 0, pdf.w, pdf.h, 'F')

    title = None
    for b in final:
        if b[0] in ('h1','h2') and isinstance(b[1], str):
            title = b[1]; break

    if title:
        bh = pdf.h * 0.42
        pdf.set_fill_color(*T['header_band']); pdf.rect(0, 0, pdf.w, bh, 'F')
        pdf.set_fill_color(*T['accent']); pdf.rect(0, bh, pdf.w, 2, 'F')
        pdf.set_text_color(*T['header_text'])
        try: pdf.set_font(ff, 'B', 26)
        except Exception: pdf.set_font('Helvetica', 'B', 26)
        pdf.set_xy(20, bh * 0.32)
        pdf.multi_cell(pdf.w - 40, 12, title[:70], align='C')
        pdf.set_fill_color(*T['accent'])
        cy = bh * 0.32 + 30
        for i in range(3): pdf.ellipse(pdf.w/2 - 12 + i*12, cy, 5, 5, 'F')
        pdf.set_y(bh + 25)
        skipped = True
    else:
        skipped = False

    for bt, bd in final:
        if bt == 'pagebreak':
            pdf.add_page()
            pdf.set_fill_color(*T['bg']); pdf.rect(0, 0, pdf.w, pdf.h, 'F')
            continue

        if bt == 'chart':
            _np(90)
            data_json = bd.get('data', '[]')
            ctype = bd.get('type', 'line')
            ctitle = bd.get('title', '')
            entry = bd.get('entry'); stop = bd.get('stop'); target = bd.get('target')
            try:
                _draw_native_chart(pdf, data_json, x=18, y=pdf.get_y(), w=pdf.w-36, h=85, chart_type=ctype, title=ctitle, entry=entry, stop=stop, target=target)
                pdf.ln(90)
            except Exception as e:
                print(f"[pdf] native chart error: {e}")
            continue

        if bt == 'img':
            src = bd.get('src', '')
            try: w_img = float(bd.get('w', pdf.w - 36))
            except Exception: w_img = pdf.w - 36
            png = _download_image_bytes(src)
            if png:
                import tempfile as _tf
                with _tf.NamedTemporaryFile(suffix='.png', delete=False) as t:
                    t.write(png); tpath = t.name
                try:
                    _np(70)
                    y = pdf.get_y()
                    x = (pdf.w - w_img) / 2
                    pdf.image(tpath, x=x, y=y, w=w_img)
                    pdf.ln(4)
                except Exception as e: print('[pdf] img ' + str(e))
                finally:
                    try: _os.unlink(tpath)
                    except Exception: pass
            continue

        if bt == 'table':
            rows = bd
            if not rows: continue
            _np(20)
            ncol = max(len(r) for r in rows)
            cw = (pdf.w - 36) / ncol
            for ri, row in enumerate(rows):
                _np(12)
                if ri == 0:
                    y = pdf.get_y()
                    pdf.set_fill_color(*T['accent']); pdf.rect(18, y, pdf.w - 36, 8, 'F')
                    pdf.set_text_color(*T['header_text']); SF('B', 10, T['header_text'])
                else:
                    if ri % 2 == 0:
                        y = pdf.get_y()
                        if T['light']:
                            light = tuple(min(255, int(c*0.15 + 240)) for c in T['accent'])
                        else:
                            light = tuple(max(0, c-15) for c in T['bg'])
                        pdf.set_fill_color(*light); pdf.rect(18, y, pdf.w - 36, 8, 'F')
                    SF('', 10, T['text'])
                pdf.set_x(18)
                for ci in range(ncol):
                    cell = row[ci] if ci < len(row) else ''
                    pdf.cell(cw, 8, cell[:40], border=0, align='L')
                pdf.ln(8)
            pdf.ln(3)
            continue

        if bt == 'box':
            txt = bd.get('text', '') or bd.get('content', '')
            if txt:
                _np(20)
                y = pdf.get_y()
                pdf.set_fill_color(*T['accent']); pdf.rect(18, y, pdf.w - 36, 2, 'F')
                pdf.set_xy(22, y + 4)
                SF('', 11, T['text'])
                pdf.multi_cell(pdf.w - 44, 6.5, txt)
                pdf.ln(4)
            continue

        if not (isinstance(bd, str) and bd.strip()) and bt != 'hr':
            continue
        if not skipped and bt in ('h1','h2') and bd == title:
            skipped = True; continue
        skipped = True
        _np(25)

        if bt == 'h1':
            pdf.ln(4); y = pdf.get_y()
            pdf.set_fill_color(*T['accent']); pdf.rect(18, y, 4, 11, 'F')
            pdf.set_xy(26, y); SF('B', 17, T['accent'])
            pdf.multi_cell(pdf.w - 44, 10, bd)
            pdf.set_draw_color(*T['accent2']); pdf.set_line_width(0.4)
            pdf.line(18, pdf.get_y() + 1, 60, pdf.get_y() + 1)
            pdf.ln(4)
        elif bt == 'h2':
            pdf.ln(3); y = pdf.get_y()
            if T['light']:
                bc = tuple(min(255, int(c*0.15 + 240)) for c in T['accent'])
            else:
                bc = T['accent']
            pdf.set_fill_color(*bc); pdf.rect(18, y, pdf.w - 36, 12, 'F')
            pdf.set_fill_color(*T['accent']); pdf.rect(18, y, 3, 12, 'F')
            pdf.set_xy(26, y + 3)
            SF('B', 14, T['accent2'] if T['light'] else T['accent'])
            pdf.multi_cell(pdf.w - 48, 8, bd)
            pdf.ln(4)
        elif bt == 'h3':
            pdf.ln(2); SF('B', 13, T['text']); pdf.multi_cell(0, 8, bd); pdf.ln(2)
        elif bt == 'h4':
            SF('B', 11, T['muted']); pdf.multi_cell(0, 7, bd); pdf.ln(2)
        elif bt == 'li':
            SF('', 11, T['text']); pdf.set_x(24)
            pdf.set_text_color(*T['accent']); pdf.cell(6, 6, chr(0x25CF), ln=0)
            pdf.set_text_color(*T['text']); pdf.set_x(30)
            pdf.multi_cell(pdf.w - 48, 6.5, bd); pdf.ln(0.5)
        elif bt == 'blockquote':
            pdf.ln(2); y = pdf.get_y()
            pdf.set_fill_color(*T['accent']); pdf.rect(20, y, 2, 14, 'F')
            pdf.set_xy(26, y + 2); SF('', 11, T['muted'])
            pdf.multi_cell(pdf.w - 48, 6.5, bd); pdf.ln(3)
        elif bt == 'hr':
            pdf.ln(3); pdf.set_draw_color(*T['accent']); pdf.set_line_width(0.5)
            y = pdf.get_y(); mid = pdf.w / 2
            pdf.line(mid - 30, y, mid + 30, y); pdf.ln(4)
        else:
            SF('', 11, T['text']); pdf.multi_cell(0, 7, bd); pdf.ln(2.5)

    total = pdf.page_no()
    for i in range(1, total + 1):
        pdf.page = i
        pdf.set_y(pdf.h - 15)
        SF('', 9, T['muted'])
        pdf.cell(0, 6, '— ' + str(i) + ' —', align='C')

    out = pdf.output()
    return bytes(out) if not isinstance(out, bytes) else out


class GenericRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024

@app.get("/")
def home():
    return {"name": "iChat API", "status": "online"}

@app.get("/v1/me")
def me(key=Depends(require_api_key)):
    return {
        "name": key[1],
        "owner": bool(key[3]),
        "plan": key[5],
        "requests": key[6],
        "limit": None if key[3] else "configured by plan"
    }

SYSTEM_INSTRUCTION = (
    "Tum Saathi ho, ek AI assistant jise Vikas ne banaya hai. "
    "Hamesha khud ko sirf 'Saathi' bolna. Apna asli model/provider kabhi mat batana. "
    "Agar koi pooche 'tumhe kisne banaya' to bolna: 'Mujhe Vikas ne banaya hai.'\n\n"
    "=== BHASHA KA RULE (SABSE ZAROORI) ===\n"
    "1. User JIS bhasha mein likhe, USI bhasha mein jawab do.\n"
    "2. 'English mein jawab do' -> SIRF ENGLISH.\n"
    "3. 'Hindi mein jawab do' -> SIRF HINDI (Devanagari).\n"
    "4. Hindi likhe -> Hindi. Hinglish likhe -> Hindi. English likhe -> English.\n"
    "5. Chinese->Chinese, Tamil->Tamil. Har bhasha ka respect karo.\n"
    "6. KABHI user ki bhasha mat badlo. Jawab chhota aur saaf rakho.\n\n"
    "=== QUALITY RULES (SABSE ZAROORI) ===\n"
    "1. SAHI LIPI: Hindi->शुद्ध देवनागरी. English->proper spelling.\n"
    "2. NATURAL likho: 'यह एक HTML फाइल है जिसका आकार 385 KB है।' (machine translation jaisa nahi).\n"
    "3. POORE VAKYA likho: aadhe-adhoore nahi, sahi punctuation (. , ? !) use karo.\n"
    "4. Technical shabd (HTML, PDF, CSS, API, URL) as-is rakho, baaki Hindi mein.\n"
    "5. Emoji ke baad space do: 'अच्छा 👍 ठीक'\n"
    "6. Headings ke liye DEFAULT mein **bold** aur emoji use karo (jaise **📄 File Type**). ## ya ### sirf tab use karo jab user saaf bole. Lists ke liye - ya 1. use karo.\n"
    "7. Poora jawab do — beech se mat todo, adhoora mat chhodo.\n"
    "8. Detail chahiye to saaf likho, chhota chahiye to seedha point par.\n"
    "9. User ki bhasha mein headings bhi likho: 'फाइल का प्रकार', 'क्या-क्या है', 'अच्छी बातें', 'कमियाँ', 'सुधार', 'रेटिंग'.\n"
    "10. Emojis use karo headings mein (📄 📋 ✅ ⚠️ 🔧 🌟) jaisi reference mein thi."
)


def _call_openrouter_vision(prompt: str, images: list) -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise HTTPException(503, "OPENROUTER_API_KEY set nahi hai")

    content = [{"type": "text", "text": prompt or "Is photo me kya hai? Puri detail batao."}]
    for img in images[:3]:
        url = img.dataUrl or ""
        if not url.startswith("data:image"):
            continue
        content.append({
            "type": "image_url",
            "image_url": {"url": url},
        })

    models_to_try = [
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.2-11b-vision-instruct:free",
        "qwen/qwen-2-vl-7b-instruct:free",
        "openrouter/free",
    ]

    last_err = None
    for model in models_to_try:
        try:
            r = _req.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": content},
                    ],
                },
                timeout=300,
            )
            if r.status_code != 200:
                last_err = f"{model}: HTTP {r.status_code}"
                continue
            data = r.json()
            choices = data.get("choices") or []
            if not choices:
                last_err = f"{model}: no choices"
                continue
            txt = (choices[0].get("message", {}).get("content") or "").strip()
            if txt:
                return txt
        except Exception as e:
            last_err = f"{model}: {e}"

    raise HTTPException(500, f"Vision fail: {last_err}")


import re as _re

def _detect_action(msg: str) -> str:
    """User ke message se samjho kya banane ka hai."""
    m = (msg or "").lower()
    # ═══ STEP 1: LAMBA MESSAGE = FILE UPLOAD → हमेशा ANALYZE ═══
    if len(msg) > 1500:
        return "analyze"
    # ═══ STEP 2: FILE MARKERS ═══
    if '=== file:' in m or '===file:' in m:
        return "analyze"
    if 'user ne neeche file bheji' in m or 'user ne neeche file bheja' in m:
        return "analyze"
    if 'file ka naam:' in m and '---' in m:
        return "analyze"
    if 'file bheji' in m or 'file bheja' in m or 'file check' in m or 'file padho' in m or 'file dekho' in m or 'file batao' in m:
        return "analyze"
    # ═══ STEP 3: Code + analyze words ═══
    has_code = any(x in m for x in ['<!doctype', '<html', '<body', '<div', 'function ', 'const ', 'class ', 'def ', 'import ', 'public class'])
    has_analyze = any(x in m for x in ['analyze', 'check karo', 'batao isme', 'isme kya', 'kya kya hai', 'review karo', 'dekho isko', 'sahi hai ya', 'theek hai ya', 'quality batao', 'improve karo'])
    if has_code and has_analyze:
        return "analyze"
    # PDF
    if _re.search(r"\bpdf\b|पीडीएफ|पी\.डी\.एफ|document banao|report banao|docx banao|letter banao", m):
        return "pdf"
    # Website
    if _re.search(r"\bwebsite\b|\bsite\b|वेबसाइट|webpage|landing page|html page|homepage banao|web page", m):
        return "website"
    # Image (banane ke liye — dekhne ke liye nahi)
    if _re.search(r"(image|photo|picture|तस्वीर|फोटो|चित्र|pic).*(banao|banaao|bana do|generate|create|banade|बनाओ|बनाओ|बना दो|बनाएं|बनायें)", m) or \
       _re.search(r"(banao|banaao|generate|create|bana do).*(image|photo|picture|तस्वीर|फोटो|चित्र)", m):
        return "image"
    # ═══ Kahani / Story / Poem ═══
    if any(x in m for x in ["kahani","कहानी","story","किस्सा","कविता","poem","शायरी","baal","baat","बात","joke","चुटकुला"]):
        return "chat"
    return "chat"



def _generate_pdf_playwright(html_content: str) -> bytes:
    """Playwright (Chromium) se HTML ko PDF me convert karo."""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        # Chromium launch karo (Render Docker ke liye no-sandbox zaroori hai)
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page()
        
        # Agar AI ne adhoora HTML diya hai, to use complete karo
        if "<!doctype" not in html_content.lower() and "<html" not in html_content.lower():
            html_content = f"<html><head><meta charset='utf-8'></head><body>{html_content}</body></html>"
            
        # HTML load karo
        page.set_content(html_content, wait_until="networkidle")
        
        # PDF generate karo (A4 size, background colors ke saath)
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "30px", "bottom": "30px", "left": "30px", "right": "30px"}
        )
        browser.close()
        return pdf_bytes


@app.post("/v1/chat")
def chat(body: ChatRequest, key=Depends(require_api_key)):
    record_usage(key, "chat")

    # Images extract karo
    images = [a for a in (body.attachments or []) if a.kind == "photo" and a.dataUrl]

    # ═══ SABSE PEHLE action detect karo ═══
    action = _detect_action(body.message)

    # ═══ PRIORITY: Agar user PDF/website/image banane ko bola hai, to WAHI karo ═══
    # (image bheji ho ya na ho — explicit request ko priority mile)
    if action in ("pdf", "website", "image"):
        # Agar image bhi hai, to use content me mention karo
        if images:
            try:
                _img_analysis = _call_vision_v2(body.message, images)
                if _img_analysis:
                    body.message = body.message + "\n\n[User ne jo image bheji hai uska analysis: " + _img_analysis[:1500] + "]"
            except Exception as _e:
                print(f"[chat] vision enrich failed: {_e}")
        # Neeche wale specific action handlers chalenge (pdf/website/image)
    elif images:
        # Image bheji hai aur koi specific action nahi maanga → vision path
        raw = _call_vision_v2(body.message, images)
        reply = _polish_vision_reply(raw, body.message)
        return {
            "service": "chat",
            "reply": reply,
            "model": "saathi-vision",
        }

    if action == "analyze":
        system = (
            "Tum ek professional code reviewer ho. User ne file bheji hai. "
            "CHHOTA aur SAARBHUT analysis do (max 200 words):\n\n"
            "## 📄 File Type\n"
            "[HTML/CSS/JS/Python]\n\n"
            "## 📋 Kya-Kya Hai\n"
            "- [4-6 main points]\n\n"
            "## ✅ Achhi Baatein\n"
            "- [3-4 points]\n\n"
            "## ⚠️ Kamiyan\n"
            "- [3-4 points]\n\n"
            "## 🔧 Improvements\n"
            "- [3-4 suggestions]\n\n"
            "## 🌟 Rating: X/10\n\n"
            "Chhota rakho. User ki bhasha mein."
        )
        try:
            reply = _call_groq(body.message, system=system)
            return {"service": "chat", "reply": reply, "model": "saathi", "kind": "analysis"}
        except Exception as e:
            return {"service": "chat", "reply": f"Analysis mein problem: {e}", "model": "saathi"}

    if action == "pdf":
        try:
            import base64 as _b64
            system = (
                "Tum ek WORLD-CLASS web designer ho. User ki request ke hisab se ek MASSIVE aur COMPLETE HTML document banao.\n\n"
                "🚨 ULTRA-STRICT RULES (Inko todne par tum FAIL ho jaoge):\n"
                "1. 'Below is a chart' ya 'Here is a table' KABHI MAT LIKHNA. Tumhe ASLI HTML CODE dena hai.\n"
                "2. HAR 2-3 PARAGRAPH KE BAAD ek chart ya table ka code zaroor dalna hai. Bina chart/table ke text mat chhodo.\n"
                "3. Page break ke liye HAMESHA <div style='page-break-before: always;'></div> use karo. Heading me 'Page 1' ya 'Page 2' KABHI MAT LIKHNA.\n"
                "4. CHART KE LIYE ye exact format copy karo (Data change kar sakte ho):\n"
                "   <img src=\"https://quickchart.io/chart?c={type:%27bar%27,data:{labels:[%27Q1%27,%27Q2%27],datasets:[{label:%27Sales%27,data:[50,60]}]}}\" style=\"width:100%; max-width:600px; margin: 20px 0; border-radius: 8px;\" />\n"
                "5. TABLE KE LIYE ye exact format copy karo:\n"
                "   <table style=\"width:100%; border-collapse: collapse; margin: 20px 0; background: #2a2a34; color: #ececf0;\"><tr style=\"background: #3a3a46;\"><th style=\"padding:12px; border:1px solid #444;\">Strategy</th><th style=\"padding:12px; border:1px solid #444;\">Risk</th></tr><tr><td style=\"padding:12px; border:1px solid #444;\">Scalping</td><td style=\"padding:12px; border:1px solid #444;\">High</td></tr></table>\n"
                "6. DARK THEME (Agar user bole): Body tag aisa hona chahiye -> <body style='background-color: #121216; color: #ececf0; font-family: Arial, sans-serif; padding: 40px; line-height: 1.6;'>\n"
                "7. Headings ko style do: <h1 style='color: #10a37f; border-bottom: 2px solid #10a37f; padding-bottom: 10px;'>Title</h1>\n\n"
                "═══ OUTPUT FORMAT ═══\n"
                "Sirf PURE HTML return karo. <!DOCTYPE html> se shuru karo, </html> par khatam. Koi markdown (```) nahi.\n"
                "Chalo shuru karo — POORA 10 page ka detailed HTML banao, aur har page par chart ya table zaroor dalo."
            )
            
            html_body = _call_groq(body.message, system=system).strip()
            if "```" in html_body:
                html_body = html_body.replace("```html", "").replace("```", "").strip()
            
            pdf_bytes = _generate_pdf_playwright(html_body)
            pdf_b64 = _b64.b64encode(pdf_bytes).decode("utf-8")
            
            return {
                "service": "chat",
                "reply": "Yeh raha aapka PDF.",
                "pdf_base64": pdf_b64,
                "filename": "saathi.pdf",
                "model": "saathi",
                "kind": "pdf",
            }
        except Exception as e:
            print(f"[pdf] error: {e}")
            return {"service": "chat", "reply": f"PDF banane mein problem aayi: {e}", "model": "saathi"}

    if action == "website":
        try:
            system = (
                "Tum ek expert full-stack web developer ho. User ki request ke hisab se ek "
                "COMPLETE, FULLY WORKING HTML website banao (HTML + inline CSS + JS). "
                "Sirf pure HTML code return karo, koi explanation nahi, koi markdown nahi. "
                "Shuru <!DOCTYPE html> se, khatam </html> par.\n"
                "ZAROORI RULES:\n"
                "1. IMAGES: Sirf picsum.photos ya placehold.co use karo. source.unsplash.com KABHI NAHI (band hai).\n"
                "2. HAR BUTTON KAAM KARE: nav links smooth scroll, Get Started contact pe, hamburger JS toggle.\n"
                "3. IMAGE UPLOAD: input type=file with preview.\n"
                "4. EDIT: headings pe contenteditable=true, Edit button.\n"
                "5. ADD/DELETE: Add Item button, har item pe delete button.\n"
                "6. FORM: submit pe alert + reset.\n"
                "7. SMOOTH SCROLL: html{scroll-behavior:smooth}.\n"
                "8. HOVER EFFECTS: har button aur card pe.\n"
                "9. MOBILE RESPONSIVE: media queries.\n"
                "10. CSS VARIABLES colors ke liye.\n"
                "11. Koi button dead nahi — har click pe action.\n"
                "\n📋 CHANGES / क्या किया (code ke neeche likho):\n"
                "- [Kya-kya banaya/badla — list mein]\n"
                "\n✅ FEATURES ADD KIYE:\n"
                "- [Naye features]\n"
                "\n📝 Aap check kariye:\n"
                "Koi galti ho, kuch aur chahiye, ya samajh na aaye to bataaiye — "
                "main turant theek kar dunga."
            )
            html = _call_groq(body.message, system=system).strip()
            if "```" in html:
                html = html.replace("```html", "").replace("```", "").strip()
            return {
                "service": "chat",
                "reply": "Yeh raha aapki website ka code.",
                "html": html,
                "filename": "index.html",
                "model": "saathi",
                "kind": "website",
            }
        except Exception as e:
            return {"service": "chat", "reply": f"Website banane mein problem aayi: {e}", "model": "saathi"}

    if action == "image":
        try:
            import urllib.parse as _up
            encoded = _up.quote(body.message)
            image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024"
            return {
                "service": "chat",
                "reply": "Yeh rahi aapki image.",
                "image_url": image_url,
                "model": "saathi",
                "kind": "image",
            }
        except Exception as e:
            return {"service": "chat", "reply": f"Image banane mein problem aayi: {e}", "model": "saathi"}

    # Warna normal text chat
    try:
        result = get_response(body.message, history=body.history or [], lang_pref=body.lang_pref)
    except TypeError:
        try:
            result = get_response(body.message, history=body.history or [])
        except TypeError:
            result = get_response(body.message)
    if isinstance(result, dict):
        return {
            "service": "chat",
            "reply": result.get("reply") or "",
            "sources": result.get("sources", []),
            "model": "saathi"
        }
    return {
        "service": "chat",
        "reply": result if isinstance(result, str) else str(result),
        "model": "saathi"
    }


import os as _os
import requests as _requests
from dotenv import load_dotenv as _load_dotenv

_load_dotenv()

def _call_groq(prompt: str, system: str = "") -> str:
    """Groq se reply laata hai. Poora output deta hai, fallback OpenRouter se."""
    key = _os.environ.get("GROQ_API_KEY")
    if not key:
        try:
            return _call_openrouter(prompt, system)
        except Exception:
            raise HTTPException(503, "GROQ_API_KEY set nahi hai")
    try:
        r = _requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": (
                    ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]
                ),
                "max_tokens": 32000,
                "temperature": 0.6,
            },
            timeout=300,
        )
        if r.status_code != 200:
            print(f"[groq] HTTP {r.status_code}, OpenRouter fallback")
            return _call_openrouter(prompt, system)
        data = r.json()
        content = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        finish = data.get("choices", [{}])[0].get("finish_reason", "")
        if finish == "length" or (content and not content.rstrip().endswith((">", "}", ")", "]", ".", "!", "?", "`"))):
            print(f"[groq] Response cut ho gaya (finish={finish}), OpenRouter try")
            try:
                alt = _call_openrouter(prompt, system)
                if alt and len(alt) > len(content):
                    return alt
            except Exception:
                pass
        return content
    except HTTPException:
        raise
    except Exception as e:
        try:
            return _call_openrouter(prompt, system)
        except Exception:
            raise HTTPException(500, f"Groq crash: {e}")


def _call_openrouter(prompt: str, system: str = "") -> str:
    """OpenRouter se reply laata hai (fallback ke liye)."""
    key = _os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise HTTPException(503, "OPENROUTER_API_KEY set nahi hai")
    try:
        r = _requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openrouter/free",
                "messages": (
                    ([{"role": "system", "content": system}] if system else []) +
                    [{"role": "user", "content": prompt}]
                ),
                "max_tokens": 32000,
            },
            timeout=300,
        )
        if r.status_code != 200:
            raise HTTPException(500, f"OpenRouter error: {r.status_code}")
        return (r.json().get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"OpenRouter crash: {e}")


@app.post("/v1/image")
def image(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "image")
    import urllib.parse
    prompt = (body.prompt or "").strip()
    if not prompt:
        raise HTTPException(400, "Prompt khaali nahi ho sakta")
    width = body.width or 1024
    height = body.height or 1024
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )
    return {
        "service": "image",
        "image_url": image_url,
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": "saathi-image"
    }

@app.post("/v1/video")
def video(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "video")
    raise HTTPException(501, "Video model/provider अभी connect नहीं है")

@app.post("/v1/voice")
def voice(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "voice")
    raise HTTPException(501, "Voice model/provider अभी connect नहीं है")

@app.post("/v1/pdf")
def pdf(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "pdf")
    import base64
    from io import BytesIO
    from xhtml2pdf import pisa

    system = (
        "Tum ek professional document writer ho. User ki request ke hisab se "
        "ek achha HTML document banao (title, headings, paragraphs). "
        "Sirf pure HTML return karo — <html> se shuru, </html> par khatam. "
        "Sirf HTML content, koi CSS, koi markdown, koi explanation nahi."
    )
    html_body = _call_groq(body.prompt, system=system)
    html_body = html_body.strip()
    if "```" in html_body:
        html_body = html_body.replace("```html", "").replace("```", "").strip()

    pdf_bytes = _generate_pdf_playwright(html_body)
    pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    return {
        "pdf_base64": pdf_b64,
        "filename": "saathi.pdf",
    }

@app.post("/v1/code")
def code(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "code")
    raise HTTPException(501, "Coding model अभी connect नहीं है")

@app.post("/v1/website")
def website(body: GenericRequest, key=Depends(require_api_key)):
    record_usage(key, "website")
    system = (
                "Tum ek expert full-stack web developer ho. User ki request ke hisab se ek "
                "COMPLETE, FULLY WORKING HTML website banao (HTML + inline CSS + JS). "
                "Sirf pure HTML code return karo, koi explanation nahi, koi markdown nahi. "
                "Shuru <!DOCTYPE html> se, khatam </html> par.\n"
                "ZAROORI RULES:\n"
                "1. IMAGES: Sirf picsum.photos ya placehold.co use karo. source.unsplash.com KABHI NAHI (band hai).\n"
                "2. HAR BUTTON KAAM KARE: nav links smooth scroll, Get Started contact pe, hamburger JS toggle.\n"
                "3. IMAGE UPLOAD: input type=file with preview.\n"
                "4. EDIT: headings pe contenteditable=true, Edit button.\n"
                "5. ADD/DELETE: Add Item button, har item pe delete button.\n"
                "6. FORM: submit pe alert + reset.\n"
                "7. SMOOTH SCROLL: html{scroll-behavior:smooth}.\n"
                "8. HOVER EFFECTS: har button aur card pe.\n"
                "9. MOBILE RESPONSIVE: media queries.\n"
                "10. CSS VARIABLES colors ke liye.\n"
                "11. Koi button dead nahi — har click pe action.\n"
                "\n📋 CHANGES / क्या किया (code ke neeche likho):\n"
                "- [Kya-kya banaya/badla — list mein]\n"
                "\n✅ FEATURES ADD KIYE:\n"
                "- [Naye features]\n"
                "\n📝 Aap check kariye:\n"
                "Koi galti ho, kuch aur chahiye, ya samajh na aaye to bataaiye — "
                "main turant theek kar dunga."
        "user ki request ke hisab se daalo."
    )
    html = _call_groq(body.prompt, system=system)
    html = html.strip()
    if "```" in html:
        html = html.replace("```html", "").replace("```", "").strip()
    return {"html": html, "filename": "index.html"}

VISION_SYSTEM_INSTRUCTION = (
    "Tum Saathi ho — ek insaan jaisa madadgaar saathi. User ne tumhe kuch bheja hai "
    "(photo, video, file, kuch bhi). Tumhara kaam hai usse DEKHNA, SAMJHNA, aur "
    "insaan ki tarah jawab dena.\n\n"
    "═══ SABSE PEHLA NIYAM ═══\n"
    "KABHI MAT KEHNA: 'file mil gayi', 'photo mil gayi', 'video mil gaya', "
    "'attachment mila', 'yeh ek photo hai'. User ko pata hai usne kya bheja. "
    "Use batao ki us cheez ke ANDAR kya hai.\n\n"
    "═══ JAWAB KA DHANCHA — 4 HISSE, IS KARM MEIN ═══\n\n"
    "◆ HISSA 1 — VIVARAN (kya-kya hai, kahan-kahan)\n"
    "Jo bhi bheja gaya hai uska POORA bayaan do. Jaise koi insaan aankhon ke saamne "
    "rakh kar gin raha ho:\n"
    "- Photo ho to: kya dikh raha hai, upar kya likha hai, neeche kya, beech mein kya, "
    "rang kaise hain, text padh kar do, button/icon/box/chart — jo bhi dikh raha hai "
    "uska naam lekar batao. Kahan hai yeh bhi batao — 'upar dayein taraf', 'beech mein', "
    "'neeche bayen'.\n"
    "- Video ho to: kitna lamba hai, kya-kya dikha, kya bola gaya, shuru se ant tak kram mein.\n"
    "- File/PDF ho to: kitne panne, har panne par kya, sheershak kya.\n"
    "Chhota-sa vivaran kaafi nahi. Poora kholkar batao — user ko lage ki tumne sach mein "
    "usse dekha hai, dhyaan se dekha hai.\n\n"
    "◆ HISSA 2 — KAAM (yeh kis kaam ki hai)\n"
    "Ab batao yeh cheez asal mein kis kaam aati hai, kahan istemal hoti hai, kyun bani "
    "hoti hai. Jaise: 'Yeh chart trading mein kaam aata hai — isse pata chalta hai ki "
    "sone ka bhaav upar jayega ya neeche. Log ise dekh kar tay karte hain ki kharidna "
    "hai ya bechna hai.'\n\n"
    "◆ HISSA 3 — SALAH (achha hai ya bura)\n"
    "Yahan imaandaar bano — dost ki tarah.\n"
    "- Achhi cheez ho to: 'Yeh aapke kaam ki cheez hai, ise sambhal kar rakhiye.'\n"
    "- Koi khatra, dhokha, galat baat ho to: 'Dhyaan dijiye — isse door rahiye.'\n"
    "- Koi kami ya galti ho to: 'Ismein ek baat sudhaarni chahiye — [kya].'\n"
    "Kabhi jhooti tareef mat karo. Kabhi bevajah dar mat dikhao. Jaisa dikh raha hai, "
    "waisa saaf kaho — pyaar se, par sach.\n\n"
    "◆ HISSA 4 — SAWAAL (aage kya?)\n"
    "Aakhir mein user se poochho — insaan ki tarah:\n"
    "- 'Kya aap iske baare mein kuch aur jaanna chahte hain?'\n"
    "- 'Aap isse kuch banwana chahte hain — jaise PDF, card, ya kuch aur?'\n"
    "- 'Kya main ismein kuch sudhaar kar sakta hoon?'\n"
    "Sawaal poochne ka matlab baatcheet jaari rakhna hai — user ko akela mat chhodo.\n\n"
    "═══ BHASHA KA RULE ═══\n"
    "User jis bhasha mein likhe, usi bhasha mein jawab do. Natural Hinglish/Hindi likho — "
    "'maine dekha', 'samjha', 'lagta hai', 'bataiye', 'theek hai', 'achha'. "
    "Machine translation jaise shabd MAT use karo — 'mulf fahaasat', 'pehchaan banayi', "
    "'bikau pressure', 'status' jaisi ajeeb bhasha nahi. Seedhi, aam bolchaal ki bhasha.\n\n"
    "Lambaai: jitna vishay maangta hai utna. Chhota mat karo, badha-chadha bhi mat karo.\n\n"
    "Agar user ne saath mein kuch likha hai (jaise 'iski PDF banao') to pehle upar ke "
    "chaaron hisse poore karo, PHIR jo maanga gaya kaam karo."
)


def _polish_vision_reply(vision_text: str, user_message: str) -> str:
    """Vision model ke tukde-tukde jawab ko saaf, insaan-jaisi bhasha mein likho.
    User ki bhasha detect karke usi mein likho — Hindi, English, Arabic, Tamil, jo bhi."""
    if not vision_text or not vision_text.strip():
        return vision_text

    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return vision_text

    system = (
        "Tum ek expert editor ho. Neeche ek vision AI ka raw observation hai — "
        "photo/video/file mein kya-kya dikha, uski tafseel. Yeh raw text tuti-phooti "
        "bhasha mein hai, shabd bigde hue hain (jaise 'HISLA' ka matlab 'hissa', "
        "'kish' ka matlab 'kis', 'aaaj' ka matlab 'aaj').\n\n"
        "Tumhara kaam: is raw text ko uthao aur ek SAFA, INSAN-JAISI bhasha mein "
        "dobara likho. Matlab badalna NAHI — sirf bhasha sudhaarni hai.\n\n"
        "═══ BHASHA KA RULE (SABSE ZAROORI) ═══\n"
        "User ne jo message bheja hai, usi bhasha mein jawab likho:\n"
        "- User Hindi/Hinglish mein likhe → Hindi/Hinglish mein likho (Devanagari + Roman mix, jaise log bolte hain)\n"
        "- User English mein likhe → English mein likho\n"
        "- User Arabic mein likhe → Arabic mein likho\n"
        "- User Tamil/Bengali/Marathi/jo bhi bhasha → usi bhasha mein likho\n"
        "- Agar user ne kuch likha hi nahi (sirf photo bheji) → Hindi/Hinglish mein likho\n\n"
        "═══ JAWAB KA DHANCHA — 4 HISSE (HAMESHA) ═══\n"
        "Ye chaar hisse saaf-saaf headings ke saath likho:\n\n"
        "1. KYA-KYA HAI (poora vivaran — kya dikha, kahan-kahan, kya likha hai)\n"
        "2. KIS KAAM KI HAI (yeh cheez kis kaam aati hai, kahan istemal hoti hai)\n"
        "3. SALAH (kya sahi hai, kya galat; koi khatra to door raho; achhi cheez to rakho)\n"
        "4. SAWAAL (user se aage poochho — aur kuch jaanna hai? kuch banwana hai?)\n\n"
        "═══ BHASHA KI SAFAAI ═══\n"
        "Ye shabd KABHI mat likho: 'HISLA', 'HESSLA', 'kish', 'aaaj', 'kahaat', "
        "'mulf fahaasat', 'bikau', 'pehchaan banayi', 'tukde'.\n"
        "Inki jagah aam bolchaal ke shabd: 'hissa', 'kis', 'aaj', 'kahan', "
        "'mukhya baatein', 'bikri ka dabav', 'upar gaya', 'tez'.\n\n"
        "Lambaai: jitna vishay maangta hai utna. Chhota mat karo, badha-chadha bhi mat karo.\n"
        "Sirf saaf-suthra, insaan-jaisa jawab do. Koi bhumika nahi, koi 'yaha hai aapka' nahi."
    )

    user_prompt = (
        "USER KA MESSAGE:\n" + (user_message or "(kuch nahi likha, sirf file bheji)") + "\n\n"
        "VISION AI KA RAW OUTPUT (ise saaf karke dobara likho):\n" + vision_text
    )

    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 32000,
                "temperature": 0.4,
            },
            timeout=120,
        )
        if r.status_code != 200:
            return vision_text
        data = r.json()
        choices = data.get("choices") or []
        if not choices:
            return vision_text
        polished = (choices[0].get("message", {}).get("content") or "").strip()
        return polished if polished else vision_text
    except Exception:
        return vision_text


def _strip_markdown(text: str) -> str:
    """Jawab se *** , ** , ## , ### jaise markdown symbols hata do.
    Sirf saaf plain text rakho — headings, bullets, sab as-is."""
    if not text:
        return text
    import re as _r
    t = text
    # Triple asterisk/underscore
    t = _r.sub(r'\*\*\*+', '', t)
    t = _r.sub(r'___+', '', t)
    # Double asterisk / underscore (bold/italic)
    t = _r.sub(r'\*\*', '', t)
    t = _r.sub(r'(?<!\w)__(?!\w)', '', t)
    # Headings: ## ### etc — hata do hashes
    t = _r.sub(r'(?m)^\s*#{1,6}\s*', '', t)
    # Horizontal rule --- or ___
    t = _r.sub(r'(?m)^\s*[-*_]{3,}\s*$', '', t)
    # Inline code backticks
    t = t.replace('`', '')
    # Leading asterisk in bullets -> convert to bullet dot
    t = _r.sub(r'(?m)^\s*\*\s+', '• ', t)
    # Stray asterisks leftover
    t = _r.sub(r'(?<!\w)\*(?!\w)', '', t)
    # Extra blank lines
    t = _r.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def _call_vision_v2(prompt: str, images: list) -> str:
    content = [{"type": "text", "text": prompt or "Is photo me kya hai? Puri detail batao."}]
    for img in images[:3]:
        url = img.dataUrl or ""
        if not url.startswith("data:image"):
            continue
        content.append({"type": "image_url", "image_url": {"url": url}})

    errors = []
    import time as _time

    # Groq (तेज़, पर 429 आ सकता है — इसलिए 3 बार कोशिश)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        groq_models = ["qwen/qwen3.8-27b"]
        for model in groq_models:
            for attempt in range(3):
                try:
                    r = _req.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": "Bearer " + groq_key, "Content-Type": "application/json"},
                        json={"model": model, "messages": [{"role": "system", "content": SYSTEM_INSTRUCTION}, {"role": "user", "content": content}], "max_tokens": 2000},
                        timeout=120,
                    )
                    if r.status_code == 429:
                        wait = (attempt + 1) * 2
                        errors.append("groq/" + model + ": 429 (wait " + str(wait) + "s)")
                        _time.sleep(wait)
                        continue
                    if r.status_code != 200:
                        errors.append("groq/" + model + ": " + str(r.status_code))
                        break
                    data = r.json()
                    choices = data.get("choices") or []
                    if choices:
                        txt = (choices[0].get("message", {}).get("content") or "").strip()
                        if txt:
                            return txt
                    break
                except Exception as e:
                    errors.append("groq/" + model + ": " + str(e))
                    break

    # OpenRouter (भरोसेमंद फॉलबैक) — अब चालू मॉडल्स
    or_key = os.environ.get("OPENROUTER_API_KEY")
    if or_key:
        or_models = [
            "qwen/qwen3.8-27b:free",
            "google/gemma-4-31b-it:free",
            "nvidia/nemotron-nano-12b-v2-vl:free",
            "thinkingmachines/inkling-small:free",
        ]
        for model in or_models:
            try:
                r = _req.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": "Bearer " + or_key, "Content-Type": "application/json", "HTTP-Referer": "https://saathi-ai-y48j.onrender.com", "X-Title": "Saathi AI"},
                    json={"model": model, "messages": [{"role": "system", "content": SYSTEM_INSTRUCTION}, {"role": "user", "content": content}], "max_tokens": 2000},
                    timeout=120,
                )
                if r.status_code != 200:
                    errors.append("or/" + model + ": " + str(r.status_code))
                    continue
                data = r.json()
                choices = data.get("choices") or []
                if choices:
                    txt = (choices[0].get("message", {}).get("content") or "").strip()
                    if txt:
                        return txt
            except Exception as e:
                errors.append("or/" + model + ": " + str(e))

    err_text = " | ".join(errors[-6:]) if errors else "no keys"
    raise HTTPException(500, "Vision fail: " + err_text)

class TitleRequest(BaseModel):
    message: Optional[str] = ""
    image: Optional[str] = None


def _title_from_text(text: str) -> str:
    if not text or not text.strip():
        return ""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        t = text.strip().replace("\n", " ")
        return t[:40] + ("…" if len(t) > 40 else "")
    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": "User ke message ka 3-6 shabd ka chat title banao. Sirf title likho, koi quote nahi, koi punctuation nahi. User ki bhasha mein hi rakho. Example: 'Gold chart analysis', 'Pizza recipe', 'Python bug fix', 'मौसम की जानकारी'."},
                    {"role": "user", "content": text},
                ],
                "max_tokens": 30,
                "temperature": 0.3,
            },
            timeout=30,
        )
        if r.status_code != 200:
            t = text.strip().replace("\n", " ")
            return t[:40] + ("…" if len(t) > 40 else "")
        data = r.json()
        t = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        t = t.replace("\n", " ").replace('"', '').replace("'", "").strip()
        return t[:50] if t else text.strip()[:40]
    except Exception:
        t = text.strip().replace("\n", " ")
        return t[:40] + ("…" if len(t) > 40 else "")


def _title_from_image(image_data_url: str) -> str:
    if not image_data_url or not image_data_url.startswith("data:image"):
        return "Photo message"
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return "Photo message"
    try:
        r = _req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
            json={
                "model": "qwen/qwen3.8-27b",
                "messages": [
                    {"role": "user", "content": [
                        {"type": "text", "text": "Is photo ka 3-5 shabd ka chat title banao. Sirf title likho, koi quote nahi. Jo bhasha user ne likha ho usme, warna Hindi/Hinglish. Example: 'Gold price chart', 'Smartphone photo', 'Restaurant menu'."},
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                    ]},
                ],
                "max_tokens": 30,
                "temperature": 0.3,
            },
            timeout=40,
        )
        if r.status_code != 200:
            return "Photo message"
        data = r.json()
        t = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        t = t.replace("\n", " ").replace('"', '').replace("'", "").strip()
        return t[:50] if t else "Photo message"
    except Exception:
        return "Photo message"


@app.post("/v1/title")
def make_title(body: TitleRequest, key=Depends(require_api_key)):
    record_usage(key, "title")
    text = (body.message or "").strip()
    if text:
        title = _title_from_text(text)
    elif body.image:
        title = _title_from_image(body.image)
    else:
        title = "New chat"
    return {"title": title}

class DesignRequest(BaseModel):
    prompt: str
    photo: Optional[str] = None  # data URL
    model: Optional[str] = "Default"


def _clean_html(h: str) -> str:
    h = (h or "").strip()
    if "```" in h:
        h = h.replace("```html", "").replace("```", "").strip()
    return h


@app.post("/v1/design")
def make_design(body: DesignRequest, key=Depends(require_api_key)):
    """HTML/CSS se design banao — card, poster, banner, invitation, kuch bhi."""
    record_usage(key, "design")

    system = (
        "Tum ek expert graphic designer aur frontend developer ho. "
        "User jo bhi design mange — wedding card, greeting card, poster, banner, "
        "visiting card, invitation, certificate, menu, flyer, kuch bhi — "
        "uska COMPLETE HTML+CSS design banao.\n\n"
        "RULES:\n"
        "1. Sirf pure HTML return karo — <!DOCTYPE html> se shuru, </html> par khatam.\n"
        "2. Sab CSS inline <style> tag mein ho — alag file nahi.\n"
        "3. Design mobile aur desktop dono par sahi dikhe — responsive.\n"
        "4. Text saaf aur bada ho — print karne layak.\n"
        "5. Sundar fonts use karo — Google Fonts ke through (link tag se).\n"
        "6. Colors, shadows, borders, gradients — sab professional ho.\n"
        "7. Agar user photo bheje to usko <img> se design mein lagao.\n"
        "8. Text user ki bhasha mein — Hindi likhe to Hindi, English likhe to English.\n"
        "9. Har cheez jo user ne kahi — naam, tareekh, jagah, rang, sab daalo.\n"
        "10. Koi markdown nahi, koi explanation nahi, sirf HTML.\n\n"
        "DIMENSION: Agar card hai to A4 ya 800x600 jaisa. Agar social post hai to square (1080x1080). "
        "Agar banner hai to wide (1200x400). User ne jo kaha uske hisab se."
    )

    prompt_text = body.prompt or ""
    if body.photo and body.photo.startswith("data:image"):
        prompt_text += "\n\n[User ki photo neeche di hai — ise design mein shamil karo: " + body.photo[:100] + "... ]"

    try:
        html = _call_groq(prompt_text, system=system)
        html = _clean_html(html)
        if not html or "<html" not in html.lower():
            raise HTTPException(500, "Design generate nahi hua")
        return {
            "service": "design",
            "reply": "Yeh raha aapka design.",
            "html": html,
            "filename": "design.html",
            "kind": "design",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, "Design banane mein problem: " + str(e))
