path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = """if(data.kind==='pdf'&&data.pdf_base64){pendingReply.attachments=[{kind:'file',name:data.filename||'saathi.pdf',dataUrl:'data:application/pdf;base64,'+data.pdf_base64,origin:'ai'}];}"""

new = """if(data.kind==='pdf'&&data.pdf_base64){pendingReply.typing=false;pendingReply.attachments=[{kind:'file',name:data.filename||'saathi.pdf',dataUrl:'data:application/pdf;base64,'+data.pdf_base64,origin:'ai'}];}"""

if old in c:
    c = c.replace(old, new)
    print("✅ Step 1 done")
else:
    print("❌ Step 1 failed")

# Also add pdf render in renderMessages - check if there's a PDF specific handling
# Find the section where attachments are rendered
old2 = """if(attachments.length>0)row.appendChild(buildAttachmentsBlock(attachments));
if(m.text||(m.role==='ai'&&m.typing)){"""

new2 = """if(attachments.length>0)row.appendChild(buildAttachmentsBlock(attachments));
if(m.role==='ai'&&!m.typing&&attachments.length>0&&attachments[0].name&&attachments[0].name.toLowerCase().endsWith('.pdf')){const idx2=chat.messages.indexOf(m);if(idx2>=0){row.appendChild(buildMessageActions(m,idx2,chat,false));}}
if(m.text||(m.role==='ai'&&m.typing)){"""

if old2 in c:
    c = c.replace(old2, new2)
    print("✅ Step 2 done")
else:
    print("⚠️ Step 2 - block not found (skip)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ File saved")
