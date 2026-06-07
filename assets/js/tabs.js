/* =========================================
   Tab 路由（hash-based）
   - 支持 #home / #projects / #notes
   - 支持 #notes?path=xxx.md 定位笔记
   - 切 tab 时切换 body[data-active-panel] 触发主题渐变
   - 使用 View Transitions API 让切换更顺滑
   ========================================= */
(() => {
  const VALID_TABS = ['home', 'projects', 'notes'];
  const DEFAULT_TAB = 'home';

  // 解析 hash，支持 "#notes?path=xxx.md" 格式
  function parseHash() {
    const raw = window.location.hash.replace(/^#/, '');
    if (!raw) return { tab: DEFAULT_TAB, params: {} };
    const [path, query = ''] = raw.split('?');
    const params = {};
    if (query) {
      query.split('&').forEach((kv) => {
        const [k, v = ''] = kv.split('=');
        params[decodeURIComponent(k)] = decodeURIComponent(v);
      });
    }
    const tab = VALID_TABS.includes(path) ? path : DEFAULT_TAB;
    return { tab, params };
  }

  // 把当前 panel 写到 body 上，触发 CSS 变量切换
  function syncBodyPanel(tab) {
    document.body.setAttribute('data-active-panel', tab);
  }

  // 真正的 DOM 切换（在 View Transition 回调里执行）
  function swapTabDom(tab) {
    document.querySelectorAll('.tab-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.tab === tab);
      btn.setAttribute('aria-selected', btn.dataset.tab === tab ? 'true' : 'false');
    });
    document.querySelectorAll('.tab-panel').forEach((panel) => {
      panel.classList.toggle('active', panel.dataset.panel === tab);
    });
    syncBodyPanel(tab);
    // 切到 tab 时滚到顶部
    window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
    // 触发自定义事件，方便 notes.js 等订阅
    document.dispatchEvent(new CustomEvent('tabchange', { detail: { tab } }));
  }

  // 用 View Transitions API 包一层，让切换更顺滑
  function setActiveTab(tab) {
    if (typeof document.startViewTransition === 'function') {
      document.startViewTransition(() => swapTabDom(tab));
    } else {
      swapTabDom(tab);
    }
  }

  function applyRoute() {
    const { tab, params } = parseHash();
    setActiveTab(tab);
    if (tab === 'notes' && params.path) {
      document.dispatchEvent(new CustomEvent('notes:navigate', { detail: { path: params.path } }));
    }
  }

  function bindTabClicks() {
    document.querySelectorAll('.tab-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const tab = btn.dataset.tab;
        if (!tab) return;
        const current = parseHash();
        let newHash = `#${tab}`;
        if (tab === 'notes' && current.tab === 'notes' && current.params.path) {
          newHash = `#notes?path=${current.params.path}`;
        }
        if (window.location.hash !== newHash) {
          window.location.hash = newHash;
        } else {
          // 已经在目标 tab，强制重新触发以便刷新
          applyRoute();
        }
      });
    });
  }

  // 提供给其他模块更新 hash 的方法
  window.wikiTabs = {
    navigate(tab, params = {}) {
      let hash = `#${tab}`;
      const entries = Object.entries(params);
      if (entries.length) {
        const qs = entries.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join('&');
        hash += `?${qs}`;
      }
      window.location.hash = hash;
    },
    getCurrentTab() {
      return parseHash().tab;
    },
  };

  window.addEventListener('hashchange', () => applyRoute());
  document.addEventListener('DOMContentLoaded', () => {
    bindTabClicks();
    applyRoute();
  });
})();
