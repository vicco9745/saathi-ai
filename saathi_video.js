window.__vidPA=function(){try{if(window.__vidApi)return window.__vidApi.get();if(typeof pendingAttachments!=='undefined')return pendingAttachments;}catch(e){}return undefined;};
window.__vidRender=function(){try{if(window.__vidApi)window.__vidApi.render();}catch(e){}};
window.__vidFlush=function(){try{if(window.__vidApi)window.__vidApi.flush();}catch(e){}};
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
        
        // Fallback: अगर एक भी फ्रेम नहीं निकला, तो 1 सेकंड पर एक फ्रेम निकालने की कोशिश करें
        if (out.length === 0) {
          try {
            var w = v.videoWidth, h = v.videoHeight;
            if (w && h) {
              var s = Math.min(1, MAXW / w);
              var c = document.createElement('canvas');
              c.width = Math.round(w * s); c.height = Math.round(h * s);
              c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
              out.push(c.toDataURL('image/jpeg', 0.72));
            }
          } catch(e) {}
        }

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
          var dataUrl = c.toDataURL('image/jpeg', 0.72);
          
          // पहले फ्रेम को वीडियो का थंबनेल (प्रीव्यू) बना दें
          if (out.length === 0) {
            att.dataUrl = dataUrl;
            if (true) {
              window.__vidRender(); // UI को तुरंत अपडेट करें
            }
          }
          out.push(dataUrl);
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
          var timer = null;

          function after() {
            if (fired) return; 
            fired = true;
            if (timer) clearTimeout(timer);
            v.removeEventListener('seeked', after);
            // फ्रेम निकालने में थोड़ा समय दें ताकि ड्रॉइंग पूरी हो जाए
            setTimeout(function () { snap(); next(); }, 300);
          }

          v.addEventListener('seeked', after);
          
          // अगर 4 सेकंड में seek न हो, तो अगले फ्रेम पर जाएँ
          timer = setTimeout(after, 4000);
          
          try { 
            v.currentTime = t; 
            // कुछ फ़ोन में seeked इवेंट नहीं आता, इसलिए थोड़ी देर बाद खुद चेक करें
            setTimeout(function() {
               if (Math.abs(v.currentTime - t) < 0.5) after();
            }, 1000);
          } catch (e) { after(); }
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
      try {
        // Base64 को Blob में बदलकर सुरक्षित तरीके से लोड करें
        var parts = att.dataUrl.split(",");
        var byteString = atob(parts[1]);
        var mimeString = parts[0].split(":")[1].split(";")[0];
        var ab = new ArrayBuffer(byteString.length);
        var ia = new Uint8Array(ab);
        for (var i = 0; i < byteString.length; i++) { ia[i] = byteString.charCodeAt(i); }
        var blob = new Blob([ab], { type: mimeString });
        v.src = URL.createObjectURL(blob);
      } catch(e) { v.src = att.dataUrl; }
    });
  }

  function scan() {
    try {
      if (typeof window.__vidPA() === 'undefined' || !Array.isArray(window.__vidPA())) {
        if (!warned) { warned = true; say('Video helper: attachments list nahi mili'); }
        return;
      }
      window.__vidPA().slice().forEach(function (a) {
        if (!a || a.kind !== 'video' || a.origin !== 'user' || !a.dataUrl || done.has(a)) return;
        done.add(a); a.__vidBusy = true;
        say('Video padh raha hoon, 10-20 second ruko...');
        grab(a).then(function (frames) {
          if (window.__vidPA().indexOf(a) === -1) return;
          if (!frames.length) { say('Video se frame nahi nikle'); return; }
          frames.forEach(function (f, i) {
            window.__vidPA().push({ kind: 'photo', name: 'video-frame-' + (i + 1) + '.jpg', size: f.length, dataUrl: f, origin: 'user' });
          });
          try { window.__vidRender(); updateActionButton(); } catch (e) {}
          say(frames.length + ' frame taiyaar, ab bhej sakte ho');
        }).catch(function () { say('Video padhne me gadbad hui'); }).then(function () { a.__vidBusy = false; try { if (true) window.__vidFlush(); } catch (e) {} });
      });
    } catch (e) {}
  }
  setInterval(scan, 400);
})();

/* __vidBadge: status chip */
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
      if (typeof window.__vidPA() === 'undefined' || !Array.isArray(window.__vidPA())) { set('❌ Video helper: attachments list nahi mili', '#dc2626'); return; }
      var vids = window.__vidPA().filter(function (a) { return a && a.kind === 'video' && a.origin === 'user'; });
      var frames = window.__vidPA().filter(function (a) { return a && a.name && String(a.name).indexOf('video-frame-') === 0; });
      var busy = vids.some(function (a) { return a.__vidBusy; });
      if (busy) { if (!busyStart) busyStart = Date.now(); set('⏳ Video padh raha hoon... ' + Math.round((Date.now() - busyStart) / 1000) + ' sec', '#d97706'); seenNoFrames = 0; return; }
      busyStart = 0;
      if (frames.length) { set('✅ ' + frames.length + ' frame taiyaar, ab bhej sakte ho', '#16a34a'); seenNoFrames = 0; return; }
      if (vids.length) { seenNoFrames++; if (seenNoFrames > 8) set('❌ 0 frame nikle', '#dc2626'); else set('⏳ Video check ho raha hai...', '#d97706'); return; }
      seenNoFrames = 0; set('Video helper ON · koi video nahi', '#6b7280');
    } catch (e) {}
  }, 500);
})();

/* frames chhupao: sirf video ki ek tile dikhe */
(function () {
  var st = document.createElement('style');
  st.textContent = '.attachment-tile:has(img[alt^="video-frame-"]),.pending-attachment[title^="video-frame-"]{display:none !important}';
  (document.head || document.documentElement).appendChild(st);
})();
