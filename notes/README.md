# 欢迎来到个人 Wiki

这里用来沉淀学习笔记、项目复盘、读过的论文与书。

## 如何使用

- 左侧是按主题分组的笔记目录
- 点击任意一篇进入阅读
- 也可以直接修改 URL：`#notes?path=study/dp.md`

## 如何新增一篇笔记

1. 在 `notes/` 下新建一个 `.md` 文件，建议按主题分目录，例如 `notes/study/xxx.md`
2. 编辑 `assets/data/notes-index.json`，把新文件登记到对应分组
3. 也可以直接运行 `node scripts/update-notes-index.mjs` 自动扫描 `notes/` 并生成索引

> 后续如果想加入 frontmatter（标签、日期、作者等），可以扩展 `notes.js` 来解析。

## 目录约定

```
notes/
├── README.md                    # 当前页
├── getting-started.md
├── study/                       # 学习笔记
│   ├── dynamic-programming.md
│   └── git-cheatsheet.md
└── projects/                    # 项目复盘
    └── opendog-notes.md
```
