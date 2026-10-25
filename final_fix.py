import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. X-API-Key ko x-api-key mein badalna
content = content.replace("'X-API-Key'", "'x-api-key'")
content = content.replace('"X-API-Key"', '"x-api-key"')

# 2. SAATHI_KEY ko hamesha test-key-123 par set karna (prompt ko hatana)
# Hum 'const SAATHI_KEY' wali line ko dhundh kar replace karenge
content = re.sub(r"const SAATHI_KEY\s*=\s*localStorage\.getItem\('saathi_api_key'\)\s*\|\|\s*\(prompt\('Saathi API Key.*?'\)\s*\|\|\s*''\);", "const SAATHI_KEY = 'test-key-123';", content)
content = re.sub(r"const SAATHI_KEY\s*=\s*localStorage\.getItem\('saathi_api_key'\)\s*\|\|\s*prompt\('Saathi API Key.*?'\);", "const SAATHI_KEY = 'test-key-123';", content)
content = re.sub(r"const SAATHI_KEY\s*=\s*prompt\('Saathi API Key.*?'\);", "const SAATHI_KEY = 'test-key-123';", content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('SUCCESS! Header aur Key dono fix ho gaye.')
