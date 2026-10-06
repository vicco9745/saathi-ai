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
const interval=Math.max(50,TARGET_MS/steps);
const chunk=Math.max(1,Math.ceil(totalLen/steps));
let i=0;let lastRender=0;
aiIsTyping=true;activeTypingMessage=message;message.fullText=text;updateActionButton();
function finish(){
message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;
try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(text);else element.textContent=text;}catch(_){element.textContent=text;}
saveChats();updateActionButton();
setTimeout(function(){try{renderMessages();}catch(_){}},50);
}
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
}else{finish();}
}
typeNext();}'''

match = pattern.search(c)
if match:
    c = c[:match.start()] + new_fn + c[match.end():]
    print("OK - Spinner fix")
else:
    print("FAIL")

# Also cleanup stuck typing on app load
cleanup = '''
(function(){
try{
  const raw = localStorage.getItem('ai_chat_history_v1');
  if(raw){
    const chats = JSON.parse(raw);
    let changed = false;
    chats.forEach(function(ch){
      (ch.messages||[]).forEach(function(m){
        if(m.role==='ai' && m.typing===true && (!m.text || !m.text.trim())){
          m.typing = false;
          changed = true;
        }
      });
    });
    if(changed){
      localStorage.setItem('ai_chat_history_v1', JSON.stringify(chats));
      console.log('Fixed stuck typing messages');
    }
  }
}catch(_){}
})();
'''

# Insert cleanup at the very end before </script>
if 'Fixed stuck typing messages' not in c:
    c = c.replace('})();\n</script>', '})();\n' + cleanup + '\n</script>', 1)
    print("OK - Startup cleanup added")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved")
