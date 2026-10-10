with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Purani function dhoondho
start = html.find('function typeAIMessage(element,text,message){')
if start == -1:
    print('FAIL: typeAIMessage not found')
    raise SystemExit(1)

# Function ka end dhoondho — pehla '}\n' jiske baad 'function stopAITyping'
end_marker = html.find('function stopAITyping(', start)
if end_marker == -1:
    print('FAIL: stopAITyping not found')
    raise SystemExit(1)

# Uske peeche ki closing brace tak
end = html.rfind('}', start, end_marker) + 1

new_func = '''function typeAIMessage(element,text,message){
const totalLen=text.length;
if(!totalLen){
  message.typing=false;
  aiIsTyping=false;
  activeTypingMessage=null;
  updateActionButton();
  renderMessages();
  return;
}
// 3.5 se 22 second ke beech — content jitna bada, utna samay, par 22 se zyada nahi
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
function typeNext(){
if(i<text.length){
  i=Math.min(i+charsPerTick,text.length);
  const partial=text.slice(0,i);
  try{element.innerHTML=renderMarkdown(partial);}catch(_){element.textContent=partial;}
  messagesEl.scrollTop=messagesEl.scrollHeight;
  activeTypingTimeout=setTimeout(typeNext,tickMs);
}else{
  // ★ FINISH — saaf-saaf khatam
  if(activeTypingTimeout){clearTimeout(activeTypingTimeout);activeTypingTimeout=null;}
  message.typing=false;
  message.interrupted=false;
  activeTypingMessage=null;
  aiIsTyping=false;
  try{element.innerHTML=renderMarkdown(text);}catch(_){element.textContent=text;}
  saveChats();
  updateActionButton();
  // ★ Ab spinner hatao — poora chat dobara render
  renderMessages();
}
}
typeNext();
}'''

html = html[:start] + new_func + html[end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK: typeAIMessage fixed (spinner stop + slower speed)')
