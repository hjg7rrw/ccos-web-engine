#!/usr/bin/env python3
"""CCOS WebGL2 independent capability probe.
Runs only locally generated trusted HTML. Logs every success/failure as JSON.
Requires Python Playwright + Chromium; headed mode requires a display.
"""
import argparse
import json
import os
import platform
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MODES = ["headless-default", "headless-swiftshader",
         "headed-default", "headed-swiftshader", "headed-mesa"]
BASE = ["--disable-dev-shm-usage"]
ENABLE = ["--enable-webgl", "--ignore-gpu-blocklist"]
SWIFT = ENABLE + ["--enable-unsafe-swiftshader",
                  "--use-gl=angle", "--use-angle=swiftshader"]
MESA = ENABLE + ["--enable-unsafe-swiftshader",
                 "--use-gl=angle", "--use-angle=gl"]

# Verify GLSL ES 3.00 shaders, an actual triangle draw, and framebuffer pixels.
FIXTURE = r'''<!doctype html><canvas id="c" width="128" height="128"></canvas>
<script>
function probe(){
 const gl=document.querySelector('#c').getContext('webgl2',
                        {preserveDrawingBuffer:true,alpha:false});
 if(!gl)return {webgl2:false,draw_verified:false,error:'WebGL2 null'};
 const ext=gl.getExtension('WEBGL_debug_renderer_info');
 const result={webgl2:true,version:gl.getParameter(gl.VERSION),
   renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):'not exposed'};
 const shader=(kind,code)=>{
   let s=gl.createShader(kind);gl.shaderSource(s,code);gl.compileShader(s);
   if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))
     throw Error('compile: '+gl.getShaderInfoLog(s));return s;
 };
 try {
  const vs=shader(gl.VERTEX_SHADER,
    '#version 300 es\nvoid main(){vec2 p[3]=vec2[3](vec2(-1.,-1.),vec2(3.,-1.),vec2(-1.,3.));gl_Position=vec4(p[gl_VertexID],0.,1.);}');
  const fs=shader(gl.FRAGMENT_SHADER,
    '#version 300 es\nprecision highp float;out vec4 c;void main(){c=vec4(.16,.73,.46,1.);}');
  const pr=gl.createProgram();gl.attachShader(pr,vs);gl.attachShader(pr,fs);
  gl.linkProgram(pr);
  if(!gl.getProgramParameter(pr,gl.LINK_STATUS))
    throw Error('link: '+gl.getProgramInfoLog(pr));
  gl.useProgram(pr);gl.bindVertexArray(gl.createVertexArray());
  gl.viewport(0,0,128,128);gl.drawArrays(gl.TRIANGLES,0,3);gl.finish();
  const px=new Uint8Array(4);
  gl.readPixels(64,64,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);
  const err=gl.getError();result.pixel=Array.from(px);result.gl_error=err;
  result.draw_verified=err===0&&px[0]>20&&px[1]>110&&px[2]>50&&px[3]===255;
  return result;
 }catch(e){return {...result,draw_verified:false,error:String(e)};}
}
</script>'''

def chrome_path(configured):
    if configured:
        return configured
    for binary in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        found=shutil.which(binary)
        if found:
            return found
    return None

def run(browser_driver, name, binary):
    headed=name.startswith("headed")
    flags=BASE.copy()
    if name.endswith("swiftshader"):
        flags+=SWIFT
    elif name.endswith("mesa"):
        flags+=MESA
    result={"mode":name,"headed":headed,"flags":flags,
            "display":os.getenv("DISPLAY"),"passed":False}
    browser=None
    start=time.monotonic()
    try:
        opts={"headless":not headed,"args":flags,"timeout":15000}
        if binary:
            opts["executable_path"]=binary
        browser=browser_driver.launch(**opts)
        page=browser.new_page()
        errors=[]
        page.on("pageerror",lambda ex:errors.append(str(ex)))
        page.set_content(FIXTURE,wait_until="load",timeout=12000)
        data=page.evaluate("probe()")
        result.update(data)
        result["js_errors"]=errors
        result["passed"]=bool(data.get("draw_verified") and not errors)
        page.close()
    except Exception as ex:
        result["error"]=f"{type(ex).__name__}: {str(ex)[:500]}"
    finally:
        if browser:
            try:browser.close()
            except Exception:pass
    result["seconds"]=round(time.monotonic()-start,2)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--modes",default=",".join(MODES))
    parser.add_argument("--chromium")
    parser.add_argument("--output",default="qa/observed_matrix.json")
    parser.add_argument("--require-one",action="store_true")
    args=parser.parse_args()
    modes=[name.strip() for name in args.modes.split(",") if name.strip()]
    if any(name not in MODES for name in modes):
        parser.error(f"Modes allowed: {MODES}")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        parser.error("Playwright missing: python3 -m pip install playwright")
    binary=chrome_path(args.chromium)
    record={
        "lab_version":"CCOS-WEBGL2-v0.1.3",
        "utc":datetime.now(timezone.utc).isoformat(),
        "environment":{"os":platform.platform(),"python":platform.python_version(),
                       "display":os.getenv("DISPLAY"),
                       "chromium":binary or "Playwright bundled"},
        "security":"Only trusted, internally generated HTML; not for arbitrary browsing.",
        "probes":[]
    }
    with sync_playwright() as playwright:
        for name in modes:
            outcome=run(playwright.chromium,name,binary)
            record["probes"].append(outcome)
            print(name,"PASS" if outcome["passed"] else "FAIL",
                  str(outcome.get("renderer",outcome.get("error","")))[:140],flush=True)
    record["passed_any"]=any(i["passed"] for i in record["probes"])
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print("Results:",out)
    return 1 if args.require_one and not record["passed_any"] else 0

if __name__=="__main__":
    sys.exit(main())
