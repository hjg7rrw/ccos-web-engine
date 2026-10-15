#!/usr/bin/env python3
"""Optional browser QA harness. Requires locally installed Playwright and Chromium.
Run: python3 tests/browser_smoke.py http://localhost:8080
No telemetry or network calls beyond the URL under test.
"""
import sys
try:from playwright.sync_api import sync_playwright
except ImportError:raise SystemExit('Playwright not installed. Install it only if you wish to run browser QA.')
url=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8080'
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    failures=[]
    for width,height in [(1366,768),(390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
        page.goto(url,wait_until='domcontentloaded')
        page.wait_for_timeout(1000)
        assert page.get_by_role('heading',level=1).count()==1
        assert page.locator('.chapter').count()==3
        assert not page.evaluate('document.documentElement.scrollWidth > window.innerWidth'),'Horizontal overflow'
        page.locator('#worlds').scroll_into_view_if_needed()
        page.get_by_role('button',name='Particle Engine').click()
        assert page.get_by_role('button',name='Particle Engine').get_attribute('aria-pressed')=='true'
        page.get_by_role('button',name='Toggle performance information').click()
        assert page.locator('#diag').is_visible()
        if errors:failures.extend(errors)
        print('Viewport QA',width,'x',height,'OK; renderer status:',page.locator('#render-status').inner_text())
        page.close()
    browser.close()
    if failures:raise RuntimeError('; '.join(failures))
print('Browser smoke completed. Run device/GPU performance profiling separately.')
