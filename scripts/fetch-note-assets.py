"""Backfill missing image assets for already-merged external notes.

The previous run of merge-external-notes.py only downloaded .md files, not
the images inside each source folder's assets/ subdirectory. This script
re-downloads the image files for the listed notes (idempotent: skip if
file already exists with non-zero size).

Usage:
  python scripts/fetch-note-assets.py
"""
import urllib.request
import json
import sys
from pathlib import Path
from urllib.parse import quote

API_BASE = 'https://api.github.com/repos/ztstc/note/contents'
RAW_BASE = 'https://raw.githubusercontent.com/ztstc/note/main'

# (local_note_path, remote_source_dir)
TARGETS = [
    ('notes/tools/git-copilot.md', 'Git_GitHub_Copilot笔记'),
    ('notes/tools/rosbridge.md',   'ROSBridge笔记'),
    ('notes/study/slam-notes.md',  'SLAM建图笔记'),
]

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp')

def fetch_api(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github+json'})
    return json.loads(urllib.request.urlopen(req, timeout=20).read().decode('utf-8'))

def fetch_bytes(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=30).read()

def fetch_assets_for(local_rel, source_dir):
    local_path = Path(local_rel)
    target = local_path.parent / 'assets'
    target.mkdir(parents=True, exist_ok=True)
    # 关键：源 dir 里的图片可能在 assets/ 子目录（git-copilot / rosbridge）
    # 也可能在顶层（slam-notes）。两层都扫。
    subdirs_to_scan = [source_dir]
    try:
        top_items = fetch_api(f'{API_BASE}/{quote(source_dir)}')
    except Exception as e:
        print(f"  [ERR] list {source_dir}: {e}")
        return 0, 0
    for it in top_items:
        if it.get('type') == 'dir' and it.get('name', '').lower() == 'assets':
            subdirs_to_scan.append(it['path'])
    new = skip = 0
    for sub in subdirs_to_scan:
        try:
            items = fetch_api(f'{API_BASE}/{quote(sub)}')
        except Exception as e:
            print(f"  [ERR] list {sub}: {e}")
            continue
        rel = sub[len(source_dir):].lstrip('/') if sub != source_dir else ''
        for item in items:
            if item.get('type') != 'file' or not item['name'].lower().endswith(IMG_EXTS):
                continue
            out = target / item['name']
            if out.exists() and out.stat().st_size > 0:
                skip += 1
                continue
            try:
                data = fetch_bytes(f'{RAW_BASE}/{quote(item["path"])}')
                out.write_bytes(data)
                new += 1
                tag = f" ({rel})" if rel else ''
                print(f"    + {item['name']}{tag} ({len(data)} bytes)")
            except Exception as e:
                print(f"    [ERR] {item['name']}: {e}")
    return new, skip

print("Backfilling image assets for existing notes...")
total_new = 0
for local_rel, source_dir in TARGETS:
    if not Path(local_rel).exists():
        print(f"  [SKIP] {local_rel} not found locally")
        continue
    print(f"\n[{local_rel}] <- {source_dir}/")
    new, skip = fetch_assets_for(local_rel, source_dir)
    total_new += new
    print(f"  summary: +{new} new, {skip} skipped")
print(f"\nDone. {total_new} images downloaded.")
