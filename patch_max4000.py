import re
p = "ichat_ai/ai_providers.py"
s = open(p, encoding="utf-8").read()
t, n = re.subn(r'"max_tokens":\s*(?:32000|10000)', '"max_tokens": 4000', s)
if n == 0:
    print("kuch nahi mila, kuch nahi badla")
    raise SystemExit
open(p, "w", encoding="utf-8").write(t)
print(p, "->", n, "jagah badla")
