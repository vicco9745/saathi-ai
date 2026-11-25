p = 'index.html'
s = open(p, encoding='utf-8').read()
R = [
(r"""SAATHI_API_BASE+'/v1/budget-ui',{method:'POST',headers""", r"""SAATHI_API_BASE+'/v1/budget-ui2',{method:'POST',headers"""),
(r"""const done=function(d){const ok=d&&d.labels&&typeof d.labels==='object';const ui=ok?{lang:String(d.lang||'en'),cur:String(d.cur||'₹'),labels:d.labels}:{lang:'en',cur:'₹'};__bFinish(m,{mode:(d&&d.intent==='show')?'all':'form',draft:{},ui:ui});};""",
 r"""const done=function(d){const n=(d&&d.labels&&typeof d.labels==='object')?Object.keys(d.labels).length:0;const ui={lang:String((d&&d.lang)||'en'),cur:String((d&&d.cur)||'₹'),labels:(d&&d.labels)||{}};if(n<10)ui.err=(d&&d.err)?String(d.err):('translation incomplete ('+n+'/32)');__bFinish(m,{mode:(d&&d.intent==='show')?'all':'form',draft:{},ui:ui});};"""),
(r""".then(function(r){return r.ok?r.json():null;}).then(done).catch(function(){done(null);});""",
 r""".then(function(r){if(!r.ok){return {err:'server '+r.status};}return r.json();}).then(done).catch(function(e){done({err:'network: '+String(e&&e.message||e).slice(0,60)});});"""),
(r"""'<div class="bd-err" id="be"></div><button class="bd-btn primary" id="bsub">'+__bI.save""",
 r"""(bd.ui&&bd.ui.err?'<div class="bd-err">Translation: '+__bEsc(bd.ui.err)+'</div>':'')+'<div class="bd-err" id="be"></div><button class="bd-btn primary" id="bsub">'+__bI.save"""),
]
if '/v1/budget-ui2' in s:
    print('budget4: pehle se laga hai')
else:
    bad = [i for i, (a, b) in enumerate(R) if s.count(a) != 1]
    if bad:
        print('budget4: jagah nahi mili', bad)
    else:
        for a, b in R:
            s = s.replace(a, b, 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('budget4: laga diya')
