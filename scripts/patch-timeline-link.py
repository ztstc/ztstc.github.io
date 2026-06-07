"""Add lab website link to timeline.event1 in both lang files."""
import json
from pathlib import Path

LINK = {
    'url': 'https://hdu-raslab.github.io/',
    'label': 'Home',
}

# English translation of event1
EN_EVENT1 = {
    'date': '2024.09',
    'title': 'Joined HDU RAS-IRU Robotics Lab',
    'desc': 'Started learning ROS and participating in the lab\'s robotics project development and maintenance work.',
    'link': LINK,
}

for path in ['lang/zh.json', 'lang/en.json']:
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    timeline = d.setdefault('timeline', {})
    event1 = timeline.setdefault('event1', {})

    if 'en' in path:
        # Overwrite with English version (the user has only one event, in Chinese)
        event1.clear()
        event1.update(EN_EVENT1)
    else:
        # Chinese: only add link, preserve user's title/desc
        event1['link'] = LINK

    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"updated {path}")

# Verify
print("\n=== After patch ===")
for p in ['lang/zh.json', 'lang/en.json']:
    d = json.loads(Path(p).read_text(encoding='utf-8'))
    e1 = d.get('timeline', {}).get('event1', {})
    print(f"\n{p}:")
    print(f"  date:  {e1.get('date')}")
    print(f"  title: {e1.get('title')}")
    print(f"  desc:  {e1.get('desc', '')[:60]}...")
    print(f"  link:  {e1.get('link')}")
