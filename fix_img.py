with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old = "const imgSrc=data.image_url||(data.image_base64?('data:image/png;base64,'+data.image_base64):null);pendingReply.generating=false;if(imgSrc){pendingReply.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:imgSrc,origin:'ai'}];pendingReply.text=buildGenReply('image',{caption:data.caption,prompt:imgPrompt});}else{pendingReply.mediaType=null;pendingReply.text='Image generate nahi ho payi.';}saveChats();renderMessages();"

new = "const imgSrc=data.image_url||(data.image_base64?('data:image/png;base64,'+data.image_base64):null);pendingReply.generating=false;pendingReply.typing=false;pendingReply.mediaType=null;if(imgSrc){pendingReply.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:imgSrc,origin:'ai'}];pendingReply.text=buildGenReply('image',{caption:data.caption,prompt:imgPrompt});}else{pendingReply.text='Image generate nahi ho payi. Server se koi image nahi aayi.';}saveChats();renderMessages();"

if old in html:
    html = html.replace(old, new, 1)
    print('OK: image path fix — mediaType null + typing false')
else:
    print('FAIL: pattern nahi mila')
    raise SystemExit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
