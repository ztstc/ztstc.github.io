"""Normalize the github button across all 5 project pages.

For each page:
  1. Replace the kept <a> tag with a clean template using data-i18n
  2. Add 'links.github' to project4 in both lang files (was missing)
"""
import re
import json
from pathlib import Path

GH = 'https://github.com/ztstc'

# === Step 1: Ensure project4 has links.github key ===
print("=== Step 1: Ensure project4.links.github in both lang files ===")
for path in ['lang/zh.json', 'lang/en.json']:
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    lang = 'zh' if 'zh' in path else 'en'
    project4_links = d.setdefault('project4', {}).setdefault('links', {})
    if 'github' not in project4_links:
        project4_links['github'] = '开源代码' if lang == 'zh' else 'Code'
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"  added links.github to project4 in {path}")
    else:
        print(f"  {path}: already has links.github")

# === Step 2: Normalize the kept github link in each project page ===
print("\n=== Step 2: Normalize github button ===")
TEMPLATE = '''<a href="{gh}" target="_blank" rel="noopener noreferrer" class="publish-link github">
              <i class="fab fa-github"></i> <span data-i18n="project{n}.links.github">Code</span>
            </a>'''

for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')

    block_pattern = re.compile(r'(<div class="publish-links">)(.*?)(</div>)', re.DOTALL)
    m = block_pattern.search(content)
    if not m:
        print(f"  {p.name}: no publish-links block")
        continue

    a_pattern = re.compile(r'<a\b[^>]*>.*?</a>', re.DOTALL)
    links = a_pattern.findall(m.group(2))
    if not links:
        print(f"  {p.name}: no <a> in block")
        continue

    # Build clean replacement
    new_link = TEMPLATE.format(gh=GH, n=n)
    # Replace just the first <a>
    new_inner = m.group(2).replace(links[0], new_link, 1)
    new_content = content[:m.start(2)] + new_inner + content[m.end(2):]
    p.write_text(new_content, encoding='utf-8')
    print(f"  {p.name}: replaced link")

# === Step 3: Verify ===
print("\n=== Step 3: Verify ===")
for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')
    block_match = re.search(r'<div class="publish-links">(.*?)</div>', content, re.DOTALL)
    if not block_match:
        print(f"  {p.name}: no block")
        continue
    links = re.findall(r'<a\b[^>]*>.*?</a>', block_match.group(1), re.DOTALL)
    print(f"  {p.name}: {len(links)} link(s)")
    for link in links:
        href = re.search(r'href="([^"]+)"', link)
        i18n = re.search(r'data-i18n="([^"]+)"', link)
        text = re.search(r'<span[^>]*>([^<]+)</span>', link)
        print(f"    href={href.group(1) if href else '?'}")
        print(f"    i18n={i18n.group(1) if i18n else '?'}")
        print(f"    fallback text={text.group(1) if text else '?'}")
