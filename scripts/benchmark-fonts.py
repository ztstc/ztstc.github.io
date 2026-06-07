"""Benchmark CDN latency for Chinese fonts likely to be used in the wiki.

Tests each (CDN, font URL) pair by:
  1. Doing a HEAD request to measure connect+TLS time
  2. Doing a small GET (1 KB range) to measure TTFB
  3. Reporting time and HTTP status

Test scope:
  - Google Fonts (likely blocked in mainland China)
  - jsDelivr (popular for npm packages)
  - BootCDN (already used for Font Awesome)
  - chinese-fonts-cdn (community CDN for Noto fonts)
  - loli (lolicdn) - fast Chinese open source CDN
  - Staticfile (Qihoo 360)
"""
import time
import urllib.request
import ssl
import socket
from concurrent.futures import ThreadPoolExecutor

CANDIDATES = [
    # === Google Fonts (baseline) ===
    ("Google Fonts - Noto Serif SC CSS",
     "https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap"),

    # === jsDelivr ===
    ("jsDelivr - fontsource Noto Serif SC",
     "https://cdn.jsdelivr.net/npm/@fontsource/noto-serif-sc@5.0.5/index.css"),
    ("jsDelivr - fontsource LXGW WenKai",
     "https://cdn.jsdelivr.net/npm/lxgw-wenkai-screen-webfont@1.7.0/style.css"),
    ("jsDelivr - fontsource LXGW WenKai TC",
     "https://cdn.jsdelivr.net/npm/lxgw-wenkai-tc-webfont@1.0.0/style.css"),
    ("jsDelivr - fontsource JetBrains Mono",
     "https://cdn.jsdelivr.net/npm/@fontsource/jetbrains-mono@5.0.20/index.css"),

    # === BootCDN (we already use this) ===
    ("BootCDN - Noto Serif SC",
     "https://cdn.bootcdn.net/ajax/libs/noto-serif-sc/1.0.0/noto-serif-sc.css"),
    ("BootCDN - LXGW WenKai",
     "https://cdn.bootcdn.net/ajax/libs/lxgw-wenkai-screen-webfont/1.7.0/style.css"),
    ("BootCDN - JetBrains Mono",
     "https://cdn.bootcdn.net/ajax/libs/jetbrains-mono/2.304/web/jetbrains-mono.css"),

    # === chinese-fonts-cdn (community) ===
    ("chinese-fonts-cdn - Noto Serif SC",
     "https://chinese-fonts-cdn.deno.dev/packages/noto-serif-sc/dist/NotoSerifSC/result.css"),
    ("chinese-fonts-cdn - LXGW WenKai",
     "https://chinese-fonts-cdn.deno.dev/packages/lxgwwenkai/dist/LXGWWenKai-Regular/result.css"),

    # === Staticfile (Qihoo 360) ===
    ("Staticfile - LXGW WenKai",
     "https://cdn.staticfile.org/lxgw-wenkai-screen-webfont/1.7.0/style.css"),

    # === lolicdn ===
    ("lolicdn - LXGW WenKai",
     "https://fonts.loli.net/"),
]

# Bypass SSL verification noise
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def bench(name, url, timeout=8):
    print(f"\n>>> {name}")
    print(f"    URL: {url}")
    out = {"name": name, "url": url, "connect": None, "ttfb": None, "status": None, "error": None}
    # Measure DNS + TCP + TLS + first byte
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, method="GET", headers={"Range": "bytes=0-1024", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            ttfb = (time.perf_counter() - t0) * 1000
            out["ttfb"] = ttfb
            out["status"] = r.status
            try:
                _ = r.read(1024)
            except Exception:
                pass
            total = (time.perf_counter() - t0) * 1000
            out["total"] = total
            print(f"    status={r.status}  TTFB={ttfb:.0f}ms  total={total:.0f}ms")
    except Exception as e:
        out["error"] = str(e)
        print(f"    ERROR: {e}")
    return out

def main():
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(bench, n, u): (n, u) for n, u in CANDIDATES}
        for f in futs:
            results.append(f.result())

    print("\n" + "=" * 70)
    print("SUMMARY (sorted by TTFB, errors last)")
    print("=" * 70)
    valid = [r for r in results if r["status"]]
    invalid = [r for r in results if not r["status"]]
    valid.sort(key=lambda r: r["ttfb"] or 1e9)
    for r in valid:
        marker = "  OK" if r["ttfb"] < 500 else ("  SLOW" if r["ttfb"] < 1500 else "  VERY SLOW")
        print(f"{marker:>10}  {r['ttfb']:>7.0f}ms  {r['name']}")
    for r in invalid:
        print(f"   FAIL          {r['name']}: {r['error']}")

if __name__ == "__main__":
    main()
