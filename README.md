# My Wiki · Personal Hub

基于 [ztstc's Homepage](https://github.com/ztstc/My_wiki) 改造的个人主页 + 笔记 Wiki。
在 Lain-Ego0 仓库基础上 fork，加入 **Tab 栏** + **个人项目磁贴** + **Markdown 笔记 Wiki** 三大能力。

## 站点结构

三个 Tab，通过 URL Hash 切换：

| Tab | Hash | 内容 |
|-----|------|------|
| 🏠 首页 | `#home` | 个人简介、Timeline（时间轴）、Skills（技术栈）、OpenSource |
| 🚀 项目 | `#projects` | 项目磁贴网格，点击进入 `pages/projects/*.html` 详情页 |
| 📚 笔记 | `#notes` 或 `#notes?path=xxx.md` | 左侧目录 + 右侧 MD 渲染区 |

## 目录结构

```
My_wiki/
├── index.html                    # 入口，承载 3 个 tab
├── pages/projects/               # 项目详情页（独立 HTML）
├── notes/                        # MD 笔记源文件
│   ├── README.md
│   ├── getting-started.md
│   ├── study/                    # 学习笔记
│   │   ├── dynamic-programming.md
│   │   └── git-cheatsheet.md
│   └── projects/                 # 项目复盘
│       └── opendog-notes.md
├── assets/
│   ├── css/
│   │   ├── style.css             # 主题、布局
│   │   ├── tabs.css              # Tab 栏样式
│   │   └── notes.css             # 笔记页面布局 + markdown 排版
│   ├── js/
│   │   ├── i18n.js               # 中英文切换
│   │   ├── main.js               # 主题、Skills/Timeline/OpenSource 渲染
│   │   ├── tabs.js               # Tab 路由（hash-based）
│   │   └── notes.js              # MD 加载 + marked 渲染
│   ├── data/
│   │   ├── notes-index.json      # 笔记索引
│   │   └── projects.json         # 项目数据
│   ├── vendor/
│   │   └── marked.min.js         # MD 渲染器（本地化）
│   └── images/                   # 头像 + 项目封面
├── lang/
│   ├── zh.json
│   └── en.json
├── scripts/
│   └── update-notes-index.mjs    # 自动扫描 notes/ 生成索引
└── README.md
```

## 本地预览

```bash
python -m http.server 8080
# 访问 http://localhost:8080
```

或使用 VSCode Live Server 插件。

## 部署到 GitHub Pages

> 项目里已经备好 `.nojekyll`、`.gitignore`、`.github/workflows/pages.yml`，推送即可自动部署。

本项目作为 **User Site** 部署到 `ztstc.github.io`（仓库名必须是 `ztstc.github.io`），访问 `https://ztstc.github.io/` 即可。

```bash
# 1. 提交所有本地改动
git add -A
git commit -m "Initial commit: ztstc Wiki (notes + i18n + projects)"

# 2. 移除旧的 Lain-Ego0 远程
git remote remove origin

# 3. 用 gh CLI 创建并推送（首次会自动建仓 + 推送）
gh repo create ztstc.github.io --public --source=. --remote=origin --push \
  --description "ztstc's personal wiki + project hub"

# 4. 启用 Pages：仓库 Settings → Pages → Source 选 "GitHub Actions"
```

之后每次 `git push` 到 main 分支，`.github/workflows/pages.yml` 会自动重新部署。

## 如何新增一篇笔记

1. 在 `notes/` 下创建 `.md` 文件，建议按主题分目录
2. 跑一次 `node scripts/update-notes-index.mjs` 自动扫描追加到 `notes-index.json`
   - 也可手动编辑 `assets/data/notes-index.json` 调整分组和标题
3. 刷新页面即可在侧栏看到

> 笔记分组规则：第一级子目录作为分组（如 `notes/study/foo.md` 归到 `study` 分组），顶层 `.md` 归到「未分类」。

## 如何新增/修改一个项目

- 数据定义在 `assets/js/main.js` 的 `PROJECTS` 数组
- 详情页放在 `pages/projects/projectN.html`
- 改完在 `lang/zh.json` 和 `lang/en.json` 同步 `projects.itemN` 文案

> 后续可考虑把 `PROJECTS` 改成读 `assets/data/projects.json`，与笔记模块保持一致。

## Tab 路由说明

`assets/js/tabs.js` 用 URL Hash 实现路由：

- `#home` → 首页 tab
- `#projects` → 项目 tab
- `#notes` → 笔记 tab（显示欢迎页）
- `#notes?path=study/dp.md` → 笔记 tab 并自动加载指定文档

切换 tab 不刷新页面，主题 / 语言状态保持。

## 主题与语言

- 主题：light / dark，写在 `localStorage.theme`
- 语言：zh / en，写在 `localStorage.lang`
- 文案维护在 `lang/zh.json` 和 `lang/en.json`

## 后续可升级项

- 数学公式渲染（引入 KaTeX）
- 代码高亮（引入 highlight.js / Prism）
- MD frontmatter 解析（标签、日期）
- 笔记全文搜索
- 项目数据迁到 `assets/data/projects.json`
- 笔记分类标签 / 归档时间线
