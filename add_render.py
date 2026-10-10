with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

md_func = '''
function renderMarkdown(text){
  if(!text) return '';
  let t = String(text)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');

  // Code fence
  t = t.replace(/```([\\s\\S]*?)```/g, function(m, code){
    return '<pre style="background:var(--icon-hover);padding:10px 12px;border-radius:10px;overflow-x:auto;font-family:monospace;font-size:13px;margin:8px 0;white-space:pre-wrap;word-break:break-word;">'+code.replace(/^\\n+|\\n+$/g,'')+'</pre>';
  });

  // Inline code
  t = t.replace(/`([^`\\n]+)`/g, '<code style="background:var(--icon-hover);padding:2px 6px;border-radius:5px;font-family:monospace;font-size:.92em;">$1</code>');

  // Headings
  t = t.replace(/^\\s*###\\s+(.+)$/gm, '<div style="font-size:14.5px;font-weight:700;margin:14px 0 6px;color:var(--text);">$1</div>');
  t = t.replace(/^\\s*##\\s+(.+)$/gm,  '<div style="font-size:16.5px;font-weight:700;margin:16px 0 8px;color:var(--text);">$1</div>');
  t = t.replace(/^\\s*#\\s+(.+)$/gm,   '<div style="font-size:18.5px;font-weight:700;margin:18px 0 10px;color:var(--text);">$1</div>');

  // Bold
  t = t.replace(/\\*\\*([^*\\n]+)\\*\\*/g, '<strong style="font-weight:700;">$1</strong>');
  t = t.replace(/__([^_\\n]+)__/g, '<strong style="font-weight:700;">$1</strong>');

  // Italic
  t = t.replace(/(^|[^*])\\*([^*\\n]+)\\*(?!\\*)/g, '$1<em>$2</em>');

  // HR
  t = t.replace(/^\\s*[-*_]{3,}\\s*$/gm, '<div style="border-top:1px solid var(--border);margin:14px 0;"></div>');

  // Bullets - * -> nice dot
  t = t.replace(/^\\s*[\\*\\-]\\s+(.+)$/gm, '<div style="display:flex;gap:8px;margin:5px 0;padding-left:2px;"><span style="flex-shrink:0;color:var(--accent);font-weight:700;line-height:1.6;">•</span><span style="flex:1;">$1</span></div>');

  // Numbered
  t = t.replace(/^\\s*(\\d+)\\.\\s+(.+)$/gm, '<div style="display:flex;gap:8px;margin:5px 0;padding-left:2px;"><span style="flex-shrink:0;font-weight:600;color:var(--text-soft);min-width:20px;">$1.</span><span style="flex:1;">$2</span></div>');

  // Blockquote
  t = t.replace(/^&gt;\\s+(.+)$/gm, '<div style="border-left:3px solid var(--accent);padding:6px 12px;margin:8px 0;background:var(--icon-hover);border-radius:0 8px 8px 0;color:var(--text-soft);">$1</div>');

  // ═══ LAST: koi bhi bacha hua * ya # hata do ═══
  t = t.replace(/\\*/g, '');
  t = t.replace(/#/g, '');

  // Breaks
  t = t.replace(/\\n{2,}/g, '</p><p style="margin:8px 0;">');
  t = t.replace(/\\n/g, '<br>');

  return '<p style="margin:8px 0;">' + t + '</p>';
}
'''

if 'function renderMarkdown(' not in html:
    marker = 'function linkifyText(text){'
    idx = html.find(marker)
    if idx == -1:
        print('FAIL: linkifyText not found')
        raise SystemExit(1)
    html = html[:idx] + md_func.strip() + '\n\n' + html[idx:]
    print('OK: renderMarkdown added')
else:
    print('SKIP: renderMarkdown already exists')

# AI bubble -> renderMarkdown
repl = [
    ('bubble.innerHTML=linkifyText(m.text);row.appendChild(bubble);',
     'bubble.innerHTML=renderMarkdown(m.text);row.appendChild(bubble);'),
]
for old, new in repl:
    if old in html:
        n = html.count(old)
        html = html.replace(old, new)
        print('OK: replaced bubble render x' + str(n))

# Typing finish: typeAIMessage ke baad final bubble markdown mein render karo
old_finish = "activeTypingMessage=null;aiIsTyping=false;saveChats();updateActionButton();renderMessages();"
new_finish = "activeTypingMessage=null;aiIsTyping=false;saveChats();updateActionButton();renderMessages();"
# Already calls renderMessages — no change needed

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('SAVED index.html')
