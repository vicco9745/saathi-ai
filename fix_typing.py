with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_func = '''function typeAIMessage(element,text,message){element.textContent='';let i=0;const speed=35;aiIsTyping=true;activeTypingMessage=message;message.fullText=text;updateActionButton();function typeNext(){if(i<text.length){element.textContent+=text[i++];messagesEl.scrollTop=messagesEl.scrollHeight;activeTypingTimeout=setTimeout(typeNext,speed);}else{message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;saveChats();updateActionButton();renderMessages();}}typeNext();}'''

new_func = '''function typeAIMessage(element,text,message){
const totalLen=text.length;
if(!totalLen){message.typing=false;aiIsTyping=false;activeTypingMessage=null;updateActionButton();renderMessages();return;}
const targetMs=Math.min(22000,Math.max(2500,totalLen*6));
const tickMs=28;
const totalTicks=Math.max(20,Math.floor(targetMs/tickMs));
const charsPerTick=Math.max(1,Math.ceil(totalLen/totalTicks));
let i=0;
aiIsTyping=true;
activeTypingMessage=message;
message.fullText=text;
updateActionButton();
element.innerHTML='';
function typeNext(){
if(i<text.length){
i=Math.min(i+charsPerTick,text.length);
const partial=text.slice(0,i);
try{element.innerHTML=renderMarkdown(partial);}catch(_){element.textContent=partial;}
messagesEl.scrollTop=messagesEl.scrollHeight;
activeTypingTimeout=setTimeout(typeNext,tickMs);
}else{
message.typing=false;
message.interrupted=false;
activeTypingTimeout=null;
activeTypingMessage=null;
aiIsTyping=false;
try{element.innerHTML=renderMarkdown(text);}catch(_){element.textContent=text;}
saveChats();
updateActionButton();
}
}
typeNext();
}'''

if old_func in html:
    html = html.replace(old_func, new_func, 1)
    print('OK: typeAIMessage updated')
elif 'const targetMs=Math.min' in html:
    print('SKIP: already updated')
else:
    print('FAIL: typeAIMessage not found')
    raise SystemExit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
