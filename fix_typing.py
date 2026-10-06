path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Fix 1: typeAIMessage - render markdown immediately when done
old1 = """message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;saveChats();updateActionButton();renderMessages();}}"""

new1 = """message.typing=false;message.interrupted=false;activeTypingTimeout=null;activeTypingMessage=null;aiIsTyping=false;try{if(typeof renderMarkdown==='function')element.innerHTML=renderMarkdown(text);else element.textContent=text;}catch(_){element.textContent=text;}saveChats();updateActionButton();}}"""

if old1 in c:
    c = c.replace(old1, new1)
    print("✅ typeAIMessage fix ho gaya")
else:
    print("⚠️ typeAIMessage pattern nahi mila")

# Fix 2: Regenerate - use renderMarkdown
old2 = "'Yeh ek naya demo reply hai. Yahan apna AI / API response jodo.'"
new2 = "'Yeh ek naya demo reply hai. Yahan apna AI / API response jodo.'"
# Leave regenerate as is for now

# Fix 3: Make sure renderMarkdown wraps paragraphs
old3 = "h=h.replace(/\\n/g,'<br>');"
new3 = """h=h.replace(/\\n\\n+/g,'</p><p style="margin:8px 0;">');
h=h.replace(/\\n/g,'<br>');
h='<p style="margin:0;">'+h+'</p>';"""

if old3 in c:
    c = c.replace(old3, new3, 1)
    print("✅ Paragraph wrapping added")
else:
    print("⚠️ newline pattern nahi mila")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ File saved")
