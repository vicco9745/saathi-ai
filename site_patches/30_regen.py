p='index.html'
L=open(p,encoding='utf-8').read().split('\n')
new=r'''function regenerateReply(chat,idx){const msg=chat.messages[idx];if(!msg)return;let q='';for(let i=idx-1;i>=0;i--){if(chat.messages[i].role!=='ai'){q=String(chat.messages[i].text||'');break;}}if(!q.trim()){showToast('Pichhla sawal nahi mila');return;}chat.messages.splice(idx,1);const fresh={role:'ai',text:'',typing:true};chat.messages.push(fresh);saveChats();renderMessages();const KEY=localStorage.getItem('saathi_api_key');fetch(SAATHI_API_BASE+'/v1/chat',{method:'POST',headers:{'Content-Type':'application/json','X-API-Key':KEY},body:JSON.stringify({message:q,model:currentModel,memory:(addMemoryOn?memoryNotes:[]),learning:getSmartLearningContext(),allow_web_search:addWebSearchOn,think:addThinkOn})}).then(async res=>{const data=await res.json();if(!res.ok)throw new Error(data.detail||data.error||'API error');return data;}).then(data=>{fresh.text=data.reply||'Saathi से जवाब नहीं मिला।';if(Array.isArray(data.suggestions)&&data.suggestions.length>0)fresh.suggestions=data.suggestions.slice(0,4);if(Array.isArray(data.sources)&&data.sources.length>0)fresh.sources=data.sources.slice(0,10);saveChats();renderMessages();}).catch(err=>{fresh.text='Saathi connection error: '+err.message;saveChats();renderMessages();});}'''
n=0
for i,l in enumerate(L):
    if l.startswith('function regenerateReply(chat,idx){') and '/v1/chat' not in l:
        L[i]=new;n+=1
open(p,'w',encoding='utf-8').write('\n'.join(L))
print('regen patch:',n)
