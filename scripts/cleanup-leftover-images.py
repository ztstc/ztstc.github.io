"""Final cleanup: remove leftover old images from project3/4, then update main.js PROJECTS covers."""
import re
import json
from pathlib import Path

# 1. Remove leftover old img tags (outdated images that are now wrong)
TO_REMOVE = {
    'pages/projects/project3.html': 'robocon-detail-3.png',
    'pages/projects/project4.html': 'lobster-detail-3.png',
}
print("=== 1. Remove leftover old images ===")
for path, filename in TO_REMOVE.items():
    p = Path(path)
    content = p.read_text(encoding='utf-8')
    pattern = re.compile(
        r'\s*<img\s+src="\.\./\.\./assets/images/' + re.escape(filename) + r'"[^>]*>\s*\n?'
    )
    new_content = pattern.sub('', content)
    if new_content != content:
        p.write_text(new_content, encoding='utf-8')
        print(f"  removed {filename} from {p.name}")
    else:
        print(f"  WARN: no match in {p.name}")

# 2. Update main.js PROJECTS array (cover images)
print("\n=== 2. main.js PROJECTS cover images ===")
COVER_IMAGES = {
    1: "assets/images/IRU-wiki-cover.jpg",
    2: "assets/images/奶龙-封面.jpg",
    3: "assets/images/FOC_驱动板-封面.jpg",
    4: "assets/images/电脑性能看板-封面.jpg",
    5: "assets/images/BerryAI-封面.jpg",
}
main_js = Path('assets/js/main.js')
content = main_js.read_text(encoding='utf-8')

# Find each PROJECTS entry and update its img field
# Pattern: matches `img: 'assets/images/X',` for each project
# We'll find them by counting their position in the array
lines = content.split('\n')
new_lines = []
i = 0
project_idx = 0
while i < len(lines):
    line = lines[i]
    if 'img:' in line and "assets/images" in line and project_idx < 5:
        # This is a project cover line, replace it
        # Match leading whitespace
        m = re.match(r'^(\s*)img:\s*[\'"][^\'"]*[\'"]', line)
        if m:
            indent = m.group(1)
            new_line = f"{indent}img: '{COVER_IMAGES[project_idx + 1]}',"
            new_lines.append(new_line)
            project_idx += 1
            i += 1
            continue
    new_lines.append(line)
    i += 1

if project_idx == 5:
    main_js.write_text('\n'.join(new_lines), encoding='utf-8')
    print(f"  updated {project_idx} project covers in main.js")
else:
    print(f"  WARN: only matched {project_idx} project covers, expected 5")

# 3. Verify
print("\n=== 3. Verify ===")
for n, expected in COVER_IMAGES.items():
    # Check the corresponding detail page has correct cover
    detail = Path(f'pages/projects/project{n}.html').read_text(encoding='utf-8')
    imgs = re.findall(r'<img\s+src="\.\./\.\./assets/images/([^"]+)"', detail)
    has_old = any('agri' in i or 'lobster' in i or 'opendog' in i or 'robocon' in i or 'locowiki' in i for i in imgs)
    print(f"  project{n}.html: imgs={imgs[:3]}{'...' if len(imgs)>3 else ''}  old_leftover={has_old}")

# Also check main.js PROJECTS
content = main_js.read_text(encoding='utf-8')
imgs = re.findall(r"img:\s*'(assets/images/[^']+)'", content)
print(f"  main.js PROJECTS: {imgs}")
