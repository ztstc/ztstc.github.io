"""Merge external ztstc/note repo into local notes/ directory.

Layout:
  notes/
  ├── README.md                       (existing)
  ├── getting-started.md              (existing)
  ├── study/                          (existing)
  │   ├── dynamic-programming.md
  │   └── git-cheatsheet.md
  ├── projects/                       (existing)
  │   └── opendog-notes.md
  ├── tools/                          (NEW)
  │   ├── git-copilot.md              (renamed from 'Git & GitHub & Copilot 使用指南.md')
  │   └── rosbridge.md                (renamed from 'ROSBridge使用指南.md')
  └── ros-tutorials/                  (NEW, split by chapter)
      ├── 0/                         (intro)
      │   ├── 0.0.0Introduction.md
      │   └── ...
      ├── 1/                         (basics)
      │   ├── 1.0-...
      │   └── ...
      └── 10/                        (advanced)
          ├── 10.0-...
          └── ...
"""
import urllib.request
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

API_BASE = 'https://api.github.com/repos/ztstc/note/contents'
RAW_BASE = 'https://raw.githubusercontent.com/ztstc/note/main'

def fetch_api(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github+json'})
    return json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))

def fetch_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=15).read().decode('utf-8')

def fetch_bytes(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=30).read()

# 本地笔记对应的远端源目录（用于拉 assets/ 资源）
# 缺这个映射时该笔记对应的资源不会下载（之前只下了 .md，图片全 404）
REVERSE_SOURCE_DIR = {
    'notes/tools/git-copilot.md': 'Git_GitHub_Copilot笔记',
    'notes/tools/rosbridge.md': 'ROSBridge笔记',
    'notes/study/slam-notes.md': 'SLAM建图笔记',
    # ros-tutorials 的源 dir 名带下划线（ROSTutorials_Markdown），
    # 但 ROS 教程资源较散，这里不做强制拉取，需要时手工同步
}

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp')

def fetch_assets_for_note(local_rel):
    """把远端 source_dir/assets/ 下的图片下载到本地 notes/<dir>/assets/。
    已有同名文件跳过，幂等。"""
    src = REVERSE_SOURCE_DIR.get(local_rel)
    if not src:
        return 0
    # 本地 assets 目录：notes/<dir>/assets/
    local_path = Path(local_rel)
    local_dir = local_path.parent
    target = local_dir / 'assets'
    target.mkdir(parents=True, exist_ok=True)
    # 列远端 source_dir 下的所有 file
    try:
        items = fetch_api(f'{API_BASE}/{quote(src)}')
    except Exception as e:
        print(f"  [assets] ERR list {src}: {e}")
        return 0
    new = 0
    for item in items:
        if item.get('type') != 'file':
            continue
        name = item['name']
        if not name.lower().endswith(IMG_EXTS):
            continue
        out = target / name
        if out.exists() and out.stat().st_size > 0:
            continue
        try:
            data = fetch_bytes(f'{RAW_BASE}/{quote(item["path"])}')
            out.write_bytes(data)
            new += 1
        except Exception as e:
            print(f"  [assets] ERR {name}: {e}")
    if new:
        print(f"  [assets] {src}/ -> {target}/ (+{new} new)")
    return new

def list_all_files(path=''):
    url = f'{API_BASE}/{quote(path)}' if path else API_BASE
    items = fetch_api(url)
    files = []
    for item in items:
        if item['type'] == 'dir':
            files.extend(list_all_files(item['path'].lstrip('/')))
        elif item['type'] == 'file' and item['name'].endswith('.md'):
            files.append(item)
    return files

def map_to_local(ext_path):
    parts = ext_path.split('/')
    if len(parts) < 2:
        return None
    top_dir = parts[0]
    filename = parts[-1]

    # Git_GitHub_Copilot笔记 → tools/git-copilot.md
    if top_dir.startswith('Git_'):
        return 'notes/tools/git-copilot.md'
    # ROSBridge笔记 → tools/rosbridge.md
    if top_dir.startswith('ROSBridge'):
        return 'notes/tools/rosbridge.md'
    # ROSTutorials_Markdown → ros-tutorials/{chapter}/{filename}
    if top_dir.startswith('ROSTutorials_Markdown'):
        stem = filename.rsplit('.', 1)[0]
        for sep in ['.', '-']:
            if sep in stem:
                chapter = stem.split(sep)[0]
                break
        else:
            chapter = 'misc'
        return f'notes/ros-tutorials/{chapter}/{filename}'
    # SLAM建图笔记 → study/slam-notes.md（学习笔记分组）
    if top_dir.startswith('SLAM'):
        return 'notes/study/slam-notes.md'
    # 根目录单文件：bug解决、指令备忘 → tools/
    if ext_path == 'bug解决.md':
        return 'notes/tools/bug-fixes.md'
    if ext_path == '指令备忘.md':
        return 'notes/tools/command-cheatsheet.md'
    return None


def concat_root_files(ext_paths, target_path, header):
    """多个仓库根目录的 .md 合并到目标文件（用分割线连接）。"""
    if not ext_paths:
        return False
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    chunks = [f'# {header}\n']
    for p in ext_paths:
        try:
            raw_url = f'{RAW_BASE}/{quote(p)}'
            body = fetch_text(raw_url)
            chunks.append(f'\n---\n\n<!-- source: {p} -->\n\n{body.strip()}\n')
        except Exception as e:
            print(f"  ERROR fetching {p}: {e}")
    target.write_text('\n'.join(chunks), encoding='utf-8')
    return True

print("Fetching file list from ztstc/note...")
all_files = list_all_files()
print(f"Found {len(all_files)} .md files\n")

# 把命中同一目标文件的源文件分组（SLAM/bug解决/指令备忘 等多 .md 合并场景）
grouped = {}
single_files = []
for file in all_files:
    ext_path = file['path']
    local_rel = map_to_local(ext_path)
    if not local_rel:
        print(f"  SKIP: {ext_path}")
        continue
    grouped.setdefault(local_rel, []).append(ext_path)

success, skipped, failed = 0, 0, 0
for local_rel, ext_paths in grouped.items():
    local_path = Path(local_rel)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if len(ext_paths) == 1:
            # 单文件直接拷贝
            raw_url = f'{RAW_BASE}/{quote(ext_paths[0])}'
            content = fetch_text(raw_url)
            local_path.write_text(content, encoding='utf-8')
        else:
            # 多文件合并：用分割线 + 来源注释串起来
            header = local_path.stem
            if concat_root_files(ext_paths, local_rel, header.replace('-', ' ').title()):
                skipped += len(ext_paths) - 1
        success += 1
        # 拉对应的 assets/ 图片（之前漏了，导致所有 .md 里图片 404）
        fetch_assets_for_note(local_rel)
    except Exception as e:
        print(f"  ERROR: {ext_paths} -> {e}")
        failed += 1

print(f"\nDone: {success} groups saved, {skipped} merged, {failed} failed")
print(f"\nNew local files (sample):")
for f in sorted(Path('notes').rglob('*.md')):
    if 'README' not in f.name and 'getting-started' not in f.name and 'dynamic-programming' not in f.name and 'git-cheatsheet' not in f.name and 'opendog' not in f.name:
        print(f"  {f}")
