"""Add tabs/notes keys to zh.json and en.json."""
import json
import sys
from pathlib import Path

TABS_ZH = {'home': '首页', 'projects': '项目', 'notes': '笔记'}
NOTES_ZH = {
    'wiki': '笔记',
    'sidebarTitle': '笔记目录',
    'welcomeTitle': '欢迎来到笔记 Wiki',
    'welcomeText': '从左侧选择一篇笔记开始阅读',
    'loading': '加载中…',
    'loadError': '加载失败，请检查文件是否存在。',
    'empty': '还没有笔记，先在 notes/ 目录里写一篇吧~',
}
TABS_EN = {'home': 'Home', 'projects': 'Projects', 'notes': 'Notes'}
NOTES_EN = {
    'wiki': 'Notes',
    'sidebarTitle': 'Notes',
    'welcomeTitle': 'Welcome to the Wiki',
    'welcomeText': 'Pick a note from the sidebar to start reading',
    'loading': 'Loading…',
    'loadError': 'Failed to load. Please check if the file exists.',
    'empty': 'No notes yet. Create your first .md in the notes/ folder.',
}

ok = True
for path, tabs, notes in [
    ('lang/zh.json', TABS_ZH, NOTES_ZH),
    ('lang/en.json', TABS_EN, NOTES_EN),
]:
    try:
        p = Path(path)
        d = json.loads(p.read_text(encoding='utf-8'))
        d['tabs'] = tabs
        d['notes'] = notes
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"patched {path}")
    except Exception as e:
        print(f"{path}: FAILED -> {e}")
        ok = False

sys.exit(0 if ok else 1)
