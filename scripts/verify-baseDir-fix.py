"""End-to-end test of baseDir fix using Playwright in a fresh browser context."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # 新建一个干净的 context (没缓存)
        context = await browser.new_context()
        page = await context.new_page()
        # 收集 console 错误
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))
        page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}") if msg.type in ('error', 'warning') else None)

        await page.goto('http://localhost:8080/?_=e2etest1#notes?path=study%2Ffpga.md', wait_until='networkidle')
        await page.wait_for_timeout(2500)

        result = await page.evaluate("""() => {
          const viewer = document.querySelector('.notes-content');
          const h1 = viewer?.querySelector('h1')?.textContent;
          const imgs = Array.from(viewer?.querySelectorAll('img') || []);
          const total = imgs.length;
          const loaded = imgs.filter(i => i.complete && i.naturalWidth > 0).length;
          const sample = imgs.slice(0, 5).map(i => i.getAttribute('src'));
          return { h1, total, loaded, broken: total - loaded, sample };
        }""")
        print("RESULT:", result)
        await page.screenshot(path='scripts/verify-baseDir-fix.png', full_page=False)
        await browser.close()

asyncio.run(main())
