path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Add markdown renderer before renderMessages function
marker = "function renderMessages(){"

md_fn = '''function renderMarkdown(t){
if(!t)return'';
let h=t;
h=h.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
h=h.replace(/^### (.+)$/gm,'<h3 style="font-size:1.1em;margin:12px 0 6px;font-weight:700;">$1</h3>');
h=h.replace(/^## (.+)$/gm,'<h2 style="font-size:1.25em;margin:14px 0 8px;font-weight:700;">$1</h2>');
h=h.replace(/^# (.+)$/gm,'<h1 style="font-size:1.4em;margin:16px 0 10px;font-weight:700;">$1</h1>');
h=h.replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>');
h=h.replace(/(?<!\\*)\\*([^*\\n]+)\\*(?!\\*)/g,'<em>$1</em>');
h=h.replace(/`([^`]+)`/g,'<code style="background:rgba(0,0,0,0.06);padding:2px 6px;border-radius:4px;font-family:monospace;font-size:0.9em;">$1</code>');
h=h.replace(/^\\s*[-*] (.+)$/gm,'<li style="margin:4px 0;">$1</li>');
h=h.replace(/^\\s*(\\d+)\\. (.+)$/gm,'<li style="margin:4px 0;">$2</li>');
h=h.replace(/(<li[^>]*>.*?<\\/li>\\n?)+/g,function(m){return '<ul style="margin:8px 0;padding-left:22px;">'+m+'</ul>';});
h=h.replace(/^---$/gm,'<hr style="border:none;border-top:1px solid var(--border);margin:14px 0;">');
h=h.replace(/\\[([^\\]]+)\\]\\((https?:\\/\\/[^)]+)\\)/g,'<a href="$2" target="_blank" rel="noopener" class="msg-link">$1</a>');
h=h.replace(/(https?:\\/\\/[^\\s<]+)/g,function(u){return u.indexOf('href=')!==-1?u:'<a href="'+u+'" target="_blank" rel="noopener" class="msg-link">'+u+'</a>';});
h=h.replace(/\\n/g,'<br>');
return h;
}

'''

if 'function renderMarkdown' not in c:
    c = c.replace(marker, md_fn + marker, 1)
    print("✅ renderMarkdown जोड़ दिया")
else:
    print("⚠️ पहले से है")

# Replace linkifyText with renderMarkdown in message display
c = c.replace('bubble.innerHTML=linkifyText(m.text)', 'bubble.innerHTML=renderMarkdown(m.text)')
c = c.replace('bubble.innerHTML = linkifyText(m.text)', 'bubble.innerHTML = renderMarkdown(m.text)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ File saved")
