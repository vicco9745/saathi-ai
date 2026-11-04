p = 'index.html'
s = open(p, encoding='utf-8').read()
old = r"const pdfMatch=/^\/pdf\s+([\s\S]+)/i.exec(combinedText.trim());"
new = r"""/*pdf-nat*/const pdfMatch=(function(){const t=combinedText.trim();const m0=/^\/pdf\s+([\s\S]+)/i.exec(t);if(m0)return m0;if(t.length>1500||t.indexOf('```')>-1||t.charAt(0)==='/')return null;if(/=== file:|file ka naam:|user ne neeche file/i.test(t))return null;if(/\b(?:is|iss|yeh|ye|this|attached|uploaded|upload)\s+(?:wali\s+|ki\s+)?pdf\b/i.test(t))return null;if(/\b(?:how\s+to|kaise|kya\s+hota|what\s+is|explain)\b/i.test(t))return null;const A=/\bpdfs?\b|पीडीएफ|पी\.डी\.एफ/i;const B=/\b(?:banao|banaao|bana\s+do|bana\s+de|banade|bana\s+dijiye|bana\s+dena|banakar|bana\s+kar|likho|likh\s+do|likh\s+de|generate|create|make|build)\b|बनाओ|बना\s*दो|बना\s*दे|बनाएं|बनायें|बनाइए|बनाकर|बना\s*कर/i;const P=/\b(?:document|report|docx|letter)\s+(?:banao|banaao|bana\s+do|bana\s+de|banade)\b/i;return((A.test(t)&&B.test(t))||P.test(t))?[t,t]:null;})();"""
a2 = "if(d.kind==='image'&&d.image_url){"
PDFB = r"""if(d.kind==='pdf'&&d.pdf_base64){m.processing=null;m.attachments=[{kind:'file',name:d.filename||'generated.pdf',dataUrl:'data:application/pdf;base64,'+d.pdf_base64,origin:'ai'}];m.text=buildGenReply('pdf',{caption:d.caption,prompt:prompt});m.typing=true;try{saveChats();renderMessages();}catch(_){}return true;}
"""
out = []
if 'pdf-nat' in s:
    out.append('pdfnat: pehle se laga hai')
elif s.count(old) == 1:
    s = s.replace(old, new, 1)
    out.append('pdfnat: laga diya')
else:
    out.append('pdfnat: jagah nahi mili %d' % s.count(old))
if "d.kind==='pdf'" in s:
    out.append('pdf-branch: pehle se laga hai')
elif s.count(a2) == 1:
    s = s.replace(a2, PDFB + a2, 1)
    out.append('pdf-branch: laga diya')
else:
    out.append('pdf-branch: jagah nahi mili %d' % s.count(a2))
open(p, 'w', encoding='utf-8').write(s)
print('\n'.join(out))
