#!/usr/bin/env python3
"""校验 52 条 KU 是否都有对应 Tier A 全文，且摘录候选来自该全文。"""
import re,sys,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
plan=(ROOT/'docs/research/ku-plan.md').read_text(encoding='utf-8')
rows=re.findall(r'^\| \d+ \| (gsk-[a-z0-9-]+) \| (.+?) \| (.+?) \| (.+?) \|$',plan,re.M)
cand=(ROOT/'docs/research/excerpt-candidates.md').read_text(encoding='utf-8')
cands=dict(re.findall(r'^\| `(gsk-[a-z0-9-]+)` \| .+? \| (.*?) \|$',cand,re.M))
CN={'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'十一':11,'十二':12,'十三':13,'十四':14,'十五':15,'十六':16,'十七':17,'十八':18,'十九':19,'二十':20,'二十一':21,'二十二':22,'二十三':23,'二十四':24}
def cnnum(s):
    if s.isdigit(): return int(s)
    if s in CN: return CN[s]
    if s.startswith('十'): return 10+CN.get(s[1:],0)
    return None
def cndigit(n):
    d='零一二三四五六七八九'
    if n<10: return d[n]
    if n<20: return '十'+(d[n%10] if n%10 else '')
    return d[n//10]+'十'+(d[n%10] if n%10 else '')
def src_for(ku,loc):
    if ku.startswith('gsk-eu-annex3'): return ROOT/'docs/research/sources/eu/annex-3.md', 'ANNEX III'
    if ku.startswith('gsk-eu-'):
        n=ku.split('art')[1].split('-')[0]
        return ROOT/'docs/research/sources/eu'/f'article-{n}.md', f'Article {n}'
    if ku.startswith('gsk-cn-genai-'):
        n=cnnum(ku.split('art')[1]); return ROOT/'docs/research/sources/cn/genai-measures-2023.md', f'第{cndigit(n)}条'
    if ku.startswith('gsk-cn-label-'):
        n=cnnum(ku.split('art')[1]); return ROOT/'docs/research/sources/cn/label-measures-2025.md', f'第{cndigit(n)}条'
    return None,None
def norm(s):
    s=re.sub(r'\s+',' ',s).strip()
    s=re.sub(r'(?<=[\u4e00-\u9fff，。；：、（）《》“”‘’！？])\s+(?=[\u4e00-\u9fff，。；：、（）《》“”‘’！？])','',s)
    return s
bad=[]; okn=0
for ku,loc,title,nat in rows:
    f,needle=src_for(ku,loc)
    if not f or not f.exists(): bad.append((ku,'missing source file',str(f))); continue
    txt=norm(f.read_text(encoding='utf-8'))
    if needle not in txt: bad.append((ku,'locator not in source',needle)); continue
    c=norm(cands.get(ku,''))
    if not c or c.startswith('（W1'): bad.append((ku,'no candidate',c[:20])); continue
    # 候选前 60 字符应出现在全文（去掉截断标记）
    head=c[:60]
    if head not in txt: bad.append((ku,'candidate head not in source',head)); continue
    okn+=1
print(f'rows={len(rows)} ok={okn} bad={len(bad)}')
for b in bad[:20]: print('FAIL',b)
sys.exit(0 if not bad else 1)
