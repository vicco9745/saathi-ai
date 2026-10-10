with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_fn_start = html.find('function isDesignRequest(text){')
if old_fn_start == -1:
    print('FAIL: function not found')
    raise SystemExit(1)

old_fn_end = html.find('}', html.find('return words.some', old_fn_start)) + 1

new_fn = '''function isDesignRequest(text){
  const t = (text || '').toLowerCase().trim();
  if(t.startsWith('/design')) return true;
  const keys = [
    'design','card','poster','banner','invitation','visiting','greeting',
    'flyer','certificate','menu','wedding','birthday','diwali','marriage',
    'डिज़ाइन','कार्ड','पोस्टर','बैनर','निमंत्रण','शादी','विवाह','जन्मदिन','दिवाली','प्रमाणपत्र'
  ];
  // Match if ANY keyword is present
  return keys.some(function(w){ return t.indexOf(w) !== -1; });
}'''

html = html[:old_fn_start] + new_fn + html[old_fn_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('OK: design detector simplified — ab koi bhi design word match karega')
print('SAVED')
