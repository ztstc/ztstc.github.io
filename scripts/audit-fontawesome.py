"""Audit FA icons in main.js. Two strategies: regex + runtime DOM check."""
import re
import urllib.request
from pathlib import Path

FA_CSS_URL = 'https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css'
CACHE = Path('assets/fa-css-cache.min.css')

def get_fa_css():
    if CACHE.exists():
        return CACHE.read_text(encoding='utf-8')
    print('Fetching FA 6 CSS from BootCDN...')
    req = urllib.request.Request(FA_CSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    css = urllib.request.urlopen(req, timeout=15).read().decode('utf-8')
    CACHE.write_text(css, encoding='utf-8')
    return css

def extract_defined_icons(css):
    """Match `.fa-XXX:before{content:"\YYY"}` and `.fa-XXX,` selector lists."""
    icons = set()
    # Match .fa-XXX:before{content:"\YYY"}
    for m in re.finditer(r"\.fa-([\w-]+):before\{content:\"\\([0-9a-fA-F]+)\"\}", css):
        icons.add(m.group(1))
    # Match alias list: .fa-torah:before,.fa-scroll-torah:before{content:"\f6a0"}
    for m in re.finditer(r"\.fa-([\w-]+)(?=:[^{]*\{content:)", css):
        icons.add(m.group(1))
    return icons

def collect_used_icons(main_js_path):
    src = Path(main_js_path).read_text(encoding='utf-8')
    pattern = re.compile(r"['\"](?P<prefix>fa[bsr])\s+fa-(?P<name>[\w-]+)['\"]")
    used = []
    for m in pattern.finditer(src):
        used.append((m.group('prefix'), m.group('name'), m.group(0)))
    return used

def main():
    css = get_fa_css()
    defined = extract_defined_icons(css)
    print(f"FA 6 CSS defines {len(defined)} unique icon names")

    used = collect_used_icons('assets/js/main.js')
    print(f"=== {len(used)} refs in main.js ===\n")

    seen = set()
    missing = []
    ok = 0
    for prefix, name, full in used:
        key = (prefix, name)
        if key in seen: continue
        seen.add(key)
        if name in defined:
            ok += 1
        else:
            missing.append(f"{prefix} fa-{name}   {full}")

    print(f"Result: {ok} OK, {len(missing)} invalid\n")
    if missing:
        print("INVALID icons (these won't render):")
        for m in missing:
            print(f"  {m}")

if __name__ == '__main__':
    main()
