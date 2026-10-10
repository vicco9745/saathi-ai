with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

helper = '''
async function requestTitleFromServer(text, attachments){
  try{
    const key = localStorage.getItem('saathi_api_key');
    if(!key) return '';
    const body = { message: (text || '').trim() };
    const photo = (attachments || []).find(a => (a.kind === 'photo' || a.kind === 'image') && a.dataUrl);
    if(photo && photo.dataUrl){
      body.image = photo.dataUrl.length > 200000 ? photo.dataUrl.slice(0, 200000) : photo.dataUrl;
    }
    if(!body.message && !body.image) return '';
    const res = await fetch(SAATHI_API_BASE + '/v1/title', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-API-Key': key },
      body: JSON.stringify(body),
    });
    if(!res.ok) return '';
    const data = await res.json();
    return (data.title || '').trim();
  }catch(_){ return ''; }
}
'''

if 'async function requestTitleFromServer' not in html:
    marker = 'function friendlyChatTitle('
    idx = html.find(marker)
    if idx != -1:
        html = html[:idx] + helper.strip() + '\n\n' + html[idx:]
        print('OK 1: requestTitleFromServer added')
    else:
        print('FAIL 1: friendlyChatTitle not found')
        raise SystemExit(1)
else:
    print('SKIP 1: already there')

old = "chat.messages.push({role:'user',text:text,attachments:attachments});"
new = """chat.messages.push({role:'user',text:text,attachments:attachments});
if(isGenericTitle(chat.title)){
  const _capturedId = chat.id;
  requestTitleFromServer(text, attachments).then(function(newTitle){
    if(!newTitle) return;
    try{
      const _c = chats.find(function(x){return x.id === _capturedId;});
      if(_c){
        _c.title = newTitle;
        saveChats();
        try{ renderChatList(); }catch(_){}
      }
    }catch(_){}
  });
}"""
if old in html and 'requestTitleFromServer(text, attachments).then' not in html:
    html = html.replace(old, new, 1)
    print('OK 2: sendMessage title request added')
elif 'requestTitleFromServer(text, attachments).then' in html:
    print('SKIP 2: already there')
else:
    print('WARN 2: push line not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
