#!/usr/bin/env python3
"""Publish the complete adjacent CCOS_WebGL2_Lab_v0.1.3 source archive to a NEW isolated Git branch.
The default action is a dry-run. --execute requires the operator's existing Git authentication.
It never rewrites main/master or edits the existing Jarvis working folder.
"""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ALLOWED={'README.md','index.html','package.json','requirements-webgl2.txt',
 'run_local.bat','run_local.sh','run_webgl2_qa.sh','.gitignore',
 'src','scripts','tests','ops','docs','skills','qa-webgl2','audit-output'}
PRIVATE={'.env','.env.local','credentials.json','secrets.json','id_rsa',
 'id_ed25519','token.txt','settings.local.json'}
SKIP_PARTS={'__pycache__','.venv','.git','node_modules'}
SKIP_SUFFIX={'.pyc','.pem','.key','.p12','.pfx'}

def source_files(source):
    for name in sorted(ALLOWED):
        p=source/name
        if not p.exists():continue
        for file in (p.rglob('*') if p.is_dir() else [p]):
            if not file.is_file() or file.is_symlink():continue
            rel=file.relative_to(source)
            if any(x in SKIP_PARTS for x in rel.parts):continue
            if file.name in PRIVATE or file.suffix.lower() in SKIP_SUFFIX:continue
            yield rel,file

def git(cwd,*args):
    return subprocess.run(['git','-C',str(cwd),*args],
      capture_output=True,text=True,check=True).stdout.strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True,help='Unpacked complete CCOS_WebGL2_Lab_v0.1.3 folder')
    ap.add_argument('--repo-url',default='https://github.com/hjg7rrw/JARVIS-.git')
    ap.add_argument('--branch',default='ccos/webgl2-complete-v0.1.3')
    ap.add_argument('--base',default='master')
    ap.add_argument('--execute',action='store_true')
    cfg=ap.parse_args()
    root=Path(cfg.source).resolve()
    found=list(source_files(root))
    if not found:raise SystemExit('No acceptable source files at supplied directory')
    print(f"Plan: {len(found)} files from {root}")
    for rel,_ in found:print(' +',rel)
    if not cfg.execute:
        print('DRY RUN: no Git repository or remote has been modified')
        return
    if not shutil.which('git'):raise SystemExit('Git missing')
    with tempfile.TemporaryDirectory(prefix='ccos-webgl2-') as folder:
        repo=Path(folder)/'repo'
        subprocess.run(['git','clone','--depth','1','--branch',cfg.base,cfg.repo_url,
                        str(repo)],check=True,timeout=180)
        git(repo,'switch','-c',cfg.branch)
        target=repo/'CCOS'/'webgl2-lab'/'v0.1.3'/'full-release'
        if target.exists():raise SystemExit('Destination exists; refusal to overwrite')
        for rel,source in found:
            path=target/rel
            path.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,path)
        git(repo,'add','--','CCOS/webgl2-lab/v0.1.3/full-release')
        git(repo,'commit','-m','Add full CCOS WebGL2 v0.1.3 original source and evidence')
        git(repo,'push','--set-upstream','origin',cfg.branch)
        print('Uploaded isolated branch; default branch unchanged')

if __name__=='__main__':main()
