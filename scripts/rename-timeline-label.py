"""Rename timeline.event1.link.label from 'Home' to 'RAS' in both lang files."""
import json
from pathlib import Path

for p in ['lang/zh.json', 'lang/en.json']:
    path = Path(p)
    d = json.loads(path.read_text(encoding='utf-8'))
    link = d.get('timeline', {}).get('event1', {}).get('link')
    if not link:
        print(f"{p}: no link found, skipping")
        continue
    old = link.get('label')
    link['label'] = 'RAS'
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{p}: '{old}' -> 'RAS'")
