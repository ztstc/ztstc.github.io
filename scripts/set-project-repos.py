"""Update project 2 (2 repos) and project 4 (1 repo) with the specific GitHub URLs.

Plan:
  - project2.html: 2 github buttons (RTOS 固件, ROS 驱动)
  - project4.html: 1 github button (pointing to ESP32P4-ComputerDashboard)
  - Add new i18n keys for project2
"""
import re
import json
from pathlib import Path

# === Step 1: Add i18n keys to lang files ===
print("=== Step 1: Add i18n keys ===")
NEW_KEYS = {
    'project2.links.rtosFirmware': {'zh': 'RTOS 固件', 'en': 'RTOS Firmware'},
    'project2.links.rosDriver': {'zh': 'ROS 驱动', 'en': 'ROS Driver'},
}
for path, lang in [('lang/zh.json', 'zh'), ('lang/en.json', 'en')]:
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    proj2_links = d.setdefault('project2', {}).setdefault('links', {})
    changed = False
    for key, trans in NEW_KEYS.items():
        # key is like "project2.links.rtosFirmware" - get last segment
        short_key = key.split('.')[-1]
        if short_key not in proj2_links:
            proj2_links[short_key] = trans[lang]
            changed = True
    if changed:
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"  updated {path}")
    else:
        print(f"  {path}: already has keys")

# === Step 2: Update project2.html with 2 buttons ===
print("\n=== Step 2: Update project2.html (2 buttons) ===")
P2_TEMPLATE = '''<div class="publish-links">
            <a href="https://github.com/ztstc/RTOS_Nailong" target="_blank" rel="noopener noreferrer" class="publish-link github">
              <i class="fab fa-github"></i> <span data-i18n="project2.links.rtosFirmware">RTOS 固件</span>
            </a>
            <a href="https://github.com/ztstc/nailong_ws" target="_blank" rel="noopener noreferrer" class="publish-link github">
              <i class="fab fa-github"></i> <span data-i18n="project2.links.rosDriver">ROS 驱动</span>
            </a>
          </div>'''
P2 = Path('pages/projects/project2.html')
content = P2.read_text(encoding='utf-8')
m = re.search(r'(<div class="publish-links-wrapper">)(.*?)(</div>\s*\n\s*</div>\s*\n\s*</section>)', content, re.DOTALL)
if m:
    new_content = content[:m.start(2)] + P2_TEMPLATE + content[m.end(2):]
    P2.write_text(new_content, encoding='utf-8')
    print(f"  {P2.name}: 2 buttons added")
else:
    # Try a simpler pattern
    m = re.search(r'(<div class="publish-links">)(.*?)(</div>)', content, re.DOTALL)
    if m:
        # Build new content with the template (replacing the inner)
        new_inner = '\n'.join(P2_TEMPLATE.split('\n')[1:-1])  # remove wrapper divs
        new_content = content[:m.start(2)] + '\n' + new_inner + '\n        ' + content[m.end(2):]
        P2.write_text(new_content, encoding='utf-8')
        print(f"  {P2.name}: 2 buttons added (simple pattern)")
    else:
        print(f"  {P2.name}: ERROR - no publish-links block found")

# === Step 3: Update project4.html with 1 specific button ===
print("\n=== Step 3: Update project4.html (1 button) ===")
P4 = Path('pages/projects/project4.html')
content = P4.read_text(encoding='utf-8')
# Find the existing publish-links block
m = re.search(r'(<div class="publish-links">)(.*?)(</div>)', content, re.DOTALL)
if m:
    # Replace the inner with a single normalized button
    new_inner = '''
            <a href="https://github.com/ztstc/ESP32P4-ComputerDashboard" target="_blank" rel="noopener noreferrer" class="publish-link github">
              <i class="fab fa-github"></i> <span data-i18n="project4.links.github">Code</span>
            </a>
          '''
    new_content = content[:m.start(2)] + new_inner + content[m.end(2):]
    P4.write_text(new_content, encoding='utf-8')
    print(f"  {P4.name}: 1 button added (specific URL)")
else:
    print(f"  {P4.name}: ERROR - no publish-links block found")

# === Step 4: Verify ===
print("\n=== Step 4: Verify ===")
for n in [2, 4]:
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')
    block_match = re.search(r'<div class="publish-links">(.*?)</div>', content, re.DOTALL)
    if not block_match:
        print(f"  {p.name}: no block")
        continue
    links = re.findall(r'<a\b[^>]*>.*?</a>', block_match.group(1), re.DOTALL)
    print(f"  {p.name}: {len(links)} button(s)")
    for link in links:
        href = re.search(r'href="([^"]+)"', link)
        i18n = re.search(r'data-i18n="([^"]+)"', link)
        text = re.search(r'<span[^>]*>([^<]+)</span>', link)
        print(f"    href={href.group(1) if href else '?'}")
        print(f"    i18n={i18n.group(1) if i18n else '?'}")
        print(f"    text={text.group(1) if text else '?'}")
