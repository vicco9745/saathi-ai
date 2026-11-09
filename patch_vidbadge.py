BADGE = """/* __vidBadge: status chip */
(function () {
  var el = null, seenNoFrames = 0, busyStart = 0;
  function mk() {
    if (el || !document.body) return;
    el = document.createElement('div');
    el.id = 'vidBadge';
    el.style.cssText = 'position:fixed;bottom:140px;left:50%;transform:translateX(-50%);z-index:99999;padding:6px 12px;border-radius:14px;font:600 12px/1.2 sans-serif;color:#fff;background:#6b7280;pointer-events:none;box-shadow:0 2px 8px rgba(0,0,0,.2);max-width:90%;text-align:center;';
    document.body.appendChild(el);
  }
  function set(t, c) { mk(); if (!el) return; el.textContent = t; el.style.background = c; }
  setInterval(function () {
    try {
      if (typeof pendingAttachments === 'undefined' || !Array.isArray(pendingAttachments)) { set('\u274c Video helper: attachments list nahi mili', '#dc2626'); return; }
      var vids = pendingAttachments.filter(function (a) { return a && a.kind === 'video' && a.origin === 'user'; });
      var frames = pendingAttachments.filter(function (a) { return a && a.name && String(a.name).indexOf('video-frame-') === 0; });
      var busy = vids.some(function (a) { return a.__vidBusy; });
      if (busy) { if (!busyStart) busyStart = Date.now(); set('\u23f3 Video padh raha hoon... ' + Math.round((Date.now() - busyStart) / 1000) + ' sec', '#d97706'); seenNoFrames = 0; return; }
      busyStart = 0;
      if (frames.length) { set('\u2705 ' + frames.length + ' frame taiyaar, ab bhej sakte ho', '#16a34a'); seenNoFrames = 0; return; }
      if (vids.length) { seenNoFrames++; if (seenNoFrames > 8) set('\u274c 0 frame nikle', '#dc2626'); else set('\u23f3 Video check ho raha hai...', '#d97706'); return; }
      seenNoFrames = 0; set('Video helper ON \u00b7 koi video nahi', '#6b7280');
    } catch (e) {}
  }, 500);
})();
"""
j = "saathi_video.js"
t = open(j, encoding="utf-8").read()
if "__vidBadge" in t:
    print("badge: pehle se laga hai")
else:
    open(j, "w", encoding="utf-8").write(t.rstrip() + "\n\n" + BADGE)
    print("badge: saathi_video.js mein jod diya")
# cache todne ke liye v=2 se v=3
for f in ["index.html", "site_patches/98_video.py"]:
    s = open(f, encoding="utf-8").read()
    if "saathi_video.js?v=2" in s:
        open(f, "w", encoding="utf-8").write(s.replace("saathi_video.js?v=2", "saathi_video.js?v=3"))
        print(f + ": v=3 kar diya")
    else:
        print(f + ": v=2 nahi mila, chhoda")
