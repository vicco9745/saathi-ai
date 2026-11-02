p = 'index.html'
s = open(p, encoding='utf-8').read()
old = "let SAATHI_KEY=localStorage.getItem(SAATHI_KEY_STORE);"
add = "\nwindow.__sc={chats:function(){return chats;},key:function(){return SAATHI_KEY;},api:function(){return SAATHI_API_BASE;},save:function(){saveChats();},render:function(){renderChatList();}};"
if 'window.__sc=' in s:
    print('pehle se laga hua hai')
elif s.count(old) != 1:
    print('jagah nahi mili', s.count(old))
else:
    open(p, 'w', encoding='utf-8').write(s.replace(old, old + add))
    print('done')
