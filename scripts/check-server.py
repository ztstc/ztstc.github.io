"""Verify all critical resources are accessible via the local HTTP server."""
import urllib.request
import sys
from pathlib import Path

URLS = [
    '/index.html',
    '/assets/css/style.css',
    '/assets/css/tabs.css',
    '/assets/css/notes.css',
    '/assets/js/i18n.js',
    '/assets/js/main.js',
    '/assets/js/tabs.js',
    '/assets/js/notes.js',
    '/assets/data/notes-index.json',
    '/assets/data/projects.json',
    '/assets/vendor/marked.min.js',
    '/notes/README.md',
    '/notes/getting-started.md',
    '/notes/study/dynamic-programming.md',
    '/notes/study/git-cheatsheet.md',
    '/notes/projects/opendog-notes.md',
    '/lang/zh.json',
    '/lang/en.json',
    '/pages/projects/project1.html',
    '/pages/projects/project2.html',
]

BASE = 'http://localhost:8080'
all_ok = True
for u in URLS:
    try:
        with urllib.request.urlopen(BASE + u, timeout=5) as r:
            status = r.status
            length = r.headers.get('Content-Length', '?')
            print(f"{status} {u} ({length} bytes)")
            if status != 200:
                all_ok = False
    except Exception as e:
        print(f"ERR {u} -> {e}")
        all_ok = False

sys.exit(0 if all_ok else 1)
