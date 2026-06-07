"""Three things in one shot:
1. Replace 'ztstc' branding in title/nav of all 5 detail pages
2. Add remaining images, wrap extras (>2) in <details class="project-extras"> collapsible
3. Add new i18n keys (imgAlt5-10, moreImages) to both lang files
"""
import re
import json
from pathlib import Path

# === STEP 1: ztstc branding in title and nav ===
print("=== STEP 1: Title and nav 'ztstc' branding ===")
for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')
    new_content = content.replace('Lain-Ego', 'ztstc')
    if new_content != content:
        p.write_text(new_content, encoding='utf-8')
        print(f"  {p.name}: replaced")

# === STEP 2: Restructure project2/5 with collapsible ===
print("\n=== STEP 2: Add collapsible to project2 (8 imgs) and project5 (4 imgs) ===")

# Define image order: 2 main + rest in extras
PROJECT_LAYOUT = {
    2: {
        'main': [
            ('奶龙-封面.jpg', 1),
            ('奶龙底盘.jpg', 2),
        ],
        'extras': [
            ('奶龙-侧视图.jpg', 3),  # use existing imgAlt3
            ('奶龙-底盘控制器.png', 5),
            ('奶龙-底盘雷达摄像头.jpg', 6),
            ('奶龙-眼部特写.jpg', 7),
            ('奶龙-尾部.jpg', 8),
            ('奶龙底盘导航照片.jpg', 9),
        ],
    },
    5: {
        'main': [
            ('BerryAI-封面.jpg', 1),
            ('BerryAI水肥一体机主板.jpg', 2),
        ],
        'extras': [
            ('BerryAI水肥一体化主机照片.jpg', 5),
            ('BerryAI-低帧率相机.jpg', 6),
        ],
    },
}

def build_img_tag(filename, alt_n):
    return f'<img src="../../assets/images/{filename}" data-i18n="projects1.imgAlt{alt_n}" class="project-img">'

def build_details(extras):
    imgs_html = '\n        '.join(build_img_tag(fn, n) for fn, n in extras)
    return f'''\n<details class="project-extras">
  <summary><span data-i18n="projects.moreImages">查看更多图片</span> ({len(extras)})</summary>
  <div class="project-extras-grid">
        {imgs_html}
  </div>
</details>
'''

for n, layout in PROJECT_LAYOUT.items():
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')
    img_pattern = re.compile(
        r'<img\s+src="\.\./\.\./assets/images/[^"]+"\s+data-i18n="projects1\.imgAlt\d+"\s+class="project-img">\s*\n?'
    )
    matches = list(img_pattern.finditer(content))
    if not matches:
        print(f"  {p.name}: no imgs found, skip")
        continue
    # Build new block: 2 main imgs (in fixed order) + details
    main_html = '\n'.join(build_img_tag(fn, n_) for fn, n_ in layout['main'])
    details_html = build_details(layout['extras'])
    new_block = main_html + details_html
    # Replace from first img to last img
    start = matches[0].start()
    end = matches[-1].end()
    new_content = content[:start] + new_block + content[end:]
    p.write_text(new_content, encoding='utf-8')
    print(f"  {p.name}: {len(layout['main'])} main + {len(layout['extras'])} in collapsible")

# === STEP 3: Add i18n keys ===
print("\n=== STEP 3: Add new i18n keys ===")

ALT_KEYS = {
    'imgAlt5': {'zh': '补充展示图 1', 'en': 'Additional Image 1'},
    'imgAlt6': {'zh': '补充展示图 2', 'en': 'Additional Image 2'},
    'imgAlt7': {'zh': '补充展示图 3', 'en': 'Additional Image 3'},
    'imgAlt8': {'zh': '补充展示图 4', 'en': 'Additional Image 4'},
    'imgAlt9': {'zh': '补充展示图 5', 'en': 'Additional Image 5'},
    'imgAlt10': {'zh': '补充展示图 6', 'en': 'Additional Image 6'},
    'moreImages': {'zh': '查看更多图片', 'en': 'Show more images'},
}

for path in ['lang/zh.json', 'lang/en.json']:
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    lang = 'zh' if 'zh' in path else 'en'
    projects1 = d.setdefault('projects1', {})

    for key, trans in ALT_KEYS.items():
        if key == 'moreImages':
            if 'projects' in d and key not in d['projects']:
                d['projects'][key] = trans[lang]
        else:
            if key not in projects1:
                projects1[key] = trans[lang]

    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"  updated {path}")

# === Verify ===
print("\n=== Verify ===")
for n in range(1, 6):
    p = Path(f'pages/projects/project{n}.html')
    content = p.read_text(encoding='utf-8')
    has_old = 'Lain-Ego' in content
    has_extras = 'project-extras' in content
    has_ztstc = 'ztstc' in content
    img_count = len(re.findall(r'<img\s+src="\.\./\.\./assets/images/', content))
    extra_count = len(re.findall(r'class="project-extras-grid"', content))
    print(f"  {p.name}: Lain-Ego={has_old} ztstc={has_ztstc} imgs={img_count} extras-grid={extra_count}")
