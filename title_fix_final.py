with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ═══ 1. Helpers add karo ═══
helper = '''
function friendlyChatTitle(text, attachments){
  const t = (text || '').trim();
  if(t){
    const clean = t.replace(/\\s+/g, ' ').trim();
    return clean.length > 40 ? clean.slice(0, 40) + '…' : clean;
  }
  const atts = attachments || [];
  if(atts.length === 0) return 'New chat';
  const kinds = [...new Set(atts.map(a => a.kind || 'file'))];
  if(kinds.length === 1){
    const k = kinds[0];
    if(k === 'photo' || k === 'image') return 'Photo message';
    if(k === 'video') return 'Video message';
    if(k === 'text') return 'Pasted content';
    if(k === 'file') return 'File message';
  }
  if(kinds.includes('photo') && kinds.includes('video')) return 'Photo & video';
  return 'Attachment message';
}

function isGenericTitle(t){
  t = (t || '').trim();
  if(!t) return true;
  if(t === 'New chat') return true;
  if(/^(Photo message|Video message|File message|Pasted content|Attachment message|Photo & video)$/i.test(t)) return true;
  if(/\\.(jpg|jpeg|png|gif|webp|mp4|mov|pdf|txt|doc|docx)$/i.test(t)) return true;
  return false;
}

function aiPreviewTitle(aiText){
  if(!aiText) return '';
  // Pehli line ya pehla vaakya lo, saaf karo
  let t = String(aiText)
    .replace(/[*#`_>\\-]+/g, ' ')
    .replace(/\\s+/g, ' ')
    .trim();
  // Emoji aur special chars hata do shuruaat se
  t = t.replace(/^[\\p{Emoji}\\p{Punct}\\s]+/u, '').trim();
  if(!t) return '';
  // Pehla vaakya — 40 chars tak
  const m = t.match(/^[^।.!?\\n]{5,60}/);
  const candidate = m ? m[0].trim() : t.slice(0, 40).trim();
  if(!candidate) return '';
  return candidate.length > 40 ? candidate.slice(0, 40) + '…' : candidate;
}
'''

if 'function friendlyChatTitle(' not in html:
    marker = 'function genId(){'
    idx = html.find(marker)
    if idx == -1:
        print('FAIL: genId not found')
        raise SystemExit(1)
    html = html[:idx] + helper.strip() + '\n\n' + html[idx:]
    print('OK: helpers added')
else:
    print('SKIP: helpers exist')

# ═══ 2. sendMessage — title banao ═══
old1 = "if(chat.messages.length===0){const titleSource=text||(pendingAttachments[0]?pendingAttachments[0].name:'New chat');chat.title=titleSource.length>28?titleSource.slice(0,28)+'…':titleSource;}"
new1 = "if(chat.messages.length===0){chat.title=friendlyChatTitle(text, attachments);}"
if old1 in html:
    html = html.replace(old1, new1, 1)
    print('OK: sendMessage title')
elif 'friendlyChatTitle(text, attachments)' in html:
    print('SKIP: already updated')

# ═══ 3. typeAIMessage mein title auto-update ═══
old_typing = "element.innerHTML='';\nfunction typeNext(){"
new_typing = """element.innerHTML='';
try{
  const _c=getCurrentChat();
  if(_c && isGenericTitle(_c.title)){
    const preview=aiPreviewTitle(text);
    if(preview){
      _c.title=preview;
      try{renderChatList();}catch(_){}
    }
  }
}catch(_){}
function typeNext(){"""
if old_typing in html:
    html = html.replace(old_typing, new_typing, 1)
    print('OK: typing-time auto title')
else:
    print('WARN: typing loop not found')

# ═══ 4. Live message functions ═══
old2 = "chat = { id: genId(), title: text ? (text.length > 28 ? text.slice(0, 28) + '…' : text) : 'New chat', messages: [] };"
new2 = "chat = { id: genId(), title: friendlyChatTitle(text, attachments), messages: [] };"
if old2 in html:
    html = html.replace(old2, new2)
    print('OK: live chat title')

old3 = "if (chat.messages.length === 0 && text) {chat.title = text.length > 28 ? text.slice(0, 28) + '…' : text;}"
new3 = "if (chat.messages.length === 0) {chat.title = friendlyChatTitle(text, attachments);}"
if old3 in html:
    html = html.replace(old3, new3)
    print('OK: live msg title')

old4 = "if(chat.messages.length===0){chat.title=text.length>28?text.slice(0,28)+'…':text;}"
new4 = "if(chat.messages.length===0){chat.title=friendlyChatTitle(text, []);}"
if old4 in html:
    html = html.replace(old4, new4)
    print('OK: live text title')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
