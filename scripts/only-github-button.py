"""Simplify each project page: keep only the github button, point to user's main repo.

For each pages/projects/projectN.html:
  1. Find the <div class="publish-links"> block
  2. Extract all <a> tags
  3. Keep only the one with 'github' in its class
  4. Update its href to https://github.com/ztstc
"""
import re
from pathlib import Path

GH = 'https://github.com/ztstc'

print("=== Keep only github button in each project page ===")
for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')

    # Find the publish-links block (with flexible whitespace)
    block_pattern = re.compile(
        r'(<div class="publish-links">)(.*?)(</div>)',
        re.DOTALL
    )
    m = block_pattern.search(content)
    if not m:
        print(f"  {p.name}: no publish-links block, skip")
        continue

    # Find all <a>...</a> tags in the block
    a_pattern = re.compile(r'<a\b[^>]*>.*?</a>', re.DOTALL)
    links = a_pattern.findall(m.group(2))
    if not links:
        print(f"  {p.name}: no <a> tags, skip")
        continue

    # Find the github link (class contains 'github')
    github_link = None
    for link in links:
        class_match = re.search(r'class="([^"]+)"', link)
        if class_match and 'github' in class_match.group(1).split():
            github_link = link
            break

    if not github_link:
        print(f"  {p.name}: no github link found in {len(links)} links")
        continue

    # Update its href
    github_link_new = re.sub(r'href="[^"]+"', f'href="{GH}"', github_link, count=1)

    # Build new block content
    new_block = (
        m.group(1)
        + '\n            ' + github_link_new + '\n          '
        + m.group(3)
    )

    # Replace
    new_content = content.replace(m.group(0), new_block)
    p.write_text(new_content, encoding='utf-8')

    removed = len(links) - 1
    print(f"  {p.name}: kept github ({GH}), removed {removed} other link(s)")

# Verify
print("\n=== Verify ===")
for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')
    block_match = re.search(r'<div class="publish-links">(.*?)</div>', content, re.DOTALL)
    if not block_match:
        print(f"  {p.name}: no block")
        continue
    links = re.findall(r'<a\b[^>]*>.*?</a>', block_match.group(1), re.DOTALL)
    link_info = []
    for link in links:
        href = re.search(r'href="([^"]+)"', link)
        text = re.search(r'<span[^>]*>([^<]+)</span>', link)
        link_info.append({
            'href': href.group(1) if href else '?',
            'text': text.group(1).strip() if text else '?',
        })
    print(f"  {p.name}: {link_info}")
