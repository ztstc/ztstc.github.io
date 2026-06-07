(() => {
  const PROJECT_TAG_LIBRARY = {
    ROBOTICS: 'Robotics',
    EMBEDDED: 'Embedded Systems',
    REINFORCEMENT_LEARNING: 'Reinforcement Learning',
    SIM2REAL: 'Sim2Real',
    DEPLOYMENT: 'Deployment',
    FREERTOS: 'FreeRTOS',
    MOTION_CONTROL: 'Motion Control',
    MOTOR_CONTROL: 'Motor Control',
    SLAM: 'SLAM',
    LIDAR: 'LiDAR',
    MECHANICAL_DESIGN: 'Mechanical Design',
    UNDERWATER_ROBOTICS: 'Underwater Robotics',
    VECTOR_PROPULSION: 'Vector Propulsion',
    WATERPROOF_ENGINEERING: 'Waterproof Engineering',
    AGRICULTURAL_ROBOTICS: 'Agricultural Robotics',
    MULTI_ROBOT_COLLABORATION: 'Multi-Robot Collaboration',
    WIKI: 'Wiki',
    KNOWLEDGE_BASE: 'Knowledge Base',
    OPEN_SOURCE: 'Open Source',
    FOC: 'FOC',
    ESP32: 'ESP32',
    STM32: 'STM32',
    LVGL: 'LVGL',
    IOT: 'IoT',
    SQUARELINE: 'SquareLine',
    AI_AGENT: 'AI Agent',
    ROS: 'ROS',
  };

  const PROJECTS = [
    {
      img: 'assets/images/IRU-wiki-cover.jpg',
      titleKey: 'projects.item1.title',
      descKey: 'projects.item1.desc',
      tags: [
        PROJECT_TAG_LIBRARY.WIKI,
        PROJECT_TAG_LIBRARY.KNOWLEDGE_BASE,
        PROJECT_TAG_LIBRARY.ROBOTICS,
        PROJECT_TAG_LIBRARY.OPEN_SOURCE,
      ],
      link: 'pages/projects/project1.html',
    },
    {
      img: 'assets/images/奶龙-封面.jpg',
      titleKey: 'projects.item2.title',
      descKey: 'projects.item2.desc',
      tags: [
        PROJECT_TAG_LIBRARY.ROBOTICS,
        PROJECT_TAG_LIBRARY.AI_AGENT,
        PROJECT_TAG_LIBRARY.ROS,
        PROJECT_TAG_LIBRARY.STM32,
        PROJECT_TAG_LIBRARY.FREERTOS,
      ],
      link: 'pages/projects/project2.html',
    },
    {
      img: 'assets/images/FOC_驱动板-封面.jpg',
      titleKey: 'projects.item3.title',
      descKey: 'projects.item3.desc',
      tags: [
        PROJECT_TAG_LIBRARY.MOTOR_CONTROL,
        PROJECT_TAG_LIBRARY.FOC,
        PROJECT_TAG_LIBRARY.ESP32,
        PROJECT_TAG_LIBRARY.EMBEDDED,
      ],
      link: 'pages/projects/project3.html',
    },
    {
      img: 'assets/images/电脑性能看板-封面.jpg',
      titleKey: 'projects.item4.title',
      descKey: 'projects.item4.desc',
      tags: [
        PROJECT_TAG_LIBRARY.LVGL,
        PROJECT_TAG_LIBRARY.SQUARELINE,
        PROJECT_TAG_LIBRARY.ESP32,
        PROJECT_TAG_LIBRARY.IOT,
        PROJECT_TAG_LIBRARY.EMBEDDED,
      ],
      link: 'pages/projects/project4.html',
    },
    {
      img: 'assets/images/BerryAI-封面.jpg',
      titleKey: 'projects.item5.title',
      descKey: 'projects.item5.desc',
      tags: [
        PROJECT_TAG_LIBRARY.IOT,
        PROJECT_TAG_LIBRARY.ESP32,
        PROJECT_TAG_LIBRARY.AGRICULTURAL_ROBOTICS,
        PROJECT_TAG_LIBRARY.EMBEDDED,
      ],
      link: 'pages/projects/project5.html',
    },
  ];

  // 复用 projects 数据：key 直接指向 projects.itemN，自动读取 title/desc/tags
  // linkCode 暂时统一用 GitHub profile（用户后续可替换成具体 repo URL）
  const OPEN_SOURCE_ITEMS = [
    { key: 'projects.item1', linkCode: 'https://github.com/ztstc', linkDoc: null },
    { key: 'projects.item2', linkCode: 'https://github.com/ztstc', linkDoc: null },
    { key: 'projects.item3', linkCode: 'https://github.com/ztstc', linkDoc: null },
    { key: 'projects.item4', linkCode: 'https://github.com/ztstc', linkDoc: null },
    { key: 'projects.item5', linkCode: 'https://github.com/ztstc', linkDoc: null },
  ];

  const TIMELINE_EVENTS = [
    'timeline.event11',
    'timeline.event10',
    'timeline.event9',
    'timeline.event8',
    'timeline.event7',
    'timeline.event6',
    'timeline.event5',
    'timeline.event4',
    'timeline.event3',
    'timeline.event2',
    'timeline.event1',
  ];

  const TECH_STACK = [
    {
      category: 'skills.hardware',
      items: [
        { name: '3D打印', icon: 'fas fa-cube' },
        { name: 'SolidWorks', icon: 'fas fa-drafting-compass' },
        { name: '嘉立创EDA', icon: 'fas fa-pencil-ruler' },
        { name: 'KiCad', icon: 'fas fa-layer-group' },
        { name: '精密焊接', icon: 'fas fa-layer-group' }
      ],
    },
    {
      category: 'skills.embedded',
      items: [
        { name: 'STM32', icon: 'fas fa-microchip' },
        { name: 'ESP32', icon: 'fas fa-microchip' },
        { name: 'FPGA', icon: 'fas fa-microchip' },
        { name: 'MQTT', icon: 'fas fa-server' },
        { name: 'RTOS', icon: 'fas fa-cogs' },
        { name: 'Keil MDK', icon: 'fas fa-screwdriver-wrench' },
        { name: 'STM32CubeMX', icon: 'fas fa-cubes' },
        { name: 'C/C++', icon: 'fas fa-code' },
        { name: 'Micro-Python', icon: 'fab fa-python' },
      ],
    },
    {
      category: 'skills.robotics',
      items: [
        { name: 'ROS/ROS2', icon: 'fas fa-robot' },
        { name: 'RViz', icon: 'fas fa-cube' },
        { name: 'Gazebo', icon: 'fas fa-mountain-sun' },
        { name: 'MoveIt', icon: 'fas fa-bezier-curve' },
        { name: 'SLAM', icon: 'fas fa-dumbbell' },
      ],
    },
    {
      category: 'skills.software',
      items: [
        { name: 'Linux', icon: 'fab fa-linux' },
        { name: 'Git', icon: 'fab fa-git-alt' },
        { name: 'CMake', icon: 'fas fa-gears' },
        { name: 'Docker', icon: 'fab fa-docker' },
      ],
    },
    {
      category: 'skills.ai',
      items: [
        { name: 'ONNX', icon: 'fas fa-project-diagram' },
        { name: 'AI Agent development', icon: 'fas fa-brain' },
      ],
    },
  ];

  const CONTACT_LINKS = [
    // { icon: 'fab fa-bilibili', key: 'contact.bilibili', link: 'https://space.bilibili.com/340883303/upload/video' },
    { icon: 'fab fa-github', key: 'contact.github', link: 'https://github.com/ztstc' },
    // { icon: 'fab fa-zhihu', key: 'contact.zhihu', link: 'https://www.zhihu.com/people/hua-99-50-21' },
    { text: 'CSDN', key: 'contact.csdn', link: 'https://blog.csdn.net/m0_44961830' },
  ];

  function qs(selector, root = document) {
    return root.querySelector(selector);
  }

  function qsa(selector, root = document) {
    return Array.from(root.querySelectorAll(selector));
  }

  function clear(el) {
    if (!el) return;
    el.innerHTML = '';
  }

  function t(key) {
    return window.i18n?.get ? window.i18n.get(key) : key;
  }

  function renderSpanTags(tags, className) {
    if (!Array.isArray(tags)) return '';
    return tags.map((tag) => `<span class="${className}">${tag}</span>`).join('');
  }

  function renderProjectTags(tags) {
    if (!Array.isArray(tags)) return '';
    return `<div class="project-tags">${renderSpanTags(tags, 'project-tag')}</div>`;
  }

  function initThemeToggle() {
    const toggleBtn = qs('.theme-toggle');
    const htmlEl = document.documentElement;
    if (!toggleBtn) return;

    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlEl.setAttribute('data-theme', savedTheme);

    toggleBtn.addEventListener('click', () => {
      const currentTheme = htmlEl.getAttribute('data-theme');
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';

      htmlEl.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      console.log(`[Theme] Switched to ${newTheme}`);
    });
  }

  function initLangToggle() {
    const toggleBtn = qs('.lang-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
      const current = window.i18n.currentLang();
      const next = current === 'en' ? 'zh' : 'en';
      console.log(`[Lang] Switching to ${next}...`);
      window.i18n.changeLang(next);
    });
  }

  function initProjects() {
    const grid = qs('.projects-grid');
    if (!grid) return;
    clear(grid);

    PROJECTS.forEach((project) => {
      const tagsHtml = renderProjectTags(project.tags);

      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div class="project-thumbnail-wrapper">
          <img src="${project.img}" alt="${t('projects.imgAlt')}" class="project-thumbnail">
        </div>
        <div class="project-info">
          <h3>${t(project.titleKey)}</h3>
          <p>${t(project.descKey)}</p>
          ${tagsHtml}
          <a href="${project.link}" class="project-link">${t('projects.viewDetail')}</a>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  function initOpenSource() {
    const grid = qs('.opensource-grid');
    if (!grid) return;
    clear(grid);

    OPEN_SOURCE_ITEMS.forEach((item) => {
      const tags = t(`${item.key}.tags`) || [];
      const tagsHtml = renderSpanTags(tags, 'os-tag');

      let buttonsHtml = '';
      if (item.linkCode) {
        buttonsHtml += `<a href="${item.linkCode}" target="_blank" rel="noopener noreferrer" class="os-btn"><i class="fab fa-github"></i> ${t('opensource.btnCode')}</a>`;
      }
      if (item.linkDoc) {
        buttonsHtml += `<a href="${item.linkDoc}" target="_blank" rel="noopener noreferrer" class="os-btn"><i class="fas fa-book"></i> ${t('opensource.btnDoc')}</a>`;
      }

      const card = document.createElement('div');
      card.className = 'os-card';
      card.innerHTML = `
        <div class="os-header">
          <div class="os-title">${t(`${item.key}.title`)}</div>
          <i class="fas fa-code-branch" style="color:var(--primary); opacity:0.5;"></i>
        </div>
        <p class="os-desc">${t(`${item.key}.desc`)}</p>
        <div class="os-tags">${tagsHtml}</div>
        <div class="os-actions">${buttonsHtml}</div>
      `;
      grid.appendChild(card);
    });
  }

  function initTimeline() {
    const container = qs('.timeline-container');
    if (!container) return;
    clear(container);

    TIMELINE_EVENTS.forEach((key) => {
      // 守卫：lang 里没有这个事件（t() 回退为 key 字符串）就跳过
      // 这样未来只要在 lang 文件加 eventN 数据，无需改 JS 数组
      const dateVal = t(`${key}.date`);
      if (dateVal === `${key}.date`) return;

      const item = document.createElement('div');
      item.className = 'timeline-item';
      // 可选的外链（lang 里 link: { url, label }）
      const linkData = t(`${key}.link`);
      let linkHtml = '';
      if (linkData && linkData.url) {
        const label = linkData.label || 'Home';
        linkHtml = `<a class="timeline-link" href="${linkData.url}" target="_blank" rel="noopener noreferrer"><i class="fas fa-home"></i> ${label}</a>`;
      }
      item.innerHTML = `
        <div class="timeline-dot"></div>
        <span class="timeline-date">${dateVal}</span>
        <div class="timeline-content">
          <h3>${t(`${key}.title`)}</h3>
          <p>${t(`${key}.desc`)}</p>
          ${linkHtml}
        </div>
      `;
      container.appendChild(item);
    });
  }

  function initTechStack() {
    const container = qs('.skills-wrapper');
    if (!container) return;
    clear(container);

    TECH_STACK.forEach((group) => {
      const itemsHtml = group.items
        .map((s) => `<div class="skill-badge"><i class="${s.icon}"></i> ${s.name}</div>`)
        .join('');

      const col = document.createElement('div');
      col.className = 'skill-category';
      col.innerHTML = `<h3>${t(group.category)}</h3><div class="skill-list">${itemsHtml}</div>`;
      container.appendChild(col);
    });
  }

  function initContactLinks() {
    const container = qs('.intro-contact-links');
    if (!container) return;
    clear(container);

    CONTACT_LINKS.forEach((contact) => {
      const label = t(contact.key);
      const item = document.createElement('a');
      item.className = 'intro-contact-link';
      item.href = contact.link;
      item.target = '_blank';
      item.rel = 'noopener noreferrer';
      item.title = label;
      item.setAttribute('aria-label', label);
      // 优先用 text 字段（纯文字徽章），否则用 icon
      if (contact.text) {
        item.innerHTML = `<span class="contact-text">${contact.text}</span>`;
      } else {
        item.innerHTML = `<i class="${contact.icon}"></i>`;
      }
      container.appendChild(item);
    });
  }

  function initSmoothScroll() {
    qsa('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();

        const href = this.getAttribute('href');
        if (!href || href === '#') return;

        let target;
        try {
          target = qs(href);
        } catch {
          return;
        }

        if (target) {
          window.scrollTo({
            top: target.offsetTop - 80,
            behavior: 'smooth',
          });
        }
      });
    });
  }

  function initRevealMotion() {
    const targets = [
      ...qsa('.project-detail-card'),
      ...qsa('.projects-grid .card'),
      ...qsa('.opensource-grid .os-card'),
      ...qsa('.timeline-container .timeline-item'),
      ...qsa('.skills-wrapper .skill-category'),
    ];

    if (!targets.length) return;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    targets.forEach((el, index) => {
      el.classList.add('reveal');
      el.style.setProperty('--reveal-delay', `${(index % 6) * 60}ms`);
    });

    if (reducedMotion || typeof IntersectionObserver === 'undefined') {
      targets.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12,
        rootMargin: '0px 0px -8% 0px',
      },
    );

    targets.forEach((el) => observer.observe(el));
  }

  document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initLangToggle();
    initSmoothScroll();
  });

  window.addEventListener('i18nLoaded', () => {
    console.log('[main] i18n loaded, rendering content...');
    initProjects();
    initOpenSource();
    initTimeline();
    initTechStack();
    initContactLinks();
    initRevealMotion();
  });
})();
