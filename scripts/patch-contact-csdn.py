"""Add contact.csdn key to both lang files."""
import json
from pathlib import Path

PATCHES = {
    'lang/zh.json': 'CSDN 博客',
    'lang/en.json': 'CSDN Blog',
}

for path, label in PATCHES.items():
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    contact = d.setdefault('contact', {})
    if 'csdn' in contact:
        print(f"{path}: contact.csdn already exists, skipping")
        continue
    contact['csdn'] = label
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{path}: added contact.csdn = {label!r}")
