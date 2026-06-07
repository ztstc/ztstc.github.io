"""Dump project1-4 and items 3-5 from both lang files to see current state."""
import json
from pathlib import Path

for p in ['lang/zh.json', 'lang/en.json']:
    d = json.loads(Path(p).read_text(encoding='utf-8'))
    print(f"\n=== {p} ===")
    for n in range(1, 6):
        item = d.get('projects', {}).get(f'item{n}')
        proj = d.get(f'project{n}')
        print(f"  item{n}:", 'YES' if item else 'NO', f"({item.get('title','') if item else '-'})")
        print(f"  project{n}:", 'YES' if proj else 'NO', f"({proj.get('title','') if proj else '-'})")
    print(f"  projects1:", 'YES' if d.get('projects1') else 'NO')
