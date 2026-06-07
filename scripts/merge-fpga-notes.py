"""Merge local FPGA_Note/ into the wiki notes section.

Source: FPGA_Note/FPGA学习笔记.md + assets/ (80 images)
Target: notes/study/fpga.md + notes/study/assets/

The .md references images via 'assets/image-XXX.png' (relative), so moving
the assets folder alongside the .md keeps paths working.
"""
import shutil
import json
from pathlib import Path

SRC = Path('FPGA_Note')
TGT = Path('notes/study')
TGT.mkdir(parents=True, exist_ok=True)

# 1. Copy the .md (rename to ASCII for safety)
src_md = SRC / 'FPGA学习笔记.md'
tgt_md = TGT / 'fpga.md'
shutil.copy2(src_md, tgt_md)
print(f"[1] {src_md}  ->  {tgt_md}  ({tgt_md.stat().st_size} bytes)")

# 2. Copy the assets folder
src_assets = SRC / 'assets'
tgt_assets = TGT / 'assets'
if tgt_assets.exists():
    shutil.rmtree(tgt_assets)
shutil.copytree(src_assets, tgt_assets)
img_count = sum(1 for _ in tgt_assets.iterdir())
print(f"[2] {src_assets}/  ->  {tgt_assets}/  ({img_count} files)")

# 3. Update notes-index.json (add fpga to study group)
idx_path = Path('assets/data/notes-index.json')
idx = json.loads(idx_path.read_text(encoding='utf-8'))
study_group = None
for g in idx['groups']:
    # Match by titleEn (English) or title (Chinese) or by path-based heuristic
    if (g.get('titleEn','').lower() in ('study', 'study notes', '学习笔记')
        or g.get('title','').lower() in ('study', '学习笔记')):
        study_group = g
        break
if study_group is None:
    print("[3] ERROR: study group not found in notes-index.json")
else:
    # Avoid duplicate
    if not any(it.get('path') == 'study/fpga.md' for it in study_group['items']):
        study_group['items'].append({
            'path': 'study/fpga.md',
            'title': 'FPGA 学习笔记 (Vivado 2025.2)',
            'titleEn': 'FPGA Study Notes (Vivado 2025.2)',
        })
        idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"[3] notes-index.json: appended fpga to Study Notes ({len(study_group['items'])} items now)")
    else:
        print("[3] notes-index.json: fpga already in Study Notes, skip")

# 4. Sanity check: do all referenced images exist?
print("\n[4] Image reference check:")
import re
md_content = tgt_md.read_text(encoding='utf-8')
# 严格匹配 markdown 图片 ![alt](path) 和 html <img src="path">，
# 避免之前的宽松正则把空字符串、URL 尾括号、纯文本误判为图片路径。
md_img_refs = re.findall(r'!\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)', md_content)
html_img_refs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', md_content)
all_refs = md_img_refs + html_img_refs
local_refs = [
    r for r in all_refs
    if not r.startswith(('http://', 'https://', 'data:', '//', '/'))
]
missing = [r for r in local_refs if not (tgt_md.parent / r).exists()]
if missing:
    print(f"  MISSING {len(missing)}/{len(local_refs)} local image refs:")
    for m in missing[:5]:
        print(f"    - {m}")
else:
    print(f"  OK: all {len(local_refs)} local image refs resolve")
