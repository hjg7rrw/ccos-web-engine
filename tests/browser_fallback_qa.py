#!/usr/bin/env python3
"""QA fallback/controls using actual first-party HTML/CSS/JS in a restricted network.
Does not certify ES-module loading, HTTP routing or full WebGL performance.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os,re,sys
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text(encoding='utf8')
CSS=(ROOT/'src/styles.css').read_text(encoding='utf8')
parts=[]
for filename in ('math.js','data.js','engine.js','main.js'):
    s=(ROOT/'src'/filename).read_text(encoding='utf8')
    s=re.sub(r'^import .*?;\s*','',s,flags=re.M)
    s=re.sub(r'\bexport (?=(?:const|function|class)\b)','',s)
    parts.append(s)
HTML=HTML.replace('<link rel="stylesheet" href="./src/styles.css" />','<style>'+CSS+'</style>')
HTML=HTML.replace('<script type="module" src="./src/main.js"></script>','')
HTML=HTML.replace('</body>','<script>'+'\n'.join(parts)+'</script></body>')
VIEWPORTS=((1366,768),(768,1024),(390,844),(375,812),(320,700))
result=[]
with sync_playwright() as playwright:
    executable=os.getenv('CCOS_CHROMIUM_PATH') or None
    browser=playwright.chromium.launch(executable_path=executable,headless=True,args=[
        '--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader',
        '--use-gl=angle','--use-angle=swiftshader','--disable-gpu-sandbox'])
    for width,height in VIEWPORTS:
        page=browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content(HTML,wait_until='load')
        page.wait_for_timeout(220)
        if width==1366:page.screenshot(path=str(ROOT/'qa_preview_desktop.png'))
        if width==390:page.screenshot(path=str(ROOT/'qa_preview_mobile.png'))
        h1=page.get_by_role('heading',level=1).count()
        chapters=page.locator('.chapter').count()
        overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
        webgl2=page.evaluate('!!document.createElement("canvas").getContext("webgl2")')
        status=page.locator('#render-status').inner_text()
        page.locator('#worlds').scroll_into_view_if_needed()
        page.get_by_role('button',name='Particle Engine').click()
        selected=page.get_by_role('button',name='Particle Engine').get_attribute('aria-pressed')
        page.get_by_role('button',name='Toggle performance information').click()
        diagnostics=page.locator('#diag').is_visible()
        passed=h1==1 and chapters==3 and not overflow and selected=='true' and diagnostics and not errors
        result.append({'viewport':f'{width}x{height}','passed':bool(passed),
                       'horizontal_overflow':bool(overflow),'webgl2_available':bool(webgl2),
                       'status':status,'errors':errors})
        page.close()
    browser.close()
print(json.dumps(result,indent=2))
if not all(item['passed'] for item in result):sys.exit('Fallback browser QA failed')
print('PASS: Layout, semantics, controls and fallback. WebGL2 rendering remains unverified.')
