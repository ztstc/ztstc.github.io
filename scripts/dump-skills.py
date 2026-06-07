"""Dump the skills section of both lang files for inspection."""
import json
from pathlib import Path

for p in ['lang/zh.json', 'lang/en.json']:
    d = json.loads(Path(p).read_text(encoding='utf-8'))
    s = d.get('skills', {})
    print(f"=== {p} ===")
    print(f"keys: {list(s.keys())}")
    for k, v in s.items():
        print(f"  {k}: {v!r}")
    print()
