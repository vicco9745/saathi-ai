p = "app/main.py"
s = open(p, encoding="utf-8").read()
a = "        audio = await _tts_provider(t, body.lang)"
assert s.count(a) == 1, "main.py match nahi mila"
b = ("        import time as _tm\n"
     "        _t0 = _tm.time()\n"
     "        audio = await _tts_provider(t, body.lang)\n"
     "        print(f\"[tts-time] {len(t)} chars -> {_tm.time()-_t0:.2f}s\")")
open(p, "w", encoding="utf-8").write(s.replace(a, b, 1))

q = "index.html"
h = open(q, encoding="utf-8").read()
c = "  play(0);\n}\nfunction __cvAsk"
assert h.count(c) == 1, "index.html match nahi mila"
d = "  play(0);\n  for(var __k=1;__k<Math.min(parts.length,3);__k++)load(__k);\n}\nfunction __cvAsk"
open(q, "w", encoding="utf-8").write(h.replace(c, d, 1))
print("patched")
