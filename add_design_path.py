with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# sendMessage ke andar — SAATHI_KEY define hone ke baad design check lagao
old = "const SAATHI_KEY_STORE='saathi_api_key';"
new = """// ═══ DESIGN PATH ═══
if(isDesignRequest(text)){
  const SAATHI_KEY_STORE_D='saathi_api_key';
  let SAATHI_KEY_D=localStorage.getItem(SAATHI_KEY_STORE_D);
  if(!SAATHI_KEY_D){SAATHI_KEY_D=prompt('Saathi API Key:');if(SAATHI_KEY_D)localStorage.setItem(SAATHI_KEY_STORE_D,SAATHI_KEY_D.trim());}
  const designPrompt = extractDesignPrompt(text) || 'Ek sundar design banao';
  const photoAtt = attachments.find(a => (a.kind==='photo'||a.kind==='image') && a.dataUrl);
  pendingReply.text = 'Design ban raha hai...';
  saveChats(); renderMessages();
  fetch(SAATHI_API_BASE+'/v1/design',{
    method:'POST',
    headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY_D},
    body:JSON.stringify({prompt:designPrompt, photo:photoAtt?photoAtt.dataUrl:null, model:currentModel})
  })
  .then(async res=>{const data=await res.json();if(!res.ok){if(res.status===401||res.status===403){localStorage.removeItem(SAATHI_KEY_STORE_D);}throw new Error(data.detail||data.error||'Design error');}return data;})
  .then(data=>{
    pendingReply.text = data.reply || 'Yeh raha aapka design.';
    if(data.html){
      pendingReply.attachments = [{kind:'file',name:data.filename||'design.html',content:data.html,origin:'ai'}];
    }
    pendingReply.typing = true;
    saveChats(); renderMessages();
  })
  .catch(err=>{pendingReply.text='Design error: '+err.message;pendingReply.typing=true;saveChats();renderMessages();});
  return;
}

const SAATHI_KEY_STORE='saathi_api_key';"""

if 'isDesignRequest(text)' in html and '// ═══ DESIGN PATH ═══' not in html:
    html = html.replace(old, new, 1)
    print('OK: design path added')
elif '// ═══ DESIGN PATH ═══' in html:
    print('SKIP: already there')
else:
    print('FAIL: SAATHI_KEY_STORE not found')
    raise SystemExit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
