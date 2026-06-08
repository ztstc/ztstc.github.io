"""One-off helper: 给 notes-index.json 里的关键笔记批量打 tags。

执行：python scripts/tag-notes.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / 'assets' / 'data' / 'notes-index.json'

# 演示用 tags。新 schema：每条 item 可选 tags / category / date / excerpt
TAG_MAP = {
    'study/demo-features.md':           ['demo', 'katex', 'highlight', 'test'],
    'study/dynamic-programming.md':      ['algorithm', 'dp'],
    'study/fpga.md':                     ['fpga', 'vivado', 'verilog', 'embedded'],
    'study/git-cheatsheet.md':           ['git', 'cheatsheet'],
    'study/slam-notes.md':               ['slam', 'ros', 'navigation', 'mapping'],
    'tools/bug-fixes.md':                ['troubleshooting', 'tips'],
    'tools/command-cheatsheet.md':       ['linux', 'shell', 'cheatsheet'],
    'tools/git-copilot.md':              ['git', 'copilot', 'ai'],
    'tools/rosbridge.md':                ['ros', 'bridge', 'middleware'],
}

idx = json.loads(IDX.read_text(encoding='utf-8'))
hit = 0
for g in idx['groups']:
    for it in g['items']:
        if it['path'] in TAG_MAP:
            it['tags'] = TAG_MAP[it['path']]
            if it['path'] == 'study/demo-features.md':
                it['date'] = '2026-06-08'
                it['excerpt'] = 'KaTeX 公式 + highlight.js 代码高亮 + 标签搜索的功能验证'
            hit += 1
        else:
            it.setdefault('tags', [])  # 向后兼容：其余自动补空 tags

IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

total = sum(len(g['items']) for g in idx['groups'])
print(f'已给 {hit} 个笔记打 tags')
print(f'当前 groups={len(idx["groups"])}, items={total}')
