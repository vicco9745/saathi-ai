path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = """if(mediaAttachments.length>0){
const isPhotoOnly=mediaAttachments.length===1&&mediaAttachments[0].kind==='photo';
{setTimeout(()=>{let replyText;if(mediaAttachments.length===1){const a=mediaAttachments[0];if(a.kind==='video')replyText='Video mil gaya: "'+a.name+'" ('+formatSize(a.size)+').';else if(a.kind==='photo')replyText='Image mil gayi: "'+a.name+'" ('+formatSize(a.size)+').';else replyText='File mil gayi: "'+a.name+'" ('+formatSize(a.size)+').';}else{replyText=mediaAttachments.length+' items mil gaye.';}pendingReply.text=replyText;saveChats();renderMessages();},500);}
}else{"""

new = """if(mediaAttachments.length>0){
const SAATHI_KEY_STORE='saathi_api_key';
let SAATHI_KEY=localStorage.getItem(SAATHI_KEY_STORE);
if(!SAATHI_KEY){SAATHI_KEY=prompt('Saathi API Key dalein:');if(SAATHI_KEY)localStorage.setItem(SAATHI_KEY_STORE,SAATHI_KEY.trim());}
const fileWithContent=mediaAttachments.find(a=>a.content&&a.kind==='file');
let msgToSend=text||'Is photo me kya hai? Puri detail batao';
if(fileWithContent){msgToSend=(text?text+'\\n\\n':'')+'Ye file check karo aur poori detail mein batao kya-kya hai, kya improve karna hai:\\n\\n=== File: '+fileWithContent.name+' ===\\n'+fileWithContent.content;}
fetch(SAATHI_API_BASE+'/v1/chat',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({message:msgToSend,model:currentModel,memory:memoryNotes,attachments:mediaAttachments.filter(a=>a.kind==='photo'&&a.dataUrl).map(a=>({kind:a.kind,dataUrl:a.dataUrl,name:a.name}))})}).then(async res=>{const data=await res.json();if(!res.ok){throw new Error(data.detail||data.error||'API error');}return data;}).then(data=>{pendingReply.text=data.reply||'Koi jawab nahi mila';if(data.kind==='pdf'&&data.pdf_base64){pendingReply.typing=false;pendingReply.attachments=[{kind:'file',name:data.filename||'saathi.pdf',dataUrl:'data:application/pdf;base64,'+data.pdf_base64,origin:'ai'}];}else if(data.kind==='website'&&data.html){pendingReply.typing=false;pendingReply.attachments=[{kind:'file',name:data.filename||'index.html',content:data.html,origin:'ai'}];}else if(data.kind==='image'&&data.image_url){pendingReply.typing=false;pendingReply.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:data.image_url,origin:'ai'}];}saveChats();renderMessages();}).catch(err=>{pendingReply.text='File error: '+err.message;saveChats();renderMessages();});
}else{"""

if old in c:
    c = c.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ File upload fix ho gaya")
else:
    print("❌ Block nahi mila")
