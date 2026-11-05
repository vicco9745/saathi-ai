p = "app/main.py"
s = open(p, encoding="utf-8").read()
old = '"(b) an IMAGE / picture / photo / drawing / illustration, or (c) a PDF / document / report / letter file. "\n'
new = ('"(b) an IMAGE / picture / photo / drawing / illustration, or (c) a PDF file. "\n'
       '    "Choose pdf ONLY if the user explicitly asks for a PDF, a downloadable file or a document file. "\n'
       '    "Writing an email, letter, message, essay, report text or any answer to read in the chat is NONE, "\n'
       '    "even if the user says make, create, banao or bana do. "\n')
if s.count(old) != 1:
    print("match nahi mila, kuch nahi badla")
    raise SystemExit
open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("main.py badal gaya")
