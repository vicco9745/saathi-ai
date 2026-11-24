p = "index.html"
s = open(p, encoding="utf-8").read()
assert "__saathiKeepAlive" not in s, "already patched"
assert s.count("</body>") == 1, "body tag match nahi mila"
js = r'''<script>/*__saathiKeepAlive*/
(function(){var el=null;
function wav(){var n=8000,b=new ArrayBuffer(44+n*2),v=new DataView(b);function w(o,t){for(var i=0;i<t.length;i++)v.setUint8(o+i,t.charCodeAt(i));}w(0,'RIFF');v.setUint32(4,36+n*2,true);w(8,'WAVE');w(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,8000,true);v.setUint32(28,16000,true);v.setUint16(32,2,true);v.setUint16(34,16,true);w(36,'data');v.setUint32(40,n*2,true);return new Blob([b],{type:'audio/wav'});}
function start(){try{if(el)return;el=new Audio(URL.createObjectURL(wav()));el.loop=true;var pr=el.play();if(pr&&pr.catch)pr.catch(function(){el=null;});
if('mediaSession' in navigator){navigator.mediaSession.metadata=new MediaMetadata({title:'Saathi call',artist:'Saathi'});}}catch(_){el=null;}}
function stop(){try{if(el){el.pause();el.src='';}}catch(_){}el=null;try{if('mediaSession' in navigator)navigator.mediaSession.metadata=null;}catch(_){}}
setInterval(function(){try{if(typeof callActive==='undefined')return;if(callActive)start();else stop();}catch(_){}},1500);
})();
</script>
'''
open(p, "w", encoding="utf-8").write(s.replace("</body>", js + "</body>", 1))
print("patched")
