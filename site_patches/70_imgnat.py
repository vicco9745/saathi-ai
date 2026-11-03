p = 'index.html'
s = open(p, encoding='utf-8').read()
old = r"const imageMatch=/^\/image\s+([\s\S]+)/i.exec(combinedText.trim());"
new = r"""/*img-nat*/const imageMatch=(function(){const t=combinedText.trim();const m0=/^\/image\s+([\s\S]+)/i.exec(t);if(m0)return m0;if(t.length>1500||t.indexOf('```')>-1||t.charAt(0)==='/')return null;if(/\bpdf\b|पीडीएफ|\bwebsite\b|\bsite\b|वेबसाइट|html|=== file:|file ka naam:/i.test(t))return null;const A=/\b(?:images?|photos?|pictures?|pics?)\b|तस्वीर|फोटो|चित्र/i;const B=/\b(?:banao|banaao|bana\s+do|bana\s+de|banade|bana\s+dijiye|bana\s+dena|banakar|bana\s+kar|generate|create|draw)\b|बनाओ|बना\s*दो|बना\s*दे|बनाएं|बनायें|बनाइए|बनाकर|बना\s*कर/i;return(A.test(t)&&B.test(t))?[t,t]:null;})();"""
if 'img-nat' in s:
    print('imgnat: pehle se laga hai')
elif s.count(old) == 1:
    open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('imgnat: laga diya')
else:
    print('imgnat: jagah nahi mili', s.count(old))
