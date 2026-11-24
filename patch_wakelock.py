p = "index.html"
s = open(p, encoding="utf-8").read()
assert "__saathiWakeLock" not in s, "already patched"
assert s.count("</body>") == 1, "body tag match nahi mila"
js = r'''<script>/*__saathiWakeLock*/
(function(){var wl=null;
async function acq(){try{if(!('wakeLock' in navigator)||wl)return;wl=await navigator.wakeLock.request('screen');wl.addEventListener('release',function(){wl=null;});}catch(_){wl=null;}}
function rel(){try{if(wl)wl.release();}catch(_){}wl=null;}
setInterval(function(){try{if(typeof callActive==='undefined')return;if(callActive){if(document.visibilityState==='visible')acq();}else rel();}catch(_){}},1500);
document.addEventListener('visibilitychange',function(){try{if(document.visibilityState==='visible'&&typeof callActive!=='undefined'&&callActive)acq();}catch(_){}});
})();
</script>
'''
open(p, "w", encoding="utf-8").write(s.replace("</body>", js + "</body>", 1))
print("patched")
