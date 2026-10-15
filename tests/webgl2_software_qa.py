#!/usr/bin/env python3
"""Actual CCOS WebGL2 GPU-shader drawing on isolated Xvfb software graphics.
Uses local first-party files combined only to work around restricted HTTP navigation.
Does NOT prove standard ES module imports or production routing.
"""
from pathlib import Path
import json, re, sys, os
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT/'qa-webgl2'
ARTIFACTS.mkdir(exist_ok=True)
html=(ROOT/'index.html').read_text(encoding='utf-8')
css=(ROOT/'src/styles.css').read_text(encoding='utf-8')
parts=[]
for filename in ('math.js','data.js','engine.js','main.js'):
    code=(ROOT/'src'/filename).read_text(encoding='utf-8')
    code=re.sub(r'^import .*?;\s*','',code,flags=re.M)
    code=re.sub(r'\bexport (?=(?:const|function|class)\b)','',code)
    parts.append(code)
html=html.replace('<link rel="stylesheet" href="./src/styles.css" />','<style>'+css+'</style>')
html=html.replace('<script type="module" src="./src/main.js"></script>','')
html=html.replace('</body>','<script>'+'\n'.join(parts)+'</script></body>')
result={'environment':{'display':os.environ.get('DISPLAY'),'egl_platform':os.environ.get('EGL_PLATFORM',''),'renderer':'ANGLE SwiftShader software backend','physical_gpu':False},'viewport_tests':[]}
with sync_playwright() as p:
    chromium=p.chromium.launch(executable_path=os.getenv('CCOS_CHROMIUM_PATH','/usr/bin/chromium'),headless=False,args=[
        '--disable-dev-shm-usage','--enable-webgl','--enable-unsafe-swiftshader',
        '--ignore-gpu-blocklist','--use-gl=angle','--use-angle=swiftshader'])
    for width,height in ((1366,768),(390,844)):
        page=chromium.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.set_content(html,wait_until='load')
        page.wait_for_timeout(1800)
        info=page.evaluate('''async () => {
            await new Promise(resolve=>requestAnimationFrame(resolve));
            const canvas=document.querySelector('#universe');
            const gl=canvas.getContext('webgl2');
            if(!gl)return {webgl2:false,status:document.querySelector('#render-status').textContent};
            const ext=gl.getExtension('WEBGL_debug_renderer_info');
            const w=canvas.width,h=canvas.height;
            let sample=[];
            for(let i=0;i<12;i++){
               const x=Math.floor(w*(.12+.76*((i%4)/3))),y=Math.floor(h*(.17+.66*Math.floor(i/4)/2));
               const p=new Uint8Array(4);gl.readPixels(x,y,1,1,gl.RGBA,gl.UNSIGNED_BYTE,p);sample.push(Array.from(p));
            }
            return {webgl2:true,status:document.querySelector('#render-status').textContent,
             version:gl.getParameter(gl.VERSION),renderer:ext&&gl.getParameter(ext.UNMASKED_RENDERER_WEBGL),
             canvas:[w,h],pixel_samples:sample,gl_error:gl.getError(),
             document_overflow:document.documentElement.scrollWidth>innerWidth};
        }''')
        page.screenshot(path=str(ARTIFACTS/f'webgl2_{width}x{height}_initial.png'))
        page.locator('#worlds').scroll_into_view_if_needed(timeout=5000)
        page.get_by_role('button',name='Particle Engine').click()
        page.wait_for_timeout(1750)
        selected=page.get_by_role('button',name='Particle Engine').get_attribute('aria-pressed')
        page.get_by_role('button',name='Toggle performance information').click()
        diag=page.locator('#diag').is_visible()
        metrics={k:page.locator('#diag-'+k).inner_text() for k in ('renderer','particles','fps','dpr','shape')}
        page.screenshot(path=str(ARTIFACTS/f'webgl2_{width}x{height}_interactive.png'))
        info.update({'viewport':f'{width}x{height}','particle_button_active':selected=='true','diagnostics_visible':diag,'metrics':metrics,'javascript_errors':errors})
        unique_pixels=len({tuple(x) for x in info.get('pixel_samples',[])})
        info['pixel_colors_distinct']=unique_pixels
        info['passed']=bool(info.get('webgl2') and info.get('status','').startswith('WEBGL2 ONLINE') and unique_pixels>=3 and info.get('gl_error')==0 and not info.get('document_overflow') and selected=='true' and diag and metrics['renderer']=='WebGL2' and metrics['shape']=='HELIX' and not errors)
        result['viewport_tests'].append(info)
        print(info['viewport'],'PASS' if info['passed'] else 'FAIL','colors',unique_pixels,'status',info.get('status'),'fps',metrics['fps'],flush=True)
        page.close()
    chromium.close()
(ARTIFACTS/'webgl2_qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if not all(t['passed'] for t in result['viewport_tests']):
    print(json.dumps(result,indent=2));sys.exit(1)
print('PASS: genuine WebGL2 shaders and point rendering in Xvfb/SwiftShader; not physical-device benchmark.')
