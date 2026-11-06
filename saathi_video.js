/* Saathi: video se 5 frame nikaal kar photo ki tarah jodta hai, taaki vision unhe padh sake */
(function () {
  var done = new WeakSet(), warned = false;
  var FRAMES = 5, MAXW = 900;

  function say(t) { try { if (typeof showToast === 'function') showToast(t); } catch (e) {} }

  function grab(att) {
    return new Promise(function (resolve) {
      var out = [], finished = false, started = false;
      var v = document.createElement('video');
      v.muted = true; v.defaultMuted = true; v.playsInline = true;
      v.setAttribute('playsinline', ''); v.setAttribute('muted', '');
      v.preload = 'auto';
      v.style.cssText = 'position:fixed;left:-9999px;top:0;width:2px;height:2px;opacity:0;pointer-events:none;';
      document.body.appendChild(v);

      var total = setTimeout(finish, 45000);
      function finish() {
        if (finished) return; finished = true;
        clearTimeout(total);
        try { v.pause(); v.removeAttribute('src'); v.load(); v.remove(); } catch (e) {}
        resolve(out);
      }
      v.addEventListener('error', finish);

      function snap() {
        try {
          var w = v.videoWidth, h = v.videoHeight;
          if (!w || !h) return;
          var s = Math.min(1, MAXW / w);
          var c = document.createElement('canvas');
          c.width = Math.round(w * s); c.height = Math.round(h * s);
          c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
          out.push(c.toDataURL('image/jpeg', 0.72));
        } catch (e) {}
      }

      function run() {
        var d = v.duration;
        if (!isFinite(d) || d <= 0) { finish(); return; }
        var times = [], idx = 0;
        for (var i = 0; i < FRAMES; i++) times.push(Math.min(Math.max(d - 0.1, 0), d * (i + 0.5) / FRAMES));
        function next() {
          if (idx >= times.length) { finish(); return; }
          var t = times[idx++], fired = false;
          function after() {
            if (fired) return; fired = true;
            v.removeEventListener('seeked', after);
            setTimeout(function () { snap(); next(); }, 120);
          }
          v.addEventListener('seeked', after);
          setTimeout(after, 4000);
          try { v.currentTime = t; } catch (e) { after(); }
        }
        next();
      }

      function start() {
        if (started) return; started = true;
        var p;
        try { p = v.play(); } catch (e) {}
        if (p && p.then) p.then(function () { v.pause(); run(); }).catch(function () { run(); });
        else run();
      }
      v.addEventListener('loadeddata', start);
      v.addEventListener('loadedmetadata', function () { setTimeout(start, 300); });
      v.src = att.dataUrl;
    });
  }

  function scan() {
    try {
      if (typeof pendingAttachments === 'undefined' || !Array.isArray(pendingAttachments)) {
        if (!warned) { warned = true; say('Video helper: attachments list nahi mili'); }
        return;
      }
      pendingAttachments.slice().forEach(function (a) {
        if (!a || a.kind !== 'video' || a.origin !== 'user' || !a.dataUrl || done.has(a)) return;
        done.add(a);
        say('Video padh raha hoon, 10-20 second ruko...');
        grab(a).then(function (frames) {
          if (pendingAttachments.indexOf(a) === -1) return;
          if (!frames.length) { say('Video se frame nahi nikle'); return; }
          frames.forEach(function (f, i) {
            pendingAttachments.push({ kind: 'photo', name: 'video-frame-' + (i + 1) + '.jpg', size: f.length, dataUrl: f, origin: 'user' });
          });
          try { renderPendingAttachments(); updateActionButton(); } catch (e) {}
          say(frames.length + ' frame taiyaar, ab bhej sakte ho');
        }).catch(function () { say('Video padhne me gadbad hui'); });
      });
    } catch (e) {}
  }
  setInterval(scan, 400);
})();
