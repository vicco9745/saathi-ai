import json, subprocess, sys
F = "ichat_ai/abilities.json"
if len(sys.argv) < 3 or sys.argv[2] not in ("ok", "broken"):
    print('use: python ability.py <video|photo|chrome> <ok|broken> ["kya gadbadi hai"]')
    sys.exit(1)
key, st = sys.argv[1], sys.argv[2]
note = sys.argv[3] if len(sys.argv) > 3 else ""
items = json.load(open(F, encoding="utf-8"))
hit = [it for it in items if it.get("key") == key]
if not hit:
    print("aisi suvidha nahi mili:", key, "| milti hain:", [it.get("key") for it in items])
    sys.exit(1)
hit[0]["status"] = st
hit[0]["note"] = note if st == "broken" else ""
with open(F, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)
for c in (["git", "add", F], ["git", "commit", "-m", "ability %s %s" % (key, st)], ["git", "pull", "--rebase"], ["git", "push"]):
    subprocess.run(c)
print(key, "->", st, "| Render ke Live hone mein 2-4 minute lagenge")
