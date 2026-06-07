"""Check the actual font file sizes from the chosen CDNs."""
import re
import urllib.request

def fetch(url, timeout=8):
    return urllib.request.urlopen(url, timeout=timeout).read().decode('utf-8')

def head_size(url, timeout=8):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return int(r.headers.get('Content-Length', 0))

# 1. LXGW WenKai Screen on BootCDN
css = fetch("https://cdn.bootcdn.net/ajax/libs/lxgw-wenkai-screen-webfont/1.7.0/style.css")
print("=== LXGW WenKai Screen (BootCDN) ===")
for m in re.finditer(r"@import url\(['\"]?([^'\")]+)['\"]?\)", css):
    rel = m.group(1)
    abs_url = "https://cdn.bootcdn.net/ajax/libs/lxgw-wenkai-screen-webfont/1.7.0/" + rel
    size = head_size(abs_url)
    print(f"  {rel:35s}  {size/1024:>7.1f} KB")

print()

# 2. JetBrains Mono on jsDelivr
jbm_css = fetch("https://cdn.jsdelivr.net/npm/@fontsource/jetbrains-mono@5.0.20/index.css")
print("=== JetBrains Mono (jsDelivr) ===")
weights_found = re.findall(r"font-weight:\s*(\d+)", jbm_css)
print(f"  weights declared: {sorted(set(weights_found))}")
# Try a few common font files
for w in ['400', '500', '700']:
    url = f"https://cdn.jsdelivr.net/npm/@fontsource/jetbrains-mono@5.0.20/files/jetbrains-mono-latin-{w}-normal.woff2"
    try:
        size = head_size(url)
        print(f"  weight {w}: {size/1024:.1f} KB")
    except Exception as e:
        print(f"  weight {w}: ERR {e}")
