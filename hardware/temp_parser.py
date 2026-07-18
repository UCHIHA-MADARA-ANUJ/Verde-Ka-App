import requests
import re

base = 'https://verde-main-portfolio.vercel.app'
js_url = base + '/_next/static/chunks/app/page-29f815003d9897e9.js'
js = requests.get(js_url).text

# Let's find matches
strings = re.findall(r'"([^"]{15,1000})"', js)
strings2 = re.findall(r"'([^']{15,1000})'", js)
all_strings = strings + strings2

clean_strings = []
for s in all_strings:
    # Filter out code, styles, classes
    if any(ch in s for ch in ['{', '}', ';', '=>', 'import ', '<', '>', 'px', 'bg-', 'text-', 'border-', 'grid-', 'flex-']):
        continue
    # Decode unicode/hex escapes manually or just clean them
    s_clean = s.replace('\\xaa', ' ').replace('\\xa0', ' ').replace('\\n', ' ')
    if s_clean not in clean_strings:
        clean_strings.append(s_clean)

print(f"Total clean strings found: {len(clean_strings)}")
for idx, s in enumerate(clean_strings):
    print(f"{idx}: {s}")
