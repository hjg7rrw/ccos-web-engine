#!/usr/bin/env python3
"""CCOS v0.1.4 complete archived release uploader. Dry-run unless --execute.

Stages original 73 files and the Git-history bundle under archive/v0.1.4 on
a NEW review branch, never modifying main or Jarvis. Uses preexisting Git auth.
"""
import argparse,re,shutil,subprocess,tempfile,zipfile
from pathlib import Path,PurePosixPath
REPO='https://github.com/hjg7rrw/ccos-web-engine.git'
BRANCH='ccos/full-archive-v0.1.4'
PREFIX='ccos-web-engine/'
DENY={'.env','.env.local','credentials.json','secrets.json','token.txt','id_rsa','id_ed25519'}
PATTERNS=[re.compile(x,re.I) for x in [
 r'-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----',
 r'gh[pousr]_[A-Za-z0-9_]{20,}',r'sk-(?:proj-)?[A-Za-z0-9\-_]{30,}',r'AKIA[0-9A-Z]{16}'
]]
def command(*args,cwd=None):
    p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=180)
    if p.returncode:
        raise RuntimeError(f'{args[0]} {args[1] if len(args)>1 else ""} failed (exit {p.returncode}); check Git/network auth locally')
    return p.stdout.strip()
def validate(source):
    with zipfile.ZipFile(source) as archive:
        originals=[]
        for info in archive.infolist():
            if info.is_dir():continue
            path=PurePosixPath(info.filename)
            if not str(path).startswith(PREFIX):
                if path.name=='CCOS_Web_Engine_v0.1.4_private_release.bundle' and len(path.parts)==1:
                    originals.append((info,PurePosixPath('archive/v0.1.4/git-history.bundle')))
                continue
            rel=PurePosixPath(*path.parts[1:])
            if not rel.parts or '..' in rel.parts or path.is_absolute():raise ValueError('Unsafe ZIP path')
            if rel.name.lower() in DENY or rel.suffix.lower() in ('.key','.pem','.pfx'):
                raise ValueError('Sensitive file name: '+str(rel))
            if info.external_attr >> 16 & 0o170000 == 0o120000:
                raise ValueError('Symlink rejected: '+str(rel))
            if info.file_size>20_000_000:raise ValueError('Oversized file: '+str(rel))
            if rel.suffix.lower() not in ('.png','.gif','.jpg','.jpeg','.webp','.bundle'):
                try: s=archive.read(info).decode('utf-8')
                except UnicodeDecodeError:raise ValueError('Unknown binary: '+str(rel))
                if any(p.search(s) for p in PATTERNS):
                    raise ValueError('Possible credential content: '+str(rel))
            originals.append((info,PurePosixPath('archive/v0.1.4')/rel))
        count=sum(str(i.filename).startswith(PREFIX) for i,p in originals)
        if count<70:raise ValueError(f'Expected >=70 source files, found {count}')
        return originals
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--zip',type=Path,required=True)
    p.add_argument('--execute',action='store_true')
    args=p.parse_args();source=args.zip.resolve()
    if not source.is_file():raise SystemExit('ZIP not found: '+str(source))
    files=validate(source)
    print('Repository:',REPO,'\nReview branch:',BRANCH)
    print('Validated archive entries:',len(files))
    print('Upload mode:','EXECUTE' if args.execute else 'DRY RUN: no network or Git changes')
    if not args.execute:return
    if not shutil.which('git'):raise SystemExit('Git executable required')
    with tempfile.TemporaryDirectory(prefix='ccos-archive-import-') as folder:
        target=Path(folder)/'repo'
        command('git','clone','--depth','1','--branch','main',REPO,str(target))
        if command('git','ls-remote','--heads','origin',BRANCH,cwd=target):
            raise RuntimeError('Review branch already exists. Refusing overwrite.')
        command('git','checkout','-b',BRANCH,cwd=target)
        with zipfile.ZipFile(source) as archive:
            for info,destination in files:
                out=target.joinpath(*destination.parts)
                out.parent.mkdir(parents=True,exist_ok=True)
                out.write_bytes(archive.read(info))
        command('git','add','--','archive/v0.1.4',cwd=target)
        command('git','commit','-m','archive: preserve original complete CCOS v0.1.4 release and Git history',cwd=target)
        command('git','push','--set-upstream','origin',BRANCH,cwd=target)
    print('Published review branch; compare remote inventory before merging.')
if __name__=='__main__':main()
