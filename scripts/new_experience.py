#!/usr/bin/env python3
"""Generate a separate original starter website from the reusable CCOS engine.
Does not mutate source studio canon or connect to any external repository.
Example:
 python3 scripts/new_experience.py --name "Orbit Atelier" --accent '#e6b870' --dest ../orbit-atelier
"""
from __future__ import annotations
import argparse,html,re,shutil
from pathlib import Path
TEMPLATE=Path(__file__).resolve().parent.parent

def create(name:str,accent:str,dest:Path):
    if not name.strip() or len(name)>60:raise ValueError('Name must contain 1–60 characters')
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',accent):raise ValueError('Accent must be a six-digit hex color')
    if dest.exists():raise FileExistsError('Target already exists; refusing to overwrite')
    safe=html.escape(name.strip(),quote=True)
    dest.mkdir(parents=True)
    for relative in ['index.html','package.json','.gitignore','src/styles.css','src/math.js','src/engine.js','src/data.js','src/main.js']:
        target=dest/relative;target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(TEMPLATE/relative,target)
    document=(dest/'index.html').read_text()
    document=document.replace('CCOS / An Interactive World Engine',safe+' / An Interactive World')
    document=document.replace('CCOS<span class="wordmark-end">/LAB</span>',safe+'<span class="wordmark-end">/LAB</span>')
    document=document.replace('ORIGINAL CCOS INTERACTIVE EXPERIENCE','ORIGINAL '+safe.upper()+' INTERACTIVE EXPERIENCE')
    (dest/'index.html').write_text(document)
    styles=(dest/'src/styles.css').read_text().replace('--teal:#8be5df;',f'--teal:{accent};')
    styles=styles.replace('box-shadow:0 0 17px #8be5df',f'box-shadow:0 0 17px {accent}')
    (dest/'src/styles.css').write_text(styles)
    (dest/'README.md').write_text(f'# {name}\n\nIndependent original derivative of the privately owned CCOS Web Engine starter.\n\nLaunch with `python3 -m http.server 8080` from this folder.\n\nEdit text/content/geometry before release, review asset rights, and run tests.\n')
    return dest

def main():
    p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--accent',default='#8be5df');p.add_argument('--dest',type=Path,required=True);args=p.parse_args()
    print('Created:',create(args.name,args.accent,args.dest.resolve()))
if __name__=='__main__':main()
