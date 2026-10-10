with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('function typeAIMessage(element,text,message){')
if start == -1:
    print('FAIL: typeAIMessage not found')
    raise SystemExit(1)

end_marker = html.find('function stopAITyping(', start)
if end_marker == -1:
    print('FAIL: stopAITyping not found')
    raise SystemExit(1)
end = html.rfind('}', start, end_marker) + 1

new_func = '''function typeAIMessage(element,text,message){
if(activeTypingTimeout){clearTimeout(activeTypingTimeout);activeTypingTimeout=null;}
if(activeTypingMessage && activeTypingMessage!==message){
  try{activeTypingMessage.typing=false;activeTypingMessage.generating=false;}catch(_){}
}
const totalLen=text.length;
if(!totalLen){
  message.typing=false;message.generating=false;message.interrupted=false;
  if(activeTypingMessage===message)activeTypingMessage=null;
  aiIsTyping=false;updateActionButton();renderMessages();return;
}
const targetMs=Math.min(22000,Math.max(3500,totalLen*9));
const tickMs=30;
const totalTicks=Math.max(30,Math.floor(targetMs/tickMs));
const charsPerTick=Math.max(1,Math.ceil(totalLen/totalTicks));
let i=0;
aiIsTyping=true;
activeTypingMessage=message;
message.fullText=text;
updateActionButton();
element.innerHTML='';

function finish(){
  if(activeTypingTimeout){clearTimeout(activeTypingTimeout);activeTypingTimeout=null;}
  if(window._processingIntervals){window._processingIntervals.forEach(ii=>clearInterval(ii));window._processingIntervals=[];}
  message.typing=false;message.generating=false;message.interrupted=false;
  if(activeTypingMessage===message)activeTypingMessage=null;
  aiIsTyping=false;
  try{element.innerHTML=renderMarkdown(text);}catch(_){element.textContent=text;}
  try{
    const wrap=element.closest('.ai-typing-row');
    if(wrap){const av=wrap.querySelector('.ai-typing-avatar');if(av)av.remove();wrap.classList.remove('ai-typing-row');}
  }catch(_){}
  saveChats();updateActionButton();
  try{renderChatList();}catch(_){}
}
function typeNext(){
  if(i<text.length){
    i=Math.min(i+charsPerTick,text.length);
    const partial=text.slice(0,i);
    try{element.innerHTML=renderMarkdown(partial);}catch(_){element.textContent=partial;}
    messagesEl.scrollTop=messagesEl.scrollHeight;
    activeTypingTimeout=setTimeout(typeNext,tickMs);
  }else{finish();}
}
typeNext();
}'''

html = html[:start] + new_func + html[end:]
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK: typeAIMessage fixed — turant finish')
