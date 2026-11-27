def _f(v):
    try:
        if v is None or str(v).strip() == '':
            return None
        return float(v)
    except Exception:
        return None


def mt5_chart_png(a):
    try:
        import io, json
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
        data = a.get('data', '[]')
        if isinstance(data, str):
            data = json.loads(data)
        rows = []
        for c in data:
            try:
                rows.append((str(c.get('time', '')), float(c['open']), float(c['high']), float(c['low']), float(c['close'])))
            except Exception:
                continue
        if len(rows) < 2:
            return None
        rows = rows[-120:]
        n = len(rows)
        entry, stop, target = _f(a.get('entry')), _f(a.get('stop')), _f(a.get('target'))
        side = str(a.get('side', '')).strip().upper()
        if side not in ('BUY', 'SELL'):
            side = ''
            if entry is not None and stop is not None:
                side = 'SELL' if stop > entry else 'BUY'
        sym = str(a.get('symbol', '')).strip()[:12]
        tf = str(a.get('tf', '')).strip()[:6]
        title = str(a.get('title', '')).strip()
        lows = [r[3] for r in rows]
        highs = [r[2] for r in rows]
        extra = [v for v in (entry, stop, target) if v is not None]
        lo = min(lows + extra)
        hi = max(highs + extra)
        pad = (hi - lo) * 0.08 or 1.0
        mid = (lo + hi) / 2
        fmt = '{:.2f}' if mid >= 100 else ('{:.3f}' if mid >= 10 else '{:.5f}')
        last = rows[-1][4]
        fig, ax = plt.subplots(figsize=(7, 4.6), dpi=150)
        fig.subplots_adjust(left=0.03, right=0.86, top=0.85, bottom=0.12)
        tiny = (hi - lo) * 0.002
        for i, (t, o, h, l, c) in enumerate(rows):
            col = '#26a69a' if c >= o else '#ef5350'
            ax.plot([i, i], [l, h], color='#444444', linewidth=0.8, zorder=1)
            ax.add_patch(Rectangle((i - 0.32, min(o, c)), 0.64, max(abs(c - o), tiny), facecolor=col, edgecolor=col, zorder=2))
        ax.set_xlim(-1, n + 3)
        ax.set_ylim(lo - pad, hi + pad)
        tr = ax.get_yaxis_transform()

        def hl(y, color, ls, left, tagbg, tagfg, tagec):
            ax.axhline(y, color=color, linestyle=ls, linewidth=1.1, zorder=3)
            if left:
                ax.text(0.01, y, left, transform=tr, color=color, fontsize=8, va='bottom', ha='left', zorder=5)
            ax.text(1.01, y, fmt.format(y), transform=tr, color=tagfg, fontsize=7.5, va='center', ha='left', zorder=6, clip_on=False,
                    bbox=dict(boxstyle='square,pad=0.25', facecolor=tagbg, edgecolor=tagec, linewidth=1))

        if entry is not None:
            hl(entry, '#e53935', '--', side or 'ENTRY', 'white', '#e53935', '#e53935')
        if stop is not None:
            hl(stop, '#888888', '--', 'SL', 'white', '#666666', '#888888')
        if target is not None:
            hl(target, '#888888', '--', 'TP', 'white', '#666666', '#888888')
        lc = '#26a69a' if rows[-1][4] >= rows[-1][1] else '#ef5350'
        hl(last, lc, '-', '', lc, 'white', lc)
        ax.yaxis.tick_right()
        ax.tick_params(axis='y', labelsize=7.5, length=0, pad=4)
        for sp in ('top', 'left'):
            ax.spines[sp].set_visible(False)
        ax.spines['right'].set_color('#cccccc')
        ax.spines['bottom'].set_color('#cccccc')
        k = min(4, n)
        idx = sorted(set(int(round(j * (n - 1) / max(k - 1, 1))) for j in range(k)))
        ax.set_xticks(idx)
        ax.set_xticklabels([rows[j][0] for j in idx], fontsize=7.5)
        ax.tick_params(axis='x', length=0)
        head = (sym + '  ' + tf).strip()
        if head:
            fig.text(0.03, 0.945, head, color='#1a73e8', fontsize=11, fontweight='bold', va='center')
        if title and title.isascii():
            fig.text(0.03, 0.905, title, color='#222222', fontsize=8.5, va='center')
        o, h, l, c = rows[-1][1:]
        fig.text(0.03, 0.87, fmt.format(o) + '  ' + fmt.format(h) + '  ' + fmt.format(l) + '  ' + fmt.format(c), color='#222222', fontsize=8, va='center')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor='white')
        plt.close(fig)
        return buf.getvalue()
    except Exception as e:
        print('[mt5 chart] ' + str(e))
        return None
