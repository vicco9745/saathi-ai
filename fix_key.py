with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_code = "SAATHI_KEY = 'test-key-123';"

# Purane code ko dhundh kar replace karna
content = content.replace("if(!SAATHI_KEY){SAATHI_KEY=prompt('Saathi API Key डालें:');if(SAATHI_KEY)localStorage.setItem(SAATHI_KEY_STORE,SAATHI_KEY.trim());}", new_code)
content = content.replace("if(!SAATHI_KEY){SAATHI_KEY=prompt('Saathi API Key: ');if(SAATHI_KEY)localStorage.setItem(SAATHI_KEY_STORE,SAATHI_KEY.trim());}", new_code)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('SUCCESS! API Key fix ho gayi.')
