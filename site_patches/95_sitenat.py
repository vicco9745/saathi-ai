p = 'index.html'
s = open(p, encoding='utf-8').read()
old = r"const websiteMatch=/^\/website\s+([\s\S]+)/i.exec(combinedText.trim());"
new = r"""/*site-nat*/const websiteMatch=(function(){const t=combinedText.trim();const m0=/^\/website\s+([\s\S]+)/i.exec(t);if(m0)return m0;if(t.length>1500||t.indexOf('```')>-1||t.charAt(0)==='/')return null;if(/\bpdf\b|पीडीएफ|=== file:|file ka naam:|<(?:!doctype|html|body|div)/i.test(t))return null;const A=/\b(?:websites?|webpages?|web\s+pages?|landing\s+pages?|homepage)\b|वेबसाइट|वेबपेज/i;const B=/\b(?:banao|banaao|bana\s+do|bana\s+de|banade|bana\s+dijiye|bana\s+dena|banakar|bana\s+kar|generate|create|build|make|develop|design)\b|बनाओ|बना\s*दो|बना\s*दे|बनाएं|बनायें|बनाइए|बनाकर|बना\s*कर/i;return(A.test(t)&&B.test(t))?[t,t]:null;})();"""
if 'site-nat' in s:
    print('sitenat: pehle se laga hai')
elif s.count(old) == 1:
    open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('sitenat: laga diya')
else:
    print('sitenat: jagah nahi mili', s.count(old))
