p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function renderUserText(text){text=String(text==null?'':text);if(text.indexOf('```')<0)return linkifyText(text);const re=/```([^\n`]*)\n?([\s\S]*?)(?:```|$)/g;let out='',last=0,m;
while((m=re.exec(text))!==null){if(m.index===re.lastIndex){re.lastIndex++;continue;}
const before=text.slice(last,m.index);if(before)out+=linkifyText(before.replace(/\n$/,''));
out+=renderRichText(text.slice(m.index,m.index+m[0].length));
last=m.index+m[0].length;if(text.charAt(last)==='\n')last++;}
const rest=text.slice(last);if(rest)out+=linkifyText(rest);return out;}
"""
if 'function renderUserText(' in s:
    print('usercode: pehle se laga hai')
else:
    a = 'function renderRichText(text){'
    b = "}else{bubble.innerHTML=linkifyText(m.text);}"
    if s.count(a) == 1 and s.count(b) == 1:
        s = s.replace(a, FN + a, 1)
        s = s.replace(b, "}else{bubble.innerHTML=renderUserText(m.text);wireCodeBlocks(bubble);}", 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('usercode: laga diya')
    else:
        print('usercode: jagah nahi mili', s.count(a), s.count(b))
