with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

# ═══ 1. addLiveUserText — pehla title theek karo ═══
old1 = "chat={id:genId(),title:text.length>28?text.slice(0,28)+'…':text,messages:[]}"
new1 = "chat={id:genId(),title:friendlyChatTitle(text,[]),messages:[]}"
if old1 in html:
    html = html.replace(old1, new1)
    print('OK: addLiveUserText title fixed')
    changes += 1

# ═══ 2. addLiveUserMessage — pehla title ═══
old2 = "chat = { id: genId(), title: text ? (text.length > 28 ? text.slice(0, 28) + '…' : text) : 'New chat', messages: [] };"
new2 = "chat = { id: genId(), title: friendlyChatTitle(text, attachments), messages: [] };"
if old2 in html:
    html = html.replace(old2, new2)
    print('OK: addLiveUserMessage title fixed')
    changes += 1

# ═══ 3. sendMessage — title hamesha update ho (generic ho ya na ho) ═══
old3 = "if(chat.messages.length===0){chat.title=friendlyChatTitle(text, attachments);}"
new3 = "if(chat.messages.length===0 || isGenericTitle(chat.title)){chat.title=friendlyChatTitle(text, attachments);}"
if old3 in html:
    html = html.replace(old3, new3)
    print('OK: sendMessage title always updates')
    changes += 1

# ═══ 4. AI typing ke dauran title badle ═══
old4 = "element.innerHTML='';\n\nfunction finish(){"
new4 = """element.innerHTML='';
try{
  const _c=getCurrentChat();
  if(_c && isGenericTitle(_c.title)){
    const _preview=aiPreviewTitle(text);
    if(_preview){
      _c.title=_preview;
      try{saveChats();}catch(_){}
      try{renderChatList();}catch(_){}
    }
  }
}catch(_){}

function finish(){"""
if old4 in html:
    html = html.replace(old4, new4, 1)
    print('OK: AI typing title update added')
    changes += 1

# ═══ 5. Purani chats ke kachche filename titles ko fix karo app load par ═══
old5 = "function renderChatList(){"
new5 = """function cleanupBadTitles(){
  let ch=false;
  chats.forEach(function(c){
    var t=(c.title||'').trim();
    if(/\\.(jpg|jpeg|png|gif|webp|mp4|mov|pdf|txt|doc|docx)$/i.test(t)){
      // Purana filename title — chat ke pehle message se naya naam nikaalo
      var firstUser=(c.messages||[]).find(function(m){return m.role==='user';});
      if(firstUser && firstUser.text && firstUser.text.trim()){
        c.title=friendlyChatTitle(firstUser.text,[]);
      }else if(firstUser && firstUser.attachments && firstUser.attachments.length){
        c.title=friendlyChatTitle('',firstUser.attachments);
      }else{
        c.title='Chat';
      }
      ch=true;
    }
  });
  if(ch){try{saveChats();}catch(_){}}
}

function renderChatList(){"""
if old5 in html and 'function cleanupBadTitles' not in html:
    html = html.replace(old5, new5, 1)
    print('OK: cleanupBadTitles added')
    changes += 1

# ═══ 6. Load par cleanup chalao ═══
old6 = "renderChatList();\nrenderMessages();"
new6 = "cleanupBadTitles();\nrenderChatList();\nrenderMessages();"
if old6 in html:
    html = html.replace(old6, new6, 1)
    print('OK: cleanup called on load')
    changes += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('')
print('TOTAL CHANGES:', changes)
print('SAVED')
