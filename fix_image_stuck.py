with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
changes = 0

# ═══ Image path — mediaType clear karo jab image aa jaye ═══
old = """pendingReply.generating=false;
if(imgSrc){
pendingReply.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:imgSrc,origin:'ai'}];
pendingReply.text=buildGenReply('image',{caption:data.caption,prompt:imgPrompt});
}else{
pendingReply.mediaType=null;
pendingReply.text='Image generate nahi ho payi.';
}
saveChats();renderMessages();"""

new = """pendingReply.generating=false;
pendingReply.typing=false;
pendingReply.mediaType=null;
if(imgSrc){
pendingReply.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:imgSrc,origin:'ai'}];
pendingReply.text=buildGenReply('image',{caption:data.caption,prompt:imgPrompt});
}else{
pendingReply.text='Image generate nahi ho payi. Server se koi image nahi aayi.';
}
saveChats();renderMessages();"""

if old in html:
    html = html.replace(old, new, 1)
    print('OK 1: image path mediaType clear kiya')
    changes += 1
else:
    print('WARN 1: image block pattern nahi mila')

# ═══ Error catch mein bhi mediaType clear karo ═══
old2 = "pendingReply.generating=false;pendingReply.mediaType=null;pendingReply.text='Image generation error: '+err.message;saveChats();renderMessages();"
new2 = "pendingReply.generating=false;pendingReply.typing=false;pendingReply.mediaType=null;pendingReply.text='Image generation error: '+err.message;saveChats();renderMessages();"

if old2 in html:
    html = html.replace(old2, new2, 1)
    print('OK 2: error path fix')
    changes += 1

# ═══ Video path bhi same fix ═══
old3 = "pendingReply.generating=false;pendingReply.mediaType=null;pendingReply.text='Video generation error: '+err.message;saveChats();renderMessages();"
new3 = "pendingReply.generating=false;pendingReply.typing=false;pendingReply.mediaType=null;pendingReply.text='Video generation error: '+err.message;saveChats();renderMessages();"
if old3 in html:
    html = html.replace(old3, new3, 1)
    print('OK 3: video error path fix')
    changes += 1

# ═══ Video success path bhi ═══
old4 = "pendingReply.generating=false;\nif(videoSrc){"
new4 = "pendingReply.generating=false;\npendingReply.typing=false;\npendingReply.mediaType=null;\nif(videoSrc){"
if old4 in html:
    html = html.replace(old4, new4, 1)
    print('OK 4: video success path fix')
    changes += 1

# ═══ Image path mein bhi: 90 sec timeout — server late ho to bhi loader band ═══
old5 = "fetch(SAATHI_API_BASE+'/v1/image',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({prompt:imgPrompt,model:currentModel,learning:smartCtx})}).then(async res=>{"
new5 = "const _imgTimeout=setTimeout(()=>{if(pendingReply.generating){pendingReply.generating=false;pendingReply.typing=false;pendingReply.mediaType=null;pendingReply.text='Image generation mein zyada samay lag raha hai. Thodi der baad try karein.';saveChats();renderMessages();}},120000);\nfetch(SAATHI_API_BASE+'/v1/image',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':SAATHI_KEY},body:JSON.stringify({prompt:imgPrompt,model:currentModel,learning:smartCtx})}).then(async res=>{clearTimeout(_imgTimeout);"

if old5 in html:
    html = html.replace(old5, new5, 1)
    print('OK 5: image timeout 120 sec')
    changes += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('')
print('TOTAL:', changes)
print('SAVED')
