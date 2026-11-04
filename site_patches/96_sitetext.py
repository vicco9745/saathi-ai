p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __buildGenReplyNew(kind,o){
if(kind!=='website')return __buildGenReplyOld(kind,o);
o=o||{};const cap=(o.caption||'').trim();if(cap.length>=140)return cap;
const html=String(o.html||'');const i=describeWebsiteHtml(html)||{};
let um='';try{const ch=getCurrentChat();const ms=(ch&&ch.messages)||[];for(let k=ms.length-1;k>=0;k--){if(ms[k].role==='user'){um=String(ms[k].text||'');break;}}}catch(_){}
const hi=/[\u0900-\u097F]/.test(um)||(!/[^\x00-\x7F]/.test(um)&&/\b(?:bana|banao|banaao|ki|ka|ke|mein|hai|hain|karo|kar|ek|mujhe|mere|meri|aap|jisme|wali|wala|wale|nahi|aur|chahiye|liye)\b/i.test(um));
const sx=function(x){return String(x).replace(/[*`|#]/g,'').trim();};
const heads=(Array.isArray(i.heads)?i.heads:[]).slice(0,6).map(sx).filter(Boolean);
const title=i.title?sx(i.title):'';
const lines=html?html.split('\n').length:0;
const resp=/@media|name=["']viewport/i.test(html);
const T=hi?{ready:'आपकी वेबसाइट तैयार है',head:'इसमें क्या-क्या है',sec:'सेक्शन',nav:function(n){return '**नेविगेशन मेनू** — ऊपर '+n+' लिंक';},img:function(n){return '**इमेज / गैलरी** — '+n+' इमेज';},btn:'**बटन और कॉल-टू-एक्शन**',form:'**फ़ॉर्म** — संपर्क के लिए इनपुट फ़ील्ड',js:'**इंटरैक्टिव फ़ीचर** — JavaScript से चलने वाले हिस्से',anim:'**एनिमेशन** — हल्के और स्मूद',resp:function(n){return '**रेस्पॉन्सिव डिज़ाइन** — मोबाइल और डेस्कटॉप दोनों पर, '+n+' लाइन का कोड';},code:function(n){return '**कोड** — '+n+' लाइन';},foot:'कार्ड पर टैप करके वेबसाइट लाइव देखें, या कोड कॉपी/डाउनलोड करें। कुछ बदलवाना हो तो बस बताइए।'}:{ready:'Your website is ready',head:'What is included',sec:'Sections',nav:function(n){return '**Navigation menu** — '+n+' links at the top';},img:function(n){return '**Images / gallery** — '+n+(n>1?' images':' image');},btn:'**Buttons and calls to action**',form:'**Form** — input fields for contact',js:'**Interactive features** — powered by JavaScript',anim:'**Animations** — subtle and smooth',resp:function(n){return '**Responsive design** — works on mobile and desktop, '+n+' lines of code';},code:function(n){return '**Code** — '+n+' lines';},foot:'Tap the card to preview the live site, or copy or download the code. Tell me what you would like changed.'};
let t='**'+T.ready+'**'+(title?(' — *'+title+'*'):'')+'\n\n**'+T.head+'**';
if(heads.length)t+='\n- **'+T.sec+':** '+heads.join(', ');
if(i.nav>0)t+='\n- '+T.nav(i.nav);
if(i.imgs>0)t+='\n- '+T.img(i.imgs);
if(i.btns>0)t+='\n- '+T.btn;
if(i.form)t+='\n- '+T.form;
if(i.js)t+='\n- '+T.js;
if(i.anim)t+='\n- '+T.anim;
if(lines)t+='\n- '+(resp?T.resp(lines):T.code(lines));
return t+'\n\n'+T.foot;}
function buildGenReply(kind,o){try{return __buildGenReplyNew(kind,o);}catch(e){return __buildGenReplyOld(kind,o);}}
"""
a = 'function buildGenReply(kind,o){'
oldL = r"const clean=String(m.text||'').replace(/```[^\n`]*\n?/g,'').replace(/\s+/g,' ').trim();"
newL = r"const clean=String(m.text||'').replace(/```[^\n`]*\n?/g,'').replace(/(^|\n)\s*[-•]\s+/g,'$1').replace(/[*#]/g,'')/*lbl*/.replace(/\s+/g,' ').trim();"
out = []
if '__buildGenReplyNew' in s:
    out.append('sitetext: pehle se laga hai')
elif s.count(a) == 1:
    s = s.replace(a, FN + 'function __buildGenReplyOld(kind,o){', 1)
    out.append('sitetext: laga diya')
else:
    out.append('sitetext: jagah nahi mili %d' % s.count(a))
if '/*lbl*/' in s:
    out.append('label: pehle se saaf hai')
elif s.count(oldL) == 1:
    s = s.replace(oldL, newL, 1)
    out.append('label: saaf kar diya')
else:
    out.append('label: jagah nahi mili %d' % s.count(oldL))
open(p, 'w', encoding='utf-8').write(s)
print('\n'.join(out))
