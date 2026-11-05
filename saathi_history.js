/* Saathi: har /v1/chat call me chat ke pichhle 6 sandesh 'history' ke roop me bhejta hai */
(function () {
  var _f = window.fetch;
  window.fetch = function (u, o) {
    try {
      if (typeof u === 'string' && u.indexOf('/v1/chat') > -1 && o && typeof o.body === 'string') {
        var b = JSON.parse(o.body);
        if (b && !b.history && typeof getCurrentChat === 'function') {
          var c = getCurrentChat();
          if (c && Array.isArray(c.messages)) {
            var h = [];
            c.messages.forEach(function (m) {
              var t = String((m && m.text) || '').trim();
              if (!t) return;
              h.push({ role: m.role === 'ai' ? 'assistant' : 'user', text: t.slice(0, 800) });
            });
            if (h.length && h[h.length - 1].role === 'user') h.pop();
            b.history = h.slice(-6);
            o = Object.assign({}, o, { body: JSON.stringify(b) });
          }
        }
      }
    } catch (e) {}
    return _f.call(this, u, o);
  };
})();
