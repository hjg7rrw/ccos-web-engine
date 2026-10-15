#!/usr/bin/env python3
"""Low-impact public-page inspection. No authentication, bypass, crawling, or harvesting.
Usage: python3 scripts/public_site_audit.py https://example.com --output audit-output/site.json
"""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from urllib.parse import urljoin,urlparse
from urllib.request import Request,urlopen
MAX_READ=2_000_000
class PublicPageParser(HTMLParser):
    def __init__(self):
        super().__init__();self.meta=[];self.scripts=[];self.styles=[];self.links=[];self.images=[];self.title='';self._title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self._title=True
        if tag=='meta':self.meta.append({k:v for k,v in a.items() if k in ('name','property','content')})
        if tag=='script':self.scripts.append({'src':a.get('src'),'type':a.get('type')})
        if tag=='link':self.styles.append({'rel':a.get('rel'),'href':a.get('href')})
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='img':self.images.append({'alt':a.get('alt'),'src':a.get('src')})
    def handle_data(self,data):
        if self._title:self.title+=data
    def handle_endtag(self,tag):
        if tag=='title':self._title=False
def inspect(url,timeout=15):
    p=urlparse(url)
    if p.scheme not in ('https','http') or not p.netloc or p.username or p.password:
        raise ValueError('Please provide a standard public HTTP(S) URL without credentials')
    req=Request(url,headers={'User-Agent':'CCOS-PublicWebsiteStudy/0.1 (+educational contact through operator)','Accept':'text/html'})
    start=time.monotonic()
    with urlopen(req,timeout=timeout) as response:
        content_type=response.headers.get('Content-Type','')
        if 'text/html' not in content_type:raise ValueError('Page is not HTML; received '+content_type)
        data=response.read(MAX_READ+1)
        if len(data)>MAX_READ:raise ValueError('HTML exceeded study limit (2 MB)')
        final_url=response.url;status=response.status
    tree=PublicPageParser();tree.feed(data.decode('utf-8',errors='replace'))
    origins=sorted({urlparse(urljoin(final_url,x)).netloc for x in tree.links+[s.get('src') for s in tree.scripts if s.get('src')] if x})
    return {'url_requested':url,'url_resolved':final_url,'http_status':status,'html_bytes':len(data),'fetch_seconds':round(time.monotonic()-start,3),'title':tree.title.strip(),
      'meta':tree.meta[:50],'script_references':tree.scripts[:60],'stylesheet_references':tree.styles[:60],
      'image_count':len(tree.images),'image_alt_missing_count':sum(not x['alt'] for x in tree.images),
      'anchor_count':len(tree.links),'referenced_hosts':origins[:50],
      'limitations':['HTML inspection does not establish source architecture, ownership, runtime performance, licenses, or shader implementation.',
        'A blocked request is not bypassed. Browser-visible behavior needs separate manual testing.']}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('url');parser.add_argument('--output',default='audit-output/site.json');a=parser.parse_args()
    try:result=inspect(a.url)
    except Exception as e:result={'url_requested':a.url,'status':'BLOCKED_OR_UNAVAILABLE','message':str(e),'note':'Do not bypass access controls or infer implementation from failure.'}
    dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({'report':str(dest),'status':result.get('status',result.get('http_status'))},indent=2))
if __name__=='__main__':main()
