"""给 notes/ros-tutorials/ 下所有 .md 笔记批量打 tags，写入 assets/data/notes-index.json。

tags 规则：每个笔记都加 ["ros", "tutorial"] 作为通用，再加按文件名关键字判定的专属 tag。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / 'assets' / 'data' / 'notes-index.json'

# path 后缀 → 专属 tag
SPECIFIC = {
    'ROS 是什么':            ['intro', 'overview', 'concepts'],
    'ROS1 vs ROS2':          ['ros1', 'ros2', 'migration', 'comparison'],
    'ROS1 入门':             ['ros1', 'beginner', 'tutorial-basics'],
    'ROS1 核心':             ['ros1', 'concepts'],
    'ROS2建图':              ['ros2', 'slam', 'navigation', 'mapping'],
    'VS Code':               ['vscode', 'ide', 'packaging'],
    '创建工作空间':          ['workspace', 'catkin', 'compilation'],
    '安装Ubuntu':            ['ubuntu', 'installation', 'noetic'],
    '系统更新':              ['ros2', 'system', 'installation', 'humble'],
    '快速参考':              ['reference', 'cheatsheet'],
    '摄像头':                ['camera', 'usb_cam', 'topic'],
    '配置激光':              ['lidar', 'sensor', 'configuration'],
}
COMMON = ['ros', 'tutorial']

idx = json.loads(IDX.read_text(encoding='utf-8'))
g = next((g for g in idx['groups'] if g['title'] == 'ros-tutorials'), None)
if not g:
    print('ERROR: ros-tutorials 组不存在于 index.json')
    raise SystemExit(1)

count = 0
for it in g['items']:
    tags = list(COMMON)
    for key, vals in SPECIFIC.items():
        if key in it['path']:
            tags.extend(vals)
            break
    it['tags'] = tags
    count += 1

IDX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'已给 {count} 篇 ros-tutorials 笔记打 tags')
for it in g['items'][:3]:
    print(f"  {it['path'][:50]}... → {it['tags']}")
