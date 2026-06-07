"""Verify the lang JSON files are valid and contain the new keys."""
import json
import sys
from pathlib import Path

ok = True
for p in ['lang/zh.json', 'lang/en.json']:
    try:
        d = json.loads(Path(p).read_text(encoding='utf-8'))
        has_tabs = 'tabs' in d
        has_notes = 'notes' in d
        print(f"{p}: VALID  tabs={has_tabs}  notes={has_notes}")
        if has_tabs:
            print(f"  tabs: {d['tabs']}")
        if has_notes:
            print(f"  notes keys: {list(d['notes'].keys())}")
    except Exception as e:
        print(f"{p}: INVALID -> {e}")
        ok = False

sys.exit(0 if ok else 1)
