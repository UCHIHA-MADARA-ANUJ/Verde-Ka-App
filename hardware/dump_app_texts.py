import requests
import re

base = 'https://verde-tech-proj.vercel.app'
js_url = base + '/_next/static/chunks/app/page-4e6a83bf47e9d77f.js'
js = requests.get(js_url).text

# Let's extract strings
dq = re.findall(r'"([^"]{25,500})"', js)
sq = re.findall(r"'([^']{25,500})'", js)
combined = dq + sq

clean = []
for s in combined:
    if any(ch in s for ch in ['{', '}', ';', '=>', '<', '>', 'px', 'bg-', 'text-', 'border-', 'grid-', 'flex-', 'hover:', 'translate', 'duration', 'ease-', 'cubic-bezier', 'rgba']):
        continue
    if len(re.findall(r'[a-zA-Z]', s)) > 15 and len(re.findall(r'\s', s)) > 2:
        s_clean = s.replace('\\xaa', ' ').replace('\\xa0', ' ').replace('\\n', ' ').replace('\\u00a0', ' ').replace('\\t', ' ')
        if s_clean not in clean:
            clean.append(s_clean)

print(f"Total clean strings from app: {len(clean)}")
for idx, s in enumerate(clean):
    print(f"{idx}: {s}")
