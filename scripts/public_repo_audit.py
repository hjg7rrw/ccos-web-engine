#!/usr/bin/env python3
"""Read-only public GitHub repository metadata and license triage.
Usage: python3 scripts/public_repo_audit.py --output audit-output/repos.json
May use GITHUB_TOKEN from environment; never records the token.
"""
import argparse,json,os,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
REPOS=['mrdoob/three.js','pmndrs/react-three-fiber','pmndrs/drei','greensock/GSAP','Jada-Q/igloo-mirror','LAYTAT/igloo-reverse-engineering','qusay4421/igloo-site','cortiz2894/hologram-particles','TranHuuDat2004/threejs-gsap-scroller']

def inspect(name):
    if name.count('/')!=1 or '..' in name:raise ValueError('Invalid GitHub owner/repo')
    headers={'User-Agent':'CCOS-PublicRepositoryStudy/0.1','Accept':'application/vnd.github+json'}
    if os.getenv('GITHUB_TOKEN'):headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urlopen(Request('https://api.github.com/repos/'+name,headers=headers),timeout=13) as r:obj=json.load(r)
    lic=obj.get('license') or {};spdx=lic.get('spdx_id')
    return {'name':obj.get('full_name'),'url':obj.get('html_url'),'archived':obj.get('archived'),
      'license_expression_reported':spdx or 'NONE','stars':obj.get('stargazers_count'),
      'updated_at':obj.get('updated_at'),
      'reuse_gate':'CANDIDATE_REVIEW_LICENSE_AND_DEPS' if spdx and spdx not in ('NOASSERTION','NONE') else 'STUDY_ONLY_NO_EXPLICIT_LICENSE',
      'warning':'Repository-level license does not automatically cover models, fonts, images, music, or nested dependencies.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='audit-output/repos.json');p.add_argument('--repo',action='append',default=[]);a=p.parse_args();rows=[]
    for n in (a.repo or REPOS):
        try:rows.append(inspect(n))
        except (HTTPError,URLError,ValueError,TimeoutError) as e:rows.append({'name':n,'status':'UNVERIFIED','error':str(e)})
        time.sleep(.2)
    dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(rows,indent=2),encoding='utf-8');print(f'Inspected {len(rows)} repositories; saved to {dest}')
if __name__=='__main__':main()
