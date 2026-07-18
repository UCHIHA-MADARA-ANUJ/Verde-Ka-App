import requests
import re

base = 'https://verde-main-portfolio.vercel.app'
r_main = requests.get(base)
chunks = re.findall(r'/_next/static/chunks/[^\"]+\.js', r_main.text)

print(f"Found {len(chunks)} chunks.")

for chunk in chunks:
    url = base + chunk
    res = requests.get(url)
    if res.status_code != 200:
        continue
    js = res.text
    # find double quoted strings
    dq = re.findall(r'"([^"]{30,800})"', js)
    # find single quoted strings
    sq = re.findall(r"'([^']{30,800})'", js)
    combined = dq + sq
    
    clean = []
    for s in combined:
        if any(ch in s for ch in ['{', '}', ';', '=>', '<', '>', 'px', 'bg-', 'text-', 'border-', 'grid-', 'flex-', 'hover:', 'translate', 'duration', 'ease-', 'cubic-bezier', 'rgba']):
            continue
        # check if it looks like English text (spaces, normal letters)
        if len(re.findall(r'[a-zA-Z]', s)) > 20 and len(re.findall(r'\s', s)) > 3:
            s_clean = s.replace('\\xaa', ' ').replace('\\xa0', ' ').replace('\\n', ' ').replace('\\u00a0', ' ').replace('\\t', ' ')
            if s_clean not in clean:
                clean.append(s_clean)
                
    if clean:
        print(f"\n=================== CHUNK: {chunk} ===================")
        for idx, s in enumerate(clean):
            print(f"{idx}: {s}")
