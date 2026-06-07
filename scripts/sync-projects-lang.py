"""Sync project1-5 with item1-5 in both lang files. Add project5 to zh (missing)."""
import json
from pathlib import Path

# English translations (best-effort from Chinese)
EN = {
    1: {
        'title': 'RAS-IRU Knowledge Base',
        'desc': 'A knowledge base built for robotics beginners, covering ROS/ROS2, SLAM navigation, and robotics software/hardware development. Continuously updated.',
    },
    2: {
        'title': 'Nailoong Bot "Milk Dragon Robot"',
        'desc': 'Two-wheel differential chassis robot project with full-stack development: mechanical design, chassis driver board, embedded software, ROS/ROS2 drivers, SLAM navigation, and emotional companion AI Agent.',
    },
    3: {
        'title': 'FOC_WL: ESP32S3-based 2804 Micro Brushless Motor Driver',
        'desc': 'FOC brushless motor project using ESP32S3+MP6540+MT6701. Supports Type-C PD power, temperature and current sensing. Hardware complete, driver tuning in progress.',
    },
    4: {
        'title': 'IoT PC Performance Dashboard (Waveshare ESP32P4 86 Box)',
        'desc': 'IoT project using ESP32P4 driving a 4-inch LCD touchscreen, connects to PC monitoring app via TCP. Real-time CPU/GPU/memory stats, touch interaction to switch time, weather, and more.',
    },
    5: {
        'title': 'BerryAI: Smart Strawberry Cultivation System',
        'desc': 'For strawberry cultivation: 3 generations of soil-environment sensors, 1 micro water-fertilizer integration device, and a low-frame-rate greenhouse camera. All hardware based on ESP32 series. Open-source includes hardware and backend server (excluding the AI Agent part).',
    },
}

GH = 'https://github.com/ztstc'  # 用户的 GitHub，后续可替换成具体 repo

for path, lang in [('lang/zh.json', 'zh'), ('lang/en.json', 'en')]:
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    projects_section = d.setdefault('projects', {})

    for n in range(1, 6):
        # 1) 同步 projects.itemN
        zh_item = json.loads(Path('lang/zh.json').read_text(encoding='utf-8'))['projects'][f'item{n}']
        if lang == 'zh':
            title, desc = zh_item['title'], zh_item['desc']
        else:
            title, desc = EN[n]['title'], EN[n]['desc']
        # Update or create item
        if f'item{n}' in projects_section:
            projects_section[f'item{n}']['title'] = title
            projects_section[f'item{n}']['desc'] = desc
        else:
            projects_section[f'item{n}'] = {'title': title, 'desc': desc, 'tags': zh_item.get('tags', [])}

        # 2) 同步 projectN
        existing = d.get(f'project{n}')
        if existing is None:
            # Create new (e.g., project5 in zh)
            d[f'project{n}'] = {
                'title': title,
                'desc': desc,
                'links': {'github': GH},
            }
            print(f"  + created project{n} in {path}")
        else:
            existing['title'] = title
            existing['desc'] = desc
            if 'links' not in existing:
                existing['links'] = {'github': GH}
            elif 'github' not in existing['links']:
                existing['links']['github'] = GH

    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"updated {path}")

# 验证
print("\n=== After sync ===")
for p in ['lang/zh.json', 'lang/en.json']:
    d = json.loads(Path(p).read_text(encoding='utf-8'))
    print(f"\n{p}:")
    for n in range(1, 6):
        item = d.get('projects', {}).get(f'item{n}', {})
        proj = d.get(f'project{n}', {})
        gh = proj.get('links', {}).get('github', '-')
        print(f"  item{n}:   {item.get('title', '?')[:40]}")
        print(f"  project{n}: {proj.get('title', '?')[:40]}  → {gh}")
