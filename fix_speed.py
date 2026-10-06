path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = "function typeAIMessage(element,text,message){element.textContent='';let i=0;const speed=35;aiIsTyping=true;activeTypingMessage=message;message.fullText=text;updateActionButton();function typeNext(){if(i<text.length){element.textContent+=text[i++];messagesEl.scrollTop=messagesEl.scrollHeight;activeTypingTimeout=setTimeout(typeNext,speed);}else{message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(text);else element.textContent=text;}catch(_){element.textContent=text;}saveChats();updateActionButton();}}typeNext();}"

new = "function typeAIMessage(element,text,message){element.textContent='';let i=0;const speed=8;const chunk=3;aiIsTyping=true;activeTypingMessage=message;message.fullText=text;updateActionButton();function typeNext(){if(i<text.length){i=Math.min(i+chunk,text.length);const partial=text.slice(0,i);try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(partial);else element.textContent=partial;}catch(_){element.textContent=partial;}messagesEl.scrollTop=messagesEl.scrollHeight;activeTypingTimeout=setTimeout(typeNext,speed);}else{message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(text);else element.textContent=text;}catch(_){element.textContent=text;}saveChats();updateActionButton();}}typeNext();}"

if old in c:
    c = c.replace(old, new)
    print("OK - Typing speed fix ho gaya")
else:
    print("FAIL - pattern nahi mila")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Saved")
