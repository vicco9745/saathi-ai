p = "index.html"
s = open(p, encoding="utf-8").read()
assert "__saathiNative" not in s, "already patched"
assert s.count("</body>") == 1, "body tag match nahi mila"
js = r'''<script>/*__saathiNative*/
(function(){var on=false;setInterval(function(){try{if(!window.SaathiNative||typeof callActive==='undefined')return;if(callActive&&!on){on=true;window.SaathiNative.start();}else if(!callActive&&on){on=false;window.SaathiNative.stop();}}catch(_){}},1000);})();
</script>
'''
open(p, "w", encoding="utf-8").write(s.replace("</body>", js + "</body>", 1))
print("patched")
