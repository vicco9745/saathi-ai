with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Line 2284 mein 'attachments' ki jagah 'pendingAttachments' use karo
# (kyunki line 2285 tak attachments banta nahi)

old = "if(chat.messages.length===0 || isGenericTitle(chat.title)){chat.title=friendlyChatTitle(text, attachments);}\nconst attachments=pendingAttachments;"
new = "const attachments=pendingAttachments;\nif(chat.messages.length===0 || isGenericTitle(chat.title)){chat.title=friendlyChatTitle(text, attachments);}"

if old in html:
    html = html.replace(old, new, 1)
    print('OK: attachments pehle define kar diya')
else:
    print('FAIL: pattern nahi mila, alternate try kar rahe hain')
    # Alternate: bas line badal do
    old2 = "if(chat.messages.length===0 || isGenericTitle(chat.title)){chat.title=friendlyChatTitle(text, attachments);}"
    new2 = "if(chat.messages.length===0 || isGenericTitle(chat.title)){chat.title=friendlyChatTitle(text, pendingAttachments);}"
    if old2 in html:
        html = html.replace(old2, new2, 1)
        print('OK: pendingAttachments use kiya')
    else:
        print('FAIL2: manual check karna padega')
        raise SystemExit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
