"""校对 lang/en.json：以 lang/zh.json 为准。
修复项目：
1. projects.item2/3/4/5.tags 对齐到中文
2. opensource.item1.desc 修 mojibake
3. timeline 整段重写为中文版
4. 清理多余的 timeline.event10/event11
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / 'lang' / 'en.json'

# 1. projects.tags 修复（以中文为准）
TAG_FIXES = {
    'item2': ['RL', 'Embedded Systems', 'ROS', 'STM32', 'FreeRTOS'],
    'item3': ['Robotics', 'FOC', 'Motor Control', 'Embedded Systems', 'ESP32'],
    'item4': ['LVGL', 'Embedded Systems', 'SquareLineStudio', 'ESP32', 'IOT'],
    'item5': ['Agricultural Robotics', 'Embedded Systems', 'ESP32', 'IOT'],
}

# 2. opensource.item1.desc 修 mojibake
ITEM1_DESC = (
    "Project 'BLACK\u2606ROCK SHOOTER': A full-stack parallel structure quadruped robot. "
    "The complete solution is open-source and competed in the 2025 ROBOCON National Competition."
)

# 3. timeline 整段重写（以 zh 为准）
TIMELINE = {
    'title': 'Timeline',
    'event1': {
        'date': '2024.09',
        'title': 'Joined HDU RAS-IRU Robotics Lab',
        'desc': 'Started learning ROS and participating in the lab\u2019s robotics project development and maintenance work.',
        'link': {'url': 'https://hdu-raslab.github.io/', 'label': 'RAS'},
    },
    'event2': {
        'date': '2025.03',
        'title': 'Received Third-Class Scholarship',
        'desc': '',
    },
    'event3': {
        'date': '2025.06 - 2026.09',
        'title': 'Vice Minister of the Media & News Department, Student Union, Hangzhou Dianzi University Shengguangji College',
        'desc': 'Organized and participated in filming and recording of multiple college events; contributed to public WeChat article writing.',
    },
    'event4': {
        'date': '2025.07',
        'title': 'Gold Award, 15th Zhejiang Province \u201cChallenge Cup\u201d Extracurricular Academic Sci-Tech Works Competition',
        'desc': 'As a core member of the \u201cStrawberry Twice\u201d team, designed and developed the IoT sensors, cameras, and water-fertilizer integrated equipment for a strawberry-cultivation intelligent monitoring system.',
    },
    'event5': {
        'date': '2025.08',
        'title': 'Gold Award, Zhejiang Province International College Students Innovation Competition (2025)',
        'desc': 'As a member of the \u201cStrawberry Twice\u201d team, designed and developed the IoT sensors, cameras, and water-fertilizer integrated equipment for a strawberry-cultivation intelligent monitoring system.',
    },
    'event6': {
        'date': '2025.10',
        'title': 'Received Second-Class Scholarship',
        'desc': '',
    },
    'event7': {
        'date': '2025.12',
        'title': 'Second Prize, 4th Robotics Challenge of HDU-ITMO (Mapping & Navigation Speed Race)',
        'desc': 'As team captain, led the development and integration of the car\u2019s chassis design, drive, mapping, and vision modules.',
    },
    'event8': {
        'date': '2026.04',
        'title': 'Received First-Class Scholarship',
        'desc': '',
    },
    'event9': {
        'date': '2026.05',
        'title': 'Silver Award, 15th Zhejiang Province \u201cChallenge Cup\u201d College Students Entrepreneurship Plan Competition',
        'desc': 'As a core member of the \u201cWeilin Technology\u201d team, participated in on-site Q&A; the project (intelligent forestry-painting inspection robot) was exhibited and recognized.',
    },
}

# 4. footer 微调：日期统一为 2026（与中文一致）
FOOTER = '\u00a9 2026 ztstc | Personal Homepage'

en = json.loads(EN.read_text(encoding='utf-8'))

# 应用 tags 修复
for k, v in TAG_FIXES.items():
    en['projects'][k]['tags'] = v

# 修 mojibake
en['opensource']['item1']['desc'] = ITEM1_DESC

# 重写 timeline
en['timeline'] = TIMELINE

# footer 统一
en['footer']['copyright'] = FOOTER

EN.write_text(json.dumps(en, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'en.json 校对完成: {sum(1 for _ in TAG_FIXES)} tags + opensource.item1.desc + timeline + footer 全部对齐到 zh')
