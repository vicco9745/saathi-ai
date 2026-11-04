p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __imgDims(t){t=String(t||'').toLowerCase();var w=1024,h=1024,m;
function fit(a,b){if(a>=b){w=1280;h=1280*b/a;}else{h=1280;w=1280*a/b;}}
if((m=/(\d+(?:\.\d+)?)\s*(?:x|×|\*|by)\s*(\d+(?:\.\d+)?)/.exec(t))&&Math.max(m[1]/m[2],m[2]/m[1])<=4){fit(+m[1],+m[2]);}
else if((m=/\b(16:9|9:16|4:3|3:4|3:2|2:3|4:5|5:4|21:9|1:1)\b/.exec(t))){var q=m[1].split(':');fit(+q[0],+q[1]);}
else if(/\bbanner\b|बैनर|\bcover\b|\bheader\b/.test(t)){w=1536;h=512;}
else if(/\b(?:tall|portrait|vertical|lamba|lambi|lambe|poster|reel)\b|(?:mobile|phone)\s+wallpaper|लंबा|लंबी|पोस्टर/.test(t)){w=720;h=1280;}
else if(/\b(?:wide|landscape|horizontal|chauda|chaudi|chaude|youtube|thumbnail|desktop|laptop|presentation)\b|चौड़ा|चौड़ी/.test(t)){w=1280;h=720;}
var s=1;if(/\b(?:chhota|chhoti|chhote|chota|choti|small|tiny|mini|icon)\b|छोटा|छोटी/.test(t))s=0.5;else if(/\b(?:bada|badi|bade|large|big|huge|hd|4k)\b|बड़ा|बड़ी/.test(t))s=1.4;
var L=Math.max(w,h)*s;if(L>1536)s=s*1536/L;
function r(v){return Math.max(256,Math.min(1536,Math.round(v*s/16)*16));}
return [r(w),r(h)];}
"""
a1 = 'function linkifyText(text){'
oldB = "body:JSON.stringify({prompt:imgPrompt,model:currentModel,learning:smartCtx})"
newB = "body:JSON.stringify({prompt:imgPrompt,width:__imgDims(imgPrompt)[0],height:__imgDims(imgPrompt)[1],model:currentModel,learning:smartCtx})"
oldC = "pendingReply.text=buildGenReply('image',{caption:data.caption,prompt:imgPrompt});"
newC = "pendingReply.text='';/*no-cap*/"
oldP = "if(m.role==='ai'&&m.proc&&procShow(m))row.appendChild(buildProcessRow(m));"
newP = "if(m.role==='ai'&&m.proc&&procShow(m)&&!(/*no-proc*/m.mediaType==='photo'&&m.attachments&&m.attachments.length&&!m.generating))row.appendChild(buildProcessRow(m));"
out = []
if '__imgDims' in s:
    out.append('dims: pehle se laga hai')
elif s.count(a1) == 1 and s.count(oldB) == 1:
    s = s.replace(a1, FN + a1, 1).replace(oldB, newB, 1)
    out.append('dims: laga diya')
else:
    out.append('dims: jagah nahi mili %d %d' % (s.count(a1), s.count(oldB)))
if '/*no-cap*/' in s:
    out.append('caption: pehle se hata hai')
elif s.count(oldC) == 1:
    s = s.replace(oldC, newC, 1)
    out.append('caption: hata diya')
else:
    out.append('caption: jagah nahi mili %d' % s.count(oldC))
if '/*no-proc*/' in s:
    out.append('proc: pehle se laga hai')
elif s.count(oldP) == 1:
    s = s.replace(oldP, newP, 1)
    out.append('proc: laga diya')
else:
    out.append('proc: jagah nahi mili %d' % s.count(oldP))
open(p, 'w', encoding='utf-8').write(s)
print('\n'.join(out))
