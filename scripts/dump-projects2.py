"""Read & show project1-5 from both lang files."""
import json
from pathlib import Path

for p in ['lang/zh.json', 'lang/en.json']:
    d = json.loads(Path(p).read_text(encoding='utf-8'))
    print(f"\n========= {p} =========")
    for n in range(1, 6):
        proj = d.get(f'project{n}')
        if proj:
            print(f"\nproject{n}:")
            print(f"  title: {proj.get('title', '?')}")
            print(f"  desc: {proj.get('desc', '?')[:80]}...")
            links = proj.get('links', {})
            if links:
                print(f"  links: {list(links.keys())}")
                for k, v in links.items():
                    print(f"    {k}: {v}")
        else:
            print(f"\nproject{n}: MISSING")
