window.__vidPA=function(){try{if(window.__vidApi)return window.__vidApi.get();if(typeof pendingAttachments!=='undefined')return pendingAttachments;}catch(e){}return undefined;};
window.__vidRender=function(){try{if(window.__vidApi)window.__vidApi.render();}catch(e){}};
window.__vidFlush=function(){try{if(window.__vidApi)window.__vidApi.flush();}catch(e){}};
/* Saathi: video se frame nikaalta hai, UI mein sirf 1 dikhata hai, baaki AI ko chupke se bhejta hai */
(function () {
  var done = new WeakSet(), warned = false;
  var MAXW = 900;

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

      var total = setTimeout(finish, 60000); // 60 sec tak wait karega
      function finish() {
        if (finished) return; finished = true;
        clearTimeout(total);
        
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

          if (out.length === 0) {
            att.dataUrl = dataUrl; // UI mein pehla frame
            if (true) window.__vidRender();
          }
          out.push(dataUrl);
        } catch (e) {}
      }

      function run() {
        var d = v.duration;
        if (!isFinite(d) || d <= 0) { finish(); return; }
        
        // Video ki lambai ke hisaab se frames nikale (Har 3 second mein 1 frame, max 10)
        var count = Math.max(2, Math.min(10, Math.floor(d / 3)));
        var times = [], idx = 0;
        for (var i = 0; i < count; i++) times.push(Math.min(Math.max(d - 0.1, 0), d * (i + 0.5) / count));
        
        function next() {
          if (idx >= times.length) { finish(); return; }
          var t = times[idx++], fired = false;
          var timer = null;

          function after() {
            if (fired) return; fired = true;
            if (timer) clearTimeout(timer);
            v.removeEventListener('seeked', after);
            setTimeout(function () { snap(); next(); }, 300);
          }

          v.addEventListener('seeked', after);
          timer = setTimeout(after, 4000);
          try { 
            v.currentTime = t; 
            setTimeout(function() { if (Math.abs(v.currentTime - t) < 0.5) after(); }, 1000);
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
        say('Video padh raha hoon, thoda intezaar karein...');
        
        grab(a).then(function (frames) {
          if (window.__vidPA().indexOf(a) === -1) return;
          if (!frames.length) { say('Video se frame nahi nikle'); return; }
          
          // Pehla frame UI mein dikhega
          a.dataUrl = frames[0];
          a.kind = 'photo';
          a.name = 'video-thumbnail.jpg';

          // Baaki frames chhup kar (hidden) AI ke paas jayenge
          for (var i = 1; i < frames.length; i++) {
            var f = frames[i];
            window.__vidPA().push({ 
              kind: 'photo', 
              name: 'video-frame-' + (i + 1) + '.jpg', 
              size: f.length, 
              dataUrl: f, 
              origin: 'user',
              hidden: true // Ye UI mein nahi dikhega
            });
          }

          try { window.__vidRender(); updateActionButton(); } catch (e) {}
          say('Video taiyaar hai, ab sawaal likh kar bhejein');
        }).catch(function () { say('Video padhne me gadbad hui'); }).then(function () { a.__vidBusy = false; try { if (true) window.__vidFlush(); } catch (e) {} });
      });
    } catch (e) {}
  }
  setInterval(scan, 400);
})();
