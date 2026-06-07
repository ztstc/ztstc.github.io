"""Dump notes-index.json groups."""
import json
from pathlib import Path
d = json.loads(Path('assets/data/notes-index.json').read_text(encoding='utf-8'))
for g in d.get('groups', []):
    print(f"  title='{g.get('title')}'  titleEn='{g.get('titleEn')}'  items={len(g.get('items',[]))}")
