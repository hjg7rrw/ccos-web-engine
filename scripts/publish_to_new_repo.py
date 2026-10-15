#!/usr/bin/env python3
"""HISTORICAL private-only Git publisher retained for regression testing.

This was created before the user explicitly authorized uploads to a public
ccos-web-engine repository. Its PRIVATE gate is intentionally preserved as
historical evidence; do not use it for current remote publishing.

DRY RUN: python3 scripts/publish_to_new_repo.py
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
REPO = 'hjg7rrw/ccos-web-engine'
REMOTE = 'https://github.com/' + REPO + '.git'
DEFAULT_BUNDLE = HERE.parent / 'CCOS_Web_Engine_v0.1.4_private_release.bundle'
def run(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=180)
    if proc.returncode:
        raise RuntimeError(f'Command failed at {cmd[0]} {cmd[1] if len(cmd)>1 else ""} (exit {proc.returncode}); inspect local authorization/network status')
    return proc.stdout.strip()
def private_gate() -> bool:
    if not shutil.which('gh'):return False
    try:state=run(['gh','repo','view',REPO,'--json','visibility','--jq','.visibility'])
    except (RuntimeError,subprocess.TimeoutExpired):return False
    return state.strip().upper()=='PRIVATE'
def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true')
    p.add_argument('--bundle',type=Path,default=DEFAULT_BUNDLE)
    a=p.parse_args()
    print('Target:',REPO)
    print('Mode:','PUBLICATION REQUESTED' if a.execute else 'DRY RUN - NO REMOTE ACTION')
    print('Release source:',a.bundle)
    if not a.execute:
        print('No publication attempted. Historical precondition: private repo.')
        return 0
    if not a.bundle.is_file():
        print('BLOCKED: Git history bundle is missing.');return 2
    if not shutil.which('git'):
        print('BLOCKED: git executable missing.');return 2
    if not private_gate():
        print('BLOCKED: repository PRIVATE visibility cannot be authenticated; no upload performed.');return 3
    with tempfile.TemporaryDirectory(prefix='ccos-safe-release-') as d:
        target=Path(d)/'source'
        run(['git','clone','--branch','main','--single-branch',str(a.bundle.resolve()),str(target)])
        run(['git','remote','set-url','origin',REMOTE],target)
        if run(['git','ls-remote','--heads','origin','main'],target):
            print('BLOCKED: remote main already exists.');return 4
        if not private_gate():
            print('BLOCKED: privacy changed during preparation.');return 3
        run(['git','push','origin','main:refs/heads/main'],target)
        print('Published to',REPO)
        return 0
if __name__=='__main__':raise SystemExit(main())
