path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

import re
pattern = re.compile(r'function typeAIMessage\(element,text,message\)\{.*?typeNext\(\);\}', re.DOTALL)

new_fn = '''function typeAIMessage(element,text,message){
element.textContent='';
const totalLen=text.length;
const TARGET_MS=20000;
const steps=100;
const interval=TARGET_MS/steps;
const chunk=Math.max(1,Math.ceil(totalLen/steps));
let i=0;let lastRender=0;
aiIsTyping=true;activeTypingMessage=message;message.fullText=text;updateActionButton();
function typeNext(){
if(i<text.length){
i=Math.min(i+chunk,text.length);
const now=Date.now();
if(now-lastRender>100){
const partial=text.slice(0,i);
try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(partial);else element.textContent=partial;}catch(_){element.textContent=partial;}
lastRender=now;
}
messagesEl.scrollTop=messagesEl.scrollHeight;
activeTypingTimeout=setTimeout(typeNext,interval);
}else{
message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;
try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(text);else element.textContent=text;}catch(_){element.textContent=text;}
saveChats();updateActionButton();
}}
typeNext();}'''

match = pattern.search(c)
if match:
    c = c[:match.start()] + new_fn + c[match.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("OK - 20 second typing fix ho gaya")
else:
    print("FAIL - function nahi mila")
