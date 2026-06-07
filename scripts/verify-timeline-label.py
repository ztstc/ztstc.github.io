"""Verify timeline label after rename."""
import json
from pathlib import Path

for p in ['lang/zh.json', 'lang/en.json']:
    d = json.loads(Path(p).read_text(encoding='utf-8'))
    link = d.get('timeline', {}).get('event1', {}).get('link', {})
    print(f"{p}: link = {link}")
