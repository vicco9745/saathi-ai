p = 'index.html'
s = open(p, encoding='utf-8').read()
FN = r"""function __chatArtifact(m,d,prompt){try{if(!d)return false;
if(d.kind==='website'&&d.html){m.typing=false;m.processing=null;m.attachments=[{kind:'file',name:d.filename||'index.html',content:d.html,origin:'ai'}];m.text=buildGenReply('website',{caption:d.caption,html:d.html,prompt:prompt});try{saveChats();renderMessages();}catch(_){}try{__describeSite(m,prompt,d.html);}catch(_){}try{clearTypingState();updateActionButton();}catch(_){}return true;}
if(d.kind==='image'&&d.image_url){m.mediaType='photo';m.generating=true;m.text='';try{saveChats();renderMessages();}catch(_){}__imgWait(d.image_url).then(function(u){m.generating=false;m.typing=false;m.attachments=[{kind:'photo',name:'saathi-generated-image',dataUrl:u,origin:'ai'}];m.text='';try{publishToGallery('photo',u);}catch(_){}try{saveChats();renderMessages();clearTypingState();updateActionButton();}catch(_){}}).catch(function(){m.generating=false;m.typing=false;m.mediaType=null;m.text='Image generate nahi ho payi.';try{saveChats();renderMessages();clearTypingState();updateActionButton();}catch(_){}});return true;}
}catch(_){}return false;}
"""
a1 = 'function linkifyText(text){'
old = ".then(data=>{const replyText=data.reply||'Saathi से जवाब नहीं मिला।';"
new = ".then(data=>{if(__chatArtifact(pendingReply,data,combinedText)){return;}const replyText=data.reply||'Saathi से जवाब नहीं मिला।';"
if '__chatArtifact' in s:
    print('chatartifact: pehle se laga hai')
elif s.count(a1) == 1 and s.count(old) == 1:
    s = s.replace(a1, FN + a1, 1).replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('chatartifact: laga diya')
else:
    print('chatartifact: jagah nahi mili', s.count(a1), s.count(old))
