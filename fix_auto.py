path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = """pendingReply.text=replyText;if(Array.isArray(data.suggestions)&&data.suggestions.length>0)pendingReply.suggestions=data.suggestions.slice(0,4);if(Array.isArray(data.sources)&&data.sources.length>0)pendingReply.sources=data.sources.slice(0,10);saveChats();renderMessages();}"""

new = """pendingReply.text=replyText;if(data.kind==='pdf'&&data.pdf_base64){pendingReply.typing=false;pendingReply.attachments=[{kind:'file',name:data.filename||'saathi.pdf',dataUrl:'data:application/pdf;base64,'+data.pdf_base64,origin:'ai'}];}else if(data.kind==='website'&&data.html){pendingReply.typing=false;pendingReply.attachments=[{kind:'file',name:data.filename||'index.html',content:data.html,origin:'ai'}];}else if(data.kind==='image'&&data.image_url){pendingReply.typing=false;pendingReply.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:data.image_url,origin:'ai'}];}if(Array.isArray(data.suggestions)&&data.suggestions.length>0)pendingReply.suggestions=data.suggestions.slice(0,4);if(Array.isArray(data.sources)&&data.sources.length>0)pendingReply.sources=data.sources.slice(0,10);saveChats();renderMessages();}"""

if old in c:
    c = c.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Fix ho gaya!")
else:
    print("❌ Block nahi mila")
