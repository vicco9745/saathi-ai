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
            return '\n\n<<' + name.upper() + '_B_' + str(len(store)-1) + '>>\n\n'
        html = _re.sub(pat, _r, html, flags=_re.I|_re.S)

    _extract('chart', chart_blocks)
    _extract('img', img_blocks)
    _extract('box', box_blocks)

    # Extract pagebreak
    html = _re.sub(r'<pagebreak\s*/?>', '\n\n<<PAGEBREAK_B>>\n\n', html, flags=_re.I)

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
        return '\n\n<<TABLE_B_' + str(len(tables)-1) + '>>\n\n'
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
            png = _generate_chart_png(ctype, ctitle, data_json, entry, stop, target)
            if png:
                import tempfile as _tf
                with _tf.NamedTemporaryFile(suffix='.png', delete=False) as t:
                    t.write(png); tpath = t.name
                try:
                    y = pdf.get_y()
                    pdf.image(tpath, x=18, y=y, w=pdf.w - 36)
                    pdf.ln(4)
                except Exception as e: print('[pdf] chart embed ' + str(e))
                finally:
                    try: _os.unlink(tpath)
                    except Exception: pass
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
