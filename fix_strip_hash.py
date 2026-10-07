path = 'index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

changed = False

old_h2 = 'h=h.replace(/^## (.+)$/gm,\'<h2 style="font-size:1.25em;margin:14px 0 8px;font-weight:700;">$1</h2>\');'
new_h2 = 'h=h.replace(/^##+ (.+)$/gm,\'<p style="font-size:1.15em;margin:12px 0 6px;font-weight:700;">$1</p>\');'

old_h3 = 'h=h.replace(/^### (.+)$/gm,\'<h3 style="font-size:1.1em;margin:12px 0 6px;font-weight:700;">$1</h3>\');'
new_h3 = 'h=h.replace(/^###+ (.+)$/gm,\'<p style="font-size:1.1em;margin:10px 0 6px;font-weight:700;">$1</p>\');'

old_h1 = 'h=h.replace(/^# (.+)$/gm,\'<h1 style="font-size:1.4em;margin:16px 0 10px;font-weight:700;">$1</h1>\');'
new_h1 = 'h=h.replace(/^#+ (.+)$/gm,\'<p style="font-size:1.2em;margin:14px 0 8px;font-weight:700;">$1</p>\');'

if old_h2 in c:
    c = c.replace(old_h2, new_h2)
    changed = True
    print("✅ h2 replaced")
if old_h3 in c:
    c = c.replace(old_h3, new_h3)
    changed = True
    print("✅ h3 replaced")
if old_h1 in c:
    c = c.replace(old_h1, new_h1)
    changed = True
    print("✅ h1 replaced")

if changed:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Saved")
else:
    print("❌ Patterns nahi mile — manually check karo")
