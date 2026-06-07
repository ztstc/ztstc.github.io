#!/usr/bin/env node
/**
 * 扫描 notes/ 目录下的所有 .md 文件，
 * 自动生成 / 更新 assets/data/notes-index.json。
 *
 * 用法：
 *   node scripts/update-notes-index.mjs
 *
 * 规则：
 *   - 第一级子目录作为分组（如 notes/study/xxx.md -> "study"）
 *   - 顶层 .md 文件归到 "未分类" 分组
 *   - 已存在于 index.json 且 path 一致的条目保留 title
 *   - 新文件追加到对应分组
 *   - 文件被删除时，从 index.json 中移除
 */

import { readFile, writeFile, readdir, stat } from 'node:fs/promises';
import { join, relative, sep, posix, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT = join(__dirname, '..');
const NOTES_DIR = join(ROOT, 'notes');
const INDEX_PATH = join(ROOT, 'assets', 'data', 'notes-index.json');

const LANG = {
  sidebarTitle: { zh: '笔记目录', en: 'Notes' },
  groupTitles: {
    '': { zh: '未分类', en: 'Uncategorized' },
  },
};

async function walk(dir, base = dir) {
  const out = [];
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch (err) {
    if (err.code === 'ENOENT') return out;
    throw err;
  }
  for (const entry of entries) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...(await walk(full, base)));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      const rel = relative(base, full).split(sep).join(posix.sep);
      out.push(rel);
    }
  }
  return out;
}

function extractTitle(md, fallback) {
  const m = md.match(/^\s*#\s+(.+?)\s*$/m);
  if (!m) return fallback;
  // 去 markdown 链接包装: [text](url) -> text
  // 适用 ROS 教程里 "# [1.2 ROS安装](..)" 这类返回导航
  const cleaned = m[1].replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').trim();
  return cleaned || fallback;
}

function firstSegment(path) {
  const parts = path.split(posix.sep);
  return parts.length > 1 ? parts[0] : '';
}

async function build() {
  const files = (await walk(NOTES_DIR)).sort();
  console.log(`[notes-index] found ${files.length} markdown file(s)`);

  // 读取已有索引
  let existing = { sidebarTitle: '笔记目录', sidebarTitleEn: 'Notes', groups: [] };
  try {
    const raw = await readFile(INDEX_PATH, 'utf8');
    existing = JSON.parse(raw);
    if (!Array.isArray(existing.groups)) existing.groups = [];
  } catch (err) {
    if (err.code !== 'ENOENT') throw err;
  }

  // 把现有条目拍平成 path -> entry 映射
  const flat = new Map();
  for (const g of existing.groups) {
    for (const it of g.items || []) {
      if (it?.path) flat.set(it.path, { ...it, _group: g.title });
    }
  }

  const seen = new Set();
  const grouped = new Map(); // groupTitle -> items[]
  for (const file of files) {
    seen.add(file);
    let abs;
    try {
      abs = await readFile(join(NOTES_DIR, file), 'utf8');
    } catch (err) {
      console.warn(`[notes-index] skip ${file}: ${err.message}`);
      continue;
    }
    const fallback = file.replace(/\.md$/, '').split(posix.sep).pop();
    const title = extractTitle(abs, fallback);
    const groupKey = firstSegment(file);
    const groupTitleZh = LANG.groupTitles[groupKey]?.zh || groupKey || '未分类';
    const groupTitleEn = LANG.groupTitles[groupKey]?.en || groupKey || 'Uncategorized';

    const prev = flat.get(file) || {};
    const item = {
      path: file,
      title: prev.title && prev.title !== fallback ? prev.title : title,
      titleEn: prev.titleEn || '',
    };
    if (!grouped.has(groupTitleZh)) {
      grouped.set(groupTitleZh, { title: groupTitleZh, titleEn: groupTitleEn, items: [] });
    }
    grouped.get(groupTitleZh).items.push(item);
  }

  // 报告被删除的文件
  for (const path of flat.keys()) {
    if (!seen.has(path)) {
      console.log(`[notes-index] removed: ${path}`);
    }
  }

  // 按 groupTitle 排序，未分类放最后
  const groups = Array.from(grouped.entries()).map(([_, g]) => g);
  groups.sort((a, b) => {
    if (a.title === '未分类') return 1;
    if (b.title === '未分类') return -1;
    return a.title.localeCompare(b.title, 'zh');
  });

  const out = {
    sidebarTitle: existing.sidebarTitle || LANG.sidebarTitle.zh,
    sidebarTitleEn: existing.sidebarTitleEn || LANG.sidebarTitle.en,
    groups,
  };

  await writeFile(INDEX_PATH, JSON.stringify(out, null, 2) + '\n', 'utf8');
  console.log(`[notes-index] wrote ${INDEX_PATH}`);
  console.log(`[notes-index] groups: ${groups.length}, items: ${groups.reduce((n, g) => n + g.items.length, 0)}`);
}

build().catch((err) => {
  console.error('[notes-index] failed:', err);
  process.exit(1);
});
