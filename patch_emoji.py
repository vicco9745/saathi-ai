p = "index.html"
s = open(p, encoding="utf-8").read()
a = ".replace(/[*#_>~|]+/g,' ').replace(/\\s+/g,' ').trim();}"
assert s.count("function __cvClean(t){") == 1, "cvClean nahi mila"
i = s.index("function __cvClean(t){")
j = s.index("\n", i)
line = s[i:j]
assert line.count(a) == 1, "cvClean ka ant match nahi mila"
b = ".replace(/[*#_>~|]+/g,' ').replace(/[\\u{1F000}-\\u{1FAFF}\\u{2600}-\\u{27BF}\\u{2B00}-\\u{2BFF}\\u{FE0F}\\u{200D}\\u{2190}-\\u{21FF}]/gu,' ').replace(/\\s+/g,' ').trim();}"
open(p, "w", encoding="utf-8").write(s[:i] + line.replace(a, b, 1) + s[j:])
print("emoji patched")
