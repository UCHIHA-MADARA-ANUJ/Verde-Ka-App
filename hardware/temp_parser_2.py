import requests
import re

base = 'https://verde-main-portfolio.vercel.app'
js_url = base + '/_next/static/chunks/app/page-29f815003d9897e9.js'
js = requests.get(js_url).text

# Let's find matches that look like text (capitalized start, spaces, etc.)
pattern = r'"([^"]{15,500})"'
matches = re.findall(pattern, js)

print("Let's analyze matches:")
interesting = []
for m in matches:
    # Filter classes
    if any(c in m for c in ['{', '}', ';', '=>', 'import ', '<', '>', 'px', 'bg-', 'text-', 'border-', 'grid-', 'flex-', 'hover:']):
        continue
    # Let's clean the string
    m_clean = m.replace('\\xaa', ' ').replace('\\xa0', ' ').replace('\\n', ' ').replace('\\u00a0', ' ').replace('\\t', ' ')
    if m_clean not in interesting:
        interesting.append(m_clean)

for idx, item in enumerate(interesting):
    if len(item) > 25:
        print(f"{idx}: {item}")
