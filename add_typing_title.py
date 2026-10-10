with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old = """element.innerHTML='';

function finish(){"""

new = """element.innerHTML='';

// ═══ Typing ke dauran chat title auto-update ═══
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

function finish(){"""

if old in html:
    html = html.replace(old, new, 1)
    print('OK: typing-time title update added')
elif 'aiPreviewTitle(text)' in html:
    print('SKIP: already added')
else:
    print('FAIL: pattern not found')
    raise SystemExit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
