"""统一 5 个 project 详情页的 nav 结构：和 index.html 保持一致

改 4 处：
1. <head> 加 tabs.css（tab 按钮的样式）
2. <body> nav 内的 .nav-links 整块 → .nav-tabs 容器（首页/项目/笔记 3 个 tab 链接回主页对应区）
3. lang-toggle 按钮文字 涓\u0e13枃 → 中文（之前 mojibake 写错）
4. footer 漏 → © （版权符号）
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJ = ROOT / 'pages' / 'projects'

# 1. 加 tabs.css（紧跟 style.css 后）
OLD_LINK = '  <link rel="stylesheet" href="../../assets/css/style.css">\n  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">'
NEW_LINK = '''  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="stylesheet" href="../../assets/css/tabs.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">'''

# 2. nav 内的 .nav-links 整块换成 .nav-tabs（3 个 tab 链接回主页区，"项目"高亮）
OLD_NAV_LINKS = '''        <div class="nav-links">
          <a href="../../index.html#projects" data-i18n="nav.projects">Projects</a>
          <a href="../../index.html#documents" data-i18n="nav.documents">Documents</a>
        </div>'''
NEW_NAV_TABS = '''        <div class="nav-tabs" role="tablist" aria-label="主导航">
          <a class="tab-btn" role="tab" href="../../index.html#home"><span class="tab-label" data-i18n="tabs.home">首页</span></a>
          <a class="tab-btn active" role="tab" aria-selected="true" href="../../index.html#projects"><span class="tab-label" data-i18n="tabs.projects">项目</span></a>
          <a class="tab-btn" role="tab" href="../../index.html#notes"><span class="tab-label" data-i18n="tabs.notes">笔记</span></a>
        </div>'''

# 3. lang-toggle 按钮的乱码字（涓\u0e13枃）→ 中文
OLD_LANG = '<button class="control-btn lang-toggle" aria-label="Toggle Language">涓\u0e13枃</button>'
NEW_LANG = '<button class="control-btn lang-toggle" aria-label="Toggle Language">中文</button>'

# 4. footer 乱码（漏）→ ©
OLD_FOOTER = '<footer data-i18n="footer.copyright">漏 2026 ztstc. All rights reserved.</footer>'
NEW_FOOTER = '<footer data-i18n="footer.copyright">© 2026 ztstc. All rights reserved.</footer>'

repls = [
    (OLD_LINK, NEW_LINK, 'tabs.css link'),
    (OLD_NAV_LINKS, NEW_NAV_TABS, 'nav-links → nav-tabs'),
    (OLD_LANG, NEW_LANG, 'lang text'),
    (OLD_FOOTER, NEW_FOOTER, 'footer \u00a9'),
]

changed = 0
for n in range(1, 6):
    p = PROJ / f'project{n}.html'
    if not p.exists():
        print(f'  MISS {p.name}')
        continue
    txt = p.read_text(encoding='utf-8')
    before = txt
    diffs = []
    for old, new, label in repls:
        if old in txt:
            txt = txt.replace(old, new, 1)
            diffs.append(label)
    if txt != before:
        p.write_text(txt, encoding='utf-8')
        print(f'  OK   {p.name}: {", ".join(diffs)}')
        changed += 1
    else:
        print(f'  SKIP {p.name}: no match')

print(f'\n{changed}/5 project pages updated')
