with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ═══ 1. plainTextForVoice function add karo (markdown hata kar saaf text) ═══
plain_func = '''
function plainTextForVoice(text){
  if(!text) return '';
  let t = String(text);
  // Code fences — content rakho, backticks hatao
  t = t.replace(/```[\\s\\S]*?```/g, function(m){
    return m.replace(/```[a-z]*\\n?/gi, '').replace(/```/g, '');
  });
  // Inline code
  t = t.replace(/`([^`]+)`/g, '$1');
  // Bold **text** aur __text__
  t = t.replace(/\\*\\*([^*]+)\\*\\*/g, '$1');
  t = t.replace(/__([^_]+)__/g, '$1');
  // Italic *text*
  t = t.replace(/(^|[^*])\\*([^*\\n]+)\\*(?!\\*)/g, '$1$2');
  // Headings ## ###
  t = t.replace(/^\\s*#{1,6}\\s+/gm, '');
  // HR
  t = t.replace(/^\\s*[-*_]{3,}\\s*$/gm, '');
  // Bullets * - -> hatao
  t = t.replace(/^\\s*[\\*\\-]\\s+/gm, '');
  // Numbers rakh do — "1." theek hai voice ke liye
  // Blockquote >
  t = t.replace(/^\\s*>\\s+/gm, '');
  // Extra * # ` _ | \ hatao
  t = t.replace(/[*#`_|\\\\]/g, '');
  // Multiple newlines -> ek
  t = t.replace(/\\n{2,}/g, '। ');
  t = t.replace(/\\n/g, ', ');
  return t.trim();
}
'''

if 'function plainTextForVoice(' not in html:
    marker = 'function renderMarkdown(text){'
    idx = html.find(marker)
    if idx == -1:
        print('FAIL: renderMarkdown not found')
        raise SystemExit(1)
    html = html[:idx] + plain_func.strip() + '\n\n' + html[idx:]
    print('OK: plainTextForVoice added')
else:
    print('SKIP: plainTextForVoice already exists')

# ═══ 2. TTS call mein plain text use karo ═══
old_tts = "speakText(message.text||'',null,listenBtn);"
new_tts = "speakText(plainTextForVoice(message.text||''),null,listenBtn);"
if old_tts in html:
    html = html.replace(old_tts, new_tts)
    print('OK: TTS call updated to plain text')
elif new_tts in html:
    print('SKIP: TTS already using plain')
else:
    print('WARN: TTS call not found')

# ═══ 3. copyBtn mein bhi plain text use karo ═══
old_copy = "copyBtn.addEventListener('click',()=>{const text=message.text||'';"
new_copy = "copyBtn.addEventListener('click',()=>{const text=plainTextForVoice(message.text||'');"
if old_copy in html:
    html = html.replace(old_copy, new_copy)
    print('OK: Copy button updated to plain text')
elif 'plainTextForVoice(message.text||\'\')' in html:
    print('SKIP: copy already plain')
else:
    print('WARN: copy button not found')

# ═══ 4. Share bhi plain text se ═══
old_share = "shareBtn.addEventListener('click',async()=>{const text=message.text||'';"
new_share = "shareBtn.addEventListener('click',async()=>{const text=plainTextForVoice(message.text||'');"
if old_share in html:
    html = html.replace(old_share, new_share)
    print('OK: Share button updated to plain text')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
