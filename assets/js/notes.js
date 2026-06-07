/* =========================================
   Notes Wiki Renderer
   - 加载 assets/data/notes-index.json 渲染侧栏
   - 点击条目后 fetch 笔记 .md，调用 marked 渲染
   - 监听 tabs.js 的 notes:navigate 事件
   ========================================= */
(() => {
  const INDEX_URL = 'assets/data/notes-index.json';
  const NOTES_BASE = 'notes/';  // 笔记源文件目录
  const VIEWER_SELECTOR = '.notes-viewer';
  const SIDEBAR_SELECTOR = '.notes-sidebar';

  let indexCache = null;
  let currentPath = null;
  let loadToken = 0;  // 防止快速切换导致竞态

  async function loadIndex() {
    if (indexCache) return indexCache;
    try {
      const res = await fetch(INDEX_URL, { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      indexCache = await res.json();
      return indexCache;
    } catch (err) {
      console.error('[notes] failed to load index:', err);
      throw err;
    }
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
  }

  function renderSidebar(indexData) {
    const sidebar = document.querySelector(SIDEBAR_SELECTOR);
    if (!sidebar) return;

    const emptyText = window.i18n?.get?.('notes.empty') || '还没有笔记，先在 notes/ 目录里写一篇吧~';
    if (!indexData?.groups?.length) {
      sidebar.innerHTML = `
        <div class="notes-sidebar-title" data-i18n="notes.sidebarTitle">笔记目录</div>
        <div style="padding:12px 8px; color:var(--text-muted); font-size:0.85rem;">${escapeHtml(emptyText)}</div>
      `;
      return;
    }

    const groupsHtml = indexData.groups.map((group, gi) => {
      const gid = `g-${gi}`;
      const items = (group.items || []).map((it) => `
        <li><a class="notes-list-item" data-note-path="${escapeHtml(it.path)}" href="#notes?path=${encodeURIComponent(it.path)}">${escapeHtml(it.title)}</a></li>
      `).join('');
      // 默认展开第一组
      const open = gi === 0 ? ' open' : '';
      return `
        <details class="notes-group"${open}>
          <summary class="notes-group-title">${escapeHtml(group.title)}</summary>
          <ul class="notes-list">${items}</ul>
        </details>
      `;
    }).join('');

    sidebar.innerHTML = `
      <div class="notes-sidebar-title" data-i18n="notes.sidebarTitle">${escapeHtml(indexData.sidebarTitle || '笔记目录')}</div>
      ${groupsHtml}
    `;
  }

  function highlightActiveItem(path) {
    document.querySelectorAll('.notes-list-item').forEach((el) => {
      el.classList.toggle('active', el.dataset.notePath === path);
    });
    // 自动展开活动项所在的 group（解决"目录层级混乱"：点开非默认 group 看不清 active 项）
    const active = document.querySelector('.notes-list-item.active');
    if (active) {
      const group = active.closest('details.notes-group');
      if (group && !group.hasAttribute('open')) {
        group.setAttribute('open', '');
      }
    }
  }

  function renderBreadcrumb(path, title) {
    const parts = path.split('/').filter(Boolean);
    const sep = '<span class="sep">/</span>';
    let html = `<a href="#notes" data-i18n="notes.wiki">笔记</a>${sep}`;
    let acc = '';
    parts.forEach((p, i) => {
      acc += p + (i < parts.length - 1 ? '/' : '');
      if (i < parts.length - 1) {
        html += `<span>${escapeHtml(p)}</span>${sep}`;
      } else {
        html += `<span class="current">${escapeHtml(p)}</span>`;
      }
    });
    return `<nav class="notes-breadcrumb">${html}</nav>`;
  }

  // 中文标题转 slug：保留汉字，做简单归一化
  function slugify(text) {
    return String(text)
      .trim()
      .toLowerCase()
      .replace(/[\s\u3000]+/g, '-')         // 空白（含全角）→ -
      .replace(/[`*_~()\[\]!#<>]/g, '')      // 去掉 md 标点
      .replace(/[，。！？、；：·…—「」『』《》]/g, '') // 去掉常见中文标点
      .replace(/-{2,}/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function configureMarked() {
    if (typeof window.marked === 'undefined') {
      console.warn('[notes] marked is not loaded');
      return;
    }
    try {
      window.marked.setOptions({
        gfm: true,
        breaks: false,
        headerIds: true,
        mangle: false,
      });
    } catch (e) {
      console.warn('[notes] setOptions failed, falling back', e);
    }
    // 兼容 marked v5+ / 旧版差异：用 renderer.heading 兜底注入 id，
    // 让笔记里 [跳转](#xxx) 这种锚点能命中（fpga.md 等笔记依赖此功能）
    try {
      const seen = new Set();
      window.marked.use({
        renderer: {
          heading(text, level) {
            const raw = String(text).replace(/<[^>]+>/g, ''); // 去内联 html
            let id = slugify(raw);
            if (!id) id = `h${level}-${seen.size}`;
            // 同标题去重
            let unique = id;
            let n = 2;
            while (seen.has(unique)) { unique = `${id}-${n++}`; }
            seen.add(unique);
            return `<h${level} id="${unique}">${text}</h${level}>\n`;
          }
        }
      });
    } catch (e) {
      console.warn('[notes] renderer override failed', e);
    }
  }

  async function loadAndRenderNote(path) {
    const viewer = document.querySelector(VIEWER_SELECTOR);
    if (!viewer) return;

    const myToken = ++loadToken;
    const url = NOTES_BASE + path;
    highlightActiveItem(path);
    currentPath = path;

    // 显示加载中
    const loadingText = window.i18n?.get?.('notes.loading') || '加载中…';
    viewer.innerHTML = `<div class="notes-loading">${escapeHtml(loadingText)}</div>`;

    try {
      const res = await fetch(url, { cache: 'no-store' });
      if (myToken !== loadToken) return;  // 被更新的请求取代
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const md = await res.text();
      if (myToken !== loadToken) return;

      // 取首行 # 作为标题（如果有）
      let title = path.split('/').pop().replace(/\.md$/, '');
      const h1Match = md.match(/^\s*#\s+(.+?)\s*$/m);
      if (h1Match) title = h1Match[1].trim();

      // 提取首段非空文本作为摘要（不渲染到页面）
      let html = window.marked ? window.marked.parse(md) : `<pre>${escapeHtml(md)}</pre>`;

      // 修正相对图片路径：index.html 是 base URL，但 .md 里的 src 是相对于笔记文件
      // 例：study/fpga.md 里的 assets/foo.png 实际在 notes/study/assets/foo.png
      // 必须拼上 NOTES_BASE（'notes/'），否则浏览器请求 study/assets/...（404）
      const lastSlash = path.lastIndexOf('/');
      const baseDir = lastSlash >= 0
        ? NOTES_BASE + path.substring(0, lastSlash + 1)
        : NOTES_BASE;
      html = html.replace(
        /(<img[^>]+src=")([^"]+)(")/g,
        (m, p, s, suf) => {
          if (s.startsWith('http') || s.startsWith('/') || s.startsWith('data:') || s.startsWith('blob:')) return m;
          return p + baseDir + s + suf;
        }
      );

      viewer.innerHTML = `
        ${renderBreadcrumb(path, title)}
        <article class="notes-content">${html}</article>
      `;
    } catch (err) {
      if (myToken !== loadToken) return;
      console.error('[notes] failed to load', path, err);
      const errText = window.i18n?.get?.('notes.loadError') || '加载失败，请检查文件是否存在。';
      viewer.innerHTML = `
        ${renderBreadcrumb(path)}
        <div class="notes-error">
          <p>${escapeHtml(errText)}</p>
          <p style="font-size:0.8rem;opacity:0.7;margin-top:8px;">${escapeHtml(url)}</p>
        </div>
      `;
    }
  }

  function showEmpty() {
    const viewer = document.querySelector(VIEWER_SELECTOR);
    if (!viewer) return;
    const empty = {
      icon: '📚',
      title: window.i18n?.get?.('notes.welcomeTitle') || '欢迎来到笔记 Wiki',
      text: window.i18n?.get?.('notes.welcomeText') || '从左侧选择一篇笔记开始阅读，或在 notes/ 目录新增你的 .md 文件。',
    };
    viewer.innerHTML = `
      <div class="notes-viewer-empty">
        <div class="notes-viewer-empty-icon">${empty.icon}</div>
        <div class="notes-viewer-empty-text" style="font-size:1.1rem;font-weight:600;color:var(--text-main);">${escapeHtml(empty.title)}</div>
        <div class="notes-viewer-empty-text">${escapeHtml(empty.text)}</div>
      </div>
    `;
  }

  // 全局事件：sidebar 点击（事件代理）
  function bindSidebarClick() {
    const sidebar = document.querySelector(SIDEBAR_SELECTOR);
    if (!sidebar) return;
    sidebar.addEventListener('click', (e) => {
      const link = e.target.closest('.notes-list-item');
      if (!link) return;
      e.preventDefault();
      const path = link.dataset.notePath;
      if (!path) return;
      window.wikiTabs.navigate('notes', { path });
    });
  }

  // 全局事件：tab 切换到 notes
  function onTabChange(e) {
    if (e.detail.tab !== 'notes') return;
    // 第一次切到 notes 时才绑定 sidebar 点击（避免空侧栏报错）
    bindSidebarClick();
    if (!currentPath) {
      // 解析 hash 里的 path
      const raw = window.location.hash.replace(/^#/, '');
      const [, query = ''] = raw.split('?');
      const params = {};
      if (query) {
        query.split('&').forEach((kv) => {
          const [k, v = ''] = kv.split('=');
          params[decodeURIComponent(k)] = decodeURIComponent(v);
        });
      }
      if (params.path) {
        loadAndRenderNote(params.path);
      } else {
        showEmpty();
      }
    }
  }

  // 监听来自 tabs.js 的导航事件（hash 改变时）
  function onNotesNavigate(e) {
    const path = e.detail.path;
    if (path) loadAndRenderNote(path);
  }

  async function init() {
    configureMarked();
    try {
      const indexData = await loadIndex();
      renderSidebar(indexData);
    } catch {
      // index 加载失败也要渲染一个空侧栏
      renderSidebar({ groups: [] });
    }
    document.addEventListener('tabchange', onTabChange);
    document.addEventListener('notes:navigate', onNotesNavigate);
  }

  // 暴露给外部（调试用）
  window.wikiNotes = {
    refreshIndex: () => { indexCache = null; },
    getCurrentPath: () => currentPath,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
