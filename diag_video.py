import re, os, subprocess
bad=[0]
def sh(c):
    try:
        return subprocess.run(c,shell=True,capture_output=True,text=True,timeout=45).stdout.strip()
    except Exception as e:
        return "ERR "+str(e)
def ok(n,c,x=""):
    if not c: bad[0]+=1
    print(("[OK]   " if c else "[FAIL] ")+n+((" -> "+x) if x else ""))
def head(t): print("\n=== "+t+" ===")
def rd(p):
    return open(p,encoding="utf-8").read() if os.path.exists(p) else ""
idx=rd("index.html"); js=rd("saathi_video.js"); main=rd("app/main.py")
lines=idx.split("\n")
def grep(pat,n=5,w=220):
    out=[]
    for i,l in enumerate(lines,1):
        if re.search(pat,l):
            out.append("   %d: %s"%(i,l.strip()[:w]))
            if len(out)>=n: break
    return "\n".join(out) if out else "   (kuch nahi mila)"

head("1. FILES AUR GIT")
ok("saathi_video.js maujood",bool(js),str(len(js))+" chars")
if js:
    if sh("which node"):
        r=sh("node --check saathi_video.js 2>&1")
        ok("saathi_video.js syntax sahi",r=="",r[:200])
    else:
        print("[SKIP] node nahi hai, syntax check chhoda")
ok("saathi_video.js git mein hai",sh("git ls-files saathi_video.js")=="saathi_video.js")
ok("98_video.py git mein hai",sh("git ls-files site_patches/98_video.py")!="")
un=sh("git log origin/main..HEAD --oneline")
ok("koi unpushed commit nahi",un=="",un)
st=sh("git status --short")
print("[INFO] git status: "+(st if st else "saaf"))

head("2. INDEX.HTML (local)")
ok("video script tag ek baar hai",idx.count("saathi_video.js?v=2")==1,"saathi_video.js count="+str(idx.count("saathi_video.js")))
ok("module script nahi hai",'type="module"' not in idx and "type='module'" not in idx)
for n in ["pendingAttachments","renderPendingAttachments","updateActionButton","showToast","formatSize"]:
    d=re.search(r"(function\s+%s\b|(let|var|const)\s+%s\b)"%(n,n),idx)
    ok(n+" define hai",bool(d))
print("pendingAttachments ka declaration:\n"+grep(r"(let|var|const)\s+pendingAttachments",2))
print("Video attachment kahan banta hai:\n"+grep(r"kind\s*:\s*'video'",4))
print("origin kahan set hota hai:\n"+grep(r"origin\s*:",5))
print("Photo (frames) wali lines:\n"+grep(r"kind\s*===\s*'photo'",6))
print("'video-frame' ka koi filter:\n"+grep(r"video-frame",3))
print("Video mil gaya wala rasta:\n"+grep(r"mediaAttachments\.length>0&&analyzableFiles",2))

head("3. SERVER (app/main.py)")
ok("_call_vision_v2 hai","def _call_vision_v2" in main)
ok("vision 5 frame leta hai","images[:5]" in main)
ok("/v1/chat route hai","/v1/chat" in main)
m=["   "+l.strip()[:200] for l in main.split("\n") if "images" in l][:8]
print("main.py mein 'images' wali lines:\n"+("\n".join(m) if m else "   (kuch nahi)"))

head("4. LIVE SITE AUR SERVER")
live=sh("curl -s -m 25 https://vicco9745.github.io/saathi-ai/")
ok("live index.html mein tag hai","saathi_video.js?v=2" in live)
r=sh('curl -s -m 25 -o /dev/null -w "%{http_code} %{size_download}" "https://vicco9745.github.io/saathi-ai/saathi_video.js?v=2"')
ok("live saathi_video.js 200 deti hai",r.startswith("200"),r+" bytes, local="+str(len(js.encode("utf-8")))+" bytes")
bases=sorted(set(re.findall(r"https://[A-Za-z0-9\-\.]+onrender\.com",idx)))
print("[INFO] server URL: "+str(bases))
for b in bases[:2]:
    r=sh('curl -s -m 45 -o /dev/null -w "%{http_code} %{time_total}s" '+b+'/')
    ok("server jawab deta hai "+b,not r.startswith("000"),r)

head("5. WORKFLOW")
print("[INFO] site_patches: "+sh("ls site_patches").replace("\n"," "))
ok("apply_all.py hai",os.path.exists("apply_all.py") or os.path.exists("site_patches/apply_all.py"))
wf=rd(".github/workflows/add-format.yml")
ok("workflow apply_all chalata hai","apply_all" in wf)
print("\n=== KUL FAIL: %d ==="%bad[0])
