import re
p="app/main.py"
s=open(p).read()
old="    return \"chat\"\n\n\n@app.post(\"/v1/chat\")"
new="""    # ═══ Kahani / Story / Poem ═══\n    if any(x in m for x in [\"kahani\",\"कहानी\",\"story\",\"किस्सा\",\"कविता\",\"poem\",\"शायरी\",\"baal\",\"baat\",\"बात\",\"joke\",\"चुटकुला\"]):\n        return \"chat\"\n    return \"chat\"\n\n\n@app.post(\"/v1/chat\")"""
if old in s:
    s=s.replace(old,new,1)
    open(p,"w").write(s)
    print("OK - Chat/Story detect add ho gaya")
else:
    print("FAIL - purana pattern nahi mila")
