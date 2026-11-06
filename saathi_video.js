/* Saathi: video se 6 frame nikaal kar photo ki tarah jodta hai, taaki vision unhe padh sake */
(function () {
  var done = new WeakSet();
  var FRAMES = 6, MAXW = 900;

  function grab(att) {
    return new Promise(function (resolve) {
      var v = document.createElement('video');
      v.muted = true; v.playsInline = true; v.preload = 'auto'; v.src = att.dataUrl;
      var out = [], to = setTimeout(function () { resolve(out); }, 30000);
      v.addEventListener('error', function () { clearTimeout(to); resolve(out); });
      v.addEventListener('loadedmetadata', function () {
        var d = v.duration;
        if (!isFinite(d) || d <= 0) { clearTimeout(to); resolve(out); return; }
        var times = [];
        for (var i = 0; i < FRAMES; i++) times.push(Math.min(d - 0.05, Math.max(0, d * (i + 0.5) / FRAMES)));
        var idx = 0;
        function next() {
          if (idx >= times.length) { clearTimeout(to); resolve(out); return; }
          v.currentTime = times[idx];
        }
        v.addEventListener('seeked', function () {
          try {
            var w = v.videoWidth, h = v.videoHeight;
            if (w && h) {
              var s = Math.min(1, MAXW / w);
              var c = document.createElement('canvas');
              c.width = Math.round(w * s); c.height = Math.round(h * s);
              c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
              out.push(c.toDataURL('image/jpeg', 0.72));
            }
          } catch (e) {}
          idx++; next();
        });
        next();
      });
    });
  }

  function scan() {
    try {
      if (typeof pendingAttachments === 'undefined' || !Array.isArray(pendingAttachments)) return;
      pendingAttachments.slice().forEach(function (a) {
        if (!a || a.kind !== 'video' || a.origin !== 'user' || !a.dataUrl || done.has(a)) return;
        done.add(a);
        grab(a).then(function (frames) {
          if (!frames.length) return;
          if (pendingAttachments.indexOf(a) === -1) return;
          frames.forEach(function (f, i) {
            pendingAttachments.push({ kind: 'photo', name: 'video-frame-' + (i + 1) + '.jpg', size: f.length, dataUrl: f, origin: 'user' });
          });
          try { renderPendingAttachments(); updateActionButton(); } catch (e) {}
        }).catch(function () {});
      });
    } catch (e) {}
  }
  setInterval(scan, 400);
})();
