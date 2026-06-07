"""Add 'ai' key to skills section in both lang files (safe, preserves encoding)."""
import json
from pathlib import Path

PATCHES = {
    'lang/zh.json': 'AI 与智能体',
    'lang/en.json': 'AI & Agents',
}

for path, ai_label in PATCHES.items():
    p = Path(path)
    d = json.loads(p.read_text(encoding='utf-8'))
    if 'ai' in d.get('skills', {}):
        print(f"{path}: skills.ai already exists, skipping")
        continue
    d['skills']['ai'] = ai_label
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{path}: added skills.ai = {ai_label!r}")
