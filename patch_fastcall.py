p = "index.html"
lines = open(p, encoding="utf-8").read().split("\n")
new = r'''function __cvSplit(t){var out=[],s=t;while(s.length>0&&out.length<16){var cut=-1,m,re=/[\u0964.!?]\s/g,head=s.slice(0,200);if(out.length===0){m=re.exec(head);if(m&&m.index+1>=12&&m.index+1<s.length)cut=m.index+1;}if(cut<0){if(s.length<=200){out.push(s);break;}re.lastIndex=0;while((m=re.exec(head))!==null)cut=m.index+1;if(cut<60)cut=s.lastIndexOf(' ',200);if(cut<1)cut=200;}out.push(s.slice(0,cut).trim());s=s.slice(cut).trim();}return out;}'''
n = 0
for i, l in enumerate(lines):
    if l.startswith("function __cvSplit(t){"):
        lines[i] = new
        n += 1
assert n == 1, "cvSplit line nahi mili"
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("cvSplit patched")
