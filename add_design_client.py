with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

helper = '''
function isDesignRequest(text){
  const t = (text || '').toLowerCase().trim();
  if(t.startsWith('/design')) return true;
  const words = ['design banao','card banao','poster banao','banner banao','invitation banao','visiting card','greeting card','flyer banao','certificate banao','menu banao','wedding card','birthday card','diwali card','शादी का कार्ड','निमंत्रण','पोस्टर','बैनर','डिज़ाइन'];
  return words.some(w => t.includes(w));
}
function extractDesignPrompt(text){
  const t = (text || '').trim();
  if(t.toLowerCase().startsWith('/design')){
    return t.replace(/^\\/design\\s*/i, '').trim();
  }
  return t;
}
'''

if 'function isDesignRequest(' not in html:
    marker = 'function friendlyChatTitle('
    idx = html.find(marker)
    if idx != -1:
        html = html[:idx] + helper.strip() + '\n\n' + html[idx:]
        print('OK 1: design helpers added')
    else:
        print('FAIL 1')
        raise SystemExit(1)
else:
    print('SKIP 1: already there')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('SAVED')
