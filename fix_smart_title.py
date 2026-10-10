with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
changes = 0

# ═══ 1. smartTitleFromAI function add karo ═══
smart_fn = '''
function smartTitleFromAI(aiText){
  if(!aiText) return '';
  var lines = String(aiText).split(/\\n+/);
  var skip = /^(KYA[\\s\\-]?KYA|KIS KAAM|SALAH|SAWAAL|📋|🔧|✅|❓|\\d+\\.\\s*(KYA|KIS|SALAH|SAWAAL|📋|🔧|✅|❓))/i;
  for(var i=0;i<lines.length;i++){
    var l = lines[i].replace(/[*#`_>]+/g,' ').replace(/^\\s*[-•●]\\s*/,'').replace(/^\\s*\\d+\\.\\s*/,'').replace(/[\\u{1F300}-\\u{1FAFF}\\u{2600}-\\u{27BF}]/gu,'').trim();
    if(!l) continue;
    if(skip.test(l)) continue;
    if(l.length < 6) continue;
    // "Asset: Gold" jaisa label ho to sirf value lo
    var stripped = l.replace(/^[^:]{1,20}:\\s*/, '').trim();
    var use = (stripped && stripped.length >= 5) ? stripped : l;
    // 6-7 shabd, 42 char tak
    var words = use.split(/\\s+/).slice(0,7).join(' ');
    return words.length > 42 ? words.slice(0,42)+'…' : words;
  }
  return '';
}
'''

if 'function smartTitleFromAI' not in html:
    marker = 'function friendlyChatTitle('
    idx = html.find(marker)
    if idx != -1:
        html = html[:idx] + smart_fn.strip() + '\n\n' + html[idx:]
        print('OK 1: smartTitleFromAI added')
        changes += 1
    else:
        print('WARN 1: friendlyChatTitle not found')
else:
    print('SKIP 1: already there')

# ═══ 2. Vision path — AI reply se title banao ═══
old_v = "pendingReply.text=data.reply||'';"
new_v = "pendingReply.text=data.reply||'';try{var _c=getCurrentChat();var _ut=(text||'').trim();if(_c&&!_ut&&isGenericTitle(_c.title)){var _t=smartTitleFromAI(data.reply||'');if(_t){_c.title=_t;saveChats();try{renderChatList();}catch(_){}}}}catch(_){}"
if old_v in html and 'smartTitleFromAI(data.reply' not in html:
    html = html.replace(old_v, new_v, 1)
    print('OK 2: vision path title update')
    changes += 1
else:
    print('WARN 2: vision text line not found or already')

# ═══ 3. Text path — AI reply se title banao ═══
old_t = "pendingReply.text=replyText;"
new_t = "pendingReply.text=replyText;try{var _c2=getCurrentChat();var _ut2=(text||'').trim();if(_c2&&!_ut2&&isGenericTitle(_c2.title)){var _t2=smartTitleFromAI(replyText);if(_t2){_c2.title=_t2;saveChats();try{renderChatList();}catch(_){}}}}catch(_){}"
if old_t in html and 'smartTitleFromAI(replyText)' not in html:
    html = html.replace(old_t, new_t, 1)
    print('OK 3: text path title update')
    changes += 1
else:
    print('WARN 3: text reply line not found or already')

# ═══ 4. cleanupBadTitles — purani KYA-KYA HAI wali titles bhi theek ═══
old_cleanup = "if(/KYA[\\s\\-]?KYA HAI|KIS KAAM KI|^\\s*SALAH\\b|^\\s*SAWAAL\\b/i.test(t)) needsFix=true;"
new_cleanup = "if(/KYA[\\s\\-]?KYA HAI|KIS KAAM KI|^\\s*SALAH\\b|^\\s*SAWAAL\\b/i.test(t)) needsFix=true;\n    if(/^\\s*\\d+\\.\\s*/.test(t) && t.length > 30) needsFix=true;"
if old_cleanup in html:
    html = html.replace(old_cleanup, new_cleanup, 1)
    print('OK 4: cleanup expanded')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('')
print('TOTAL:', changes)
print('SAVED')
