"""Link user's project images to the 5 detail pages.

Mapping:
  Project 1 (RAS-IRU Wiki)        -> IRU-wiki-cover.jpg
  Project 2 (Nailoong Bot 奶龙)  -> 奶龙-封面.jpg, 奶龙底盘.jpg, 奶龙-侧视图.jpg, 奶龙-底盘雷达摄像头.jpg
  Project 3 (FOC_WL 无刷驱动)     -> FOC_驱动板-封面.jpg, FOC_第一代.jpg, FOC_背面.jpg
  Project 4 (电脑性能看板)        -> 电脑性能看板-封面.jpg, 电脑性能看板-控制中心.jpg, 电脑性能看板.jpg
  Project 5 (BerryAI 草莓)       -> BerryAI-封面.jpg, BerryAI水肥一体机主板.jpg, BerryAI水肥一体化主机照片.jpg, BerryAI-低帧率相机.jpg

Also updates main.js PROJECTS img field for each project's tile.
"""
import re
from pathlib import Path

PROJECT_IMAGES = {
    1: ['IRU-wiki-cover.jpg'],
    2: ['奶龙-封面.jpg', '奶龙底盘.jpg', '奶龙-侧视图.jpg', '奶龙-底盘雷达摄像头.jpg'],
    3: ['FOC_驱动板-封面.jpg', 'FOC_第一代.jpg', 'FOC_背面.jpg'],
    4: ['电脑性能看板-封面.jpg', '电脑性能看板-控制中心.jpg', '电脑性能看板.jpg'],
    5: ['BerryAI-封面.jpg', 'BerryAI水肥一体机主板.jpg', 'BerryAI水肥一体化主机照片.jpg', 'BerryAI-低帧率相机.jpg'],
}

PAGES_DIR = Path('pages/projects')

print("=== 1. Update detail HTML pages ===")
for n, images in PROJECT_IMAGES.items():
    html_path = PAGES_DIR / f'project{n}.html'
    content = html_path.read_text(encoding='utf-8')
    pattern = re.compile(r'(<img\s+src=")\.\./\.\./assets/images/[^"]+("[^>]*>)')
    counter = [0]

    def replace(m):
        if counter[0] < len(images):
            new_src = f'../../assets/images/{images[counter[0]]}'
            counter[0] += 1
            return m.group(1) + new_src + m.group(2)
        return m.group(0)

    new_content = pattern.sub(replace, content)
    html_path.write_text(new_content, encoding='utf-8')
    print(f"  {html_path.name}: {counter[0]}/{len(images)} images replaced")

print("\n=== 2. Verify ===")
for n, images in PROJECT_IMAGES.items():
    html_path = PAGES_DIR / f'project{n}.html'
    content = html_path.read_text(encoding='utf-8')
    found = re.findall(r'<img\s+src="\.\./\.\./assets/images/([^"]+)"', content)
    print(f"  project{n}.html: {found}")
