# 如何新建一篇笔记

## 方式一：手动（推荐新手）

1. 在 `notes/` 下创建你的 `.md` 文件，比如 `notes/study/my-topic.md`
2. 编辑 `assets/data/notes-index.json`，在对应分组里加上：

   ```json
   {
     "path": "study/my-topic.md",
     "title": "我的主题",
     "titleEn": "My Topic"
   }
   ```

3. 刷新页面，左侧目录就会出现这篇笔记

## 方式二：自动扫描

运行：

```bash
node scripts/update-notes-index.mjs
```

它会扫描 `notes/` 下所有 `.md` 文件，自动追加到 `notes-index.json`。新文件默认归到"未分类"分组，你可以在脚本运行后再手动调整分组。

## Markdown 排版技巧

- 标题用 `#`、`##`、`##`...
- 代码块用三反引号
- 引用用 `>`
- 链接用 `[text](url)`
- 列表用 `-` 或 `1.`

## 接下来

- 想要公式？引入 KaTeX
- 想要代码高亮？引入 highlight.js
- 想要标签 / 分类 / 搜索？扩展 `notes-index.json` 的 schema
