with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Purani design path hatao (galat jagah se)
old_design = """// ═══ DESIGN PATH ═══
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

"""

if old_design in html:
    html = html.replace(old_design, '', 1)
    print('OK 1: purani (galat jagah wali) design path hata di')
else:
    print('WARN 1: purani design path mili nahi')

# Ab naya design check — sabse upar, sabse pehle
# Iska matlab: koi bhi design word ho (photo ho ya na ho), to design banega
new_design = """const SAATHI_KEY_STORE='saathi_api_key';
let SAATHI_KEY=localStorage.getItem(SAATHI_KEY_STORE);
if(!SAATHI_KEY){SAATHI_KEY=prompt('Saathi API Key डालें:');if(SAATHI_KEY)localStorage.setItem(SAATHI_KEY_STORE,SAATHI_KEY.trim());}

// ═══ DESIGN PATH — photo ho ya na ho, koi bhi design keyword match hone par ═══
if(isDesignRequest(text)){
  const designPrompt = extractDesignPrompt(text) || 'Ek sundar design banao';
  const photoAtt = attachments.find(a => (a.kind==='photo'||a.kind==='image') && a.dataUrl);
  pendingReply.text = 'Design ban raha hai...';
  saveChats(); renderMessages();
  fetch(SAATHI_API_BASE+'/v1/design',{
    method:'POST',
    headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},
    body:JSON.stringify({prompt:designPrompt, photo:photoAtt?photoAtt.dataUrl:null, model:currentModel})
  })
  .then(async res=>{const data=await res.json();if(!res.ok){if(res.status===401||res.status===403){localStorage.removeItem(SAATHI_KEY_STORE);}throw new Error(data.detail||data.error||'Design error');}return data;})
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
"""

# Ye check media path se PEHLE aana chahiye — sendMessage ke andar
# Pattern: "const mediaAttachments=" line ke pehle
pattern = "const mediaAttachments=attachments.filter(a=>a.kind!=='text');"
if pattern in html and '// ═══ DESIGN PATH — photo ho ya na ho' not in html:
    html = html.replace(pattern, new_design + "\n" + pattern, 1)
    print('OK 2: naya design path sahi jagah lagaya')
else:
    print('WARN 2: mediaAttachments pattern nahi mila')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
