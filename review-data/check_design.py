#!/usr/bin/env python3
"""设计期一致性检查（不是产品代码）：校验 v0.2 的 locator/KU 样例/数字/文档一致性。
用法：python3 scripts/check_design.py
退出码：0 全 PASS；1 有 FAIL。
"""
import json,re,sys,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
fails=[]; oks=[]

def ok(m): oks.append(m)
def fail(m): fails.append(m)

# 1) ku-plan
plan=(ROOT/'docs/research/ku-plan.md').read_text(encoding='utf-8')
rows=re.findall(r'^\| \d+ \| (gsk-[a-z0-9-]+) \| (.+?) \| (.+?) \| (.+?) \|$',plan,re.M)
eu=[r for r in rows if r[0].startswith('gsk-eu')]; cn=[r for r in rows if r[0].startswith('gsk-cn')]
ok(f'ku-plan rows={len(rows)} eu={len(eu)} cn={len(cn)}') if len(rows)==52 and len(eu)==32 and len(cn)==20 else fail(f'ku-plan counts rows={len(rows)} eu={len(eu)} cn={len(cn)} (want 52/32/20)')
ids=[r[0] for r in rows]
ok('ku_id unique') if len(ids)==len(set(ids)) else fail('ku_id duplicate')
forms=[r'^Art\.\d+((\(\d+\))|(\([a-z]{1,3}\))){0,4}$',r'^(§|Section )?\d+(\.\d+)*$',r'^[A-Z][A-Za-z0-9 ,.-]{2,60}$',r'^p\.\d+$',r'^\(\w+\)$',r'^第[一二三四五六七八九十百零〇\d]+条(第[一二三四五六七八九十百零〇\d]+款)?(第[一二三四五六七八九十百零〇\d]+项)?$',r'^Annex [IVX]+( point \d+)?(\([a-z]\))?$']
bad=[(r[0],r[1]) for r in rows if not any(re.match(p,r[1]) for p in forms)]
ok('locator all match 7 forms') if not bad else fail(f'locator invalid: {bad[:5]}')
ex=(ROOT/'docs/research/excerpt-candidates.md').read_text(encoding='utf-8')
exids=set(re.findall(r'gsk-[a-z0-9-]+',ex))
ok('excerpt ids == plan ids') if exids==set(ids) else fail(f'excerpt ids mismatch: missing={set(ids)-exids} extra={exids-set(ids)}')

# 2) sample KUs
import yaml
for f in ['docs/research/sample-kus/gsk-eu-art14.yaml','docs/research/sample-kus/gsk-cn-genai-art7.yaml']:
    d=yaml.safe_load((ROOT/f).read_text(encoding='utf-8'))
    n=len([k for k in d if k!='gap'])
    ok(f'{f}: 29 fields') if n==29 else fail(f'{f}: fields={n}')
    ex=d['verbatim_excerpt']
    badob=[o['id'] for o in d['obligation'] if o['text'] not in ex]
    ok(f'{f}: obligations substring') if not badob else fail(f'{f}: obligations not substring {badob}')
    if d['status']=='draft' and not d.get('gap'): fail(f'{f}: draft but empty gap')
    ok(f'{f}: gap/status ok') if d.get('gap') or d['status']!='draft' else fail(f'{f}: gap/status')
    anyl=any(re.match(p,d['locator']) for p in forms)
    ok(f'{f}: locator {d["locator"]}') if anyl else fail(f'{f}: locator invalid {d["locator"]}')
    (ok if str(d.get('registry_id','')).startswith('reg-') else fail)(f'{f}: registry_id source-level')
    (ok if str(d.get('fingerprint',''))!='minhash96:'+'0'*95+'1' else fail)(f'{f}: fingerprint not shared placeholder')

# 3) design markers
dsg=(ROOT/'docs/specs/2026-10-31-grc-skill-agent-design-v0.8.md').read_text(encoding='utf-8')
markers=['7 形态','只选句','final_text','validation_token','server_nonce','REQUIRED_SENTENCE','CONCLUSION_FORBIDDEN','conclusion_terms','issued_vs_validated','全文快照','不随包','verification_mode','verification_path','absence_kind','absence_terms','scope_note_codes','CK-16','coverage_codes','out_of_scope','backlog','groups','CK-14','CK-15','评估','Art.5 选 7 项','= **32**','16–19 人日','4 周','W4','无机器译文','scope_correction']
for m in markers:
    (ok if m in dsg else fail)(f'design marker: {m}')
for badstr in ['只存摘录','不重分发全文','Art.53–55','宿主成文','determination.yaml','determination.md','Art.5 选 5 项','insufficient_profile','零第三方运行时依赖','v0.4 决定','双人核','#Art.14(1)','binding_mode: translation','三模式','3 周内','四态']:
    (ok if badstr not in dsg else fail)(f'design stale: {badstr}')
# section order 1.1..1.4
order=[i for i in range(1,5) if re.search(rf'^### 1\.{i} ',dsg,re.M)]
ok('sections 1.1-1.4 present') if order==[1,2,4,3] or order==[1,2,3,4] else fail(f'section 1.x order={order}')

# 4) answer contract keys
for k in ['"claims"','"binding_mode"','"support_type"','"verification_url"','"verified_by"','"partial_reason"','groups','scope_correction']:
    (ok if k in dsg else fail)(f'answer field {k}')
# 5) impact matrix
im=(ROOT/'docs/impact-matrix.md').read_text(encoding='utf-8')
for p in re.findall(r'`(evidence/[^`]+)`',im):
    (ok if (ROOT/p).exists() else fail)(f'evidence exists: {p}')

# 6) golden / aliases / scope exclusions / sources
try:
    gd=yaml.safe_load((ROOT/'docs/research/golden-draft.yaml').read_text(encoding='utf-8'))
    g=gd.get('golden',[]); adv=gd.get('adversarial',[])
    (ok if len(g)==20 else fail)(f'golden count={len(g)} (want 20)')
    (ok if len(adv)==5 else fail)(f'adversarial count={len(adv)} (want 5)')
    planids=set(ids)
    refs=[k for q in g for k in q.get('expected_ku_ids',[])+q.get('retrieval_expect',[])]
    unknown=sorted(set(refs)-planids)
    (ok if not unknown else fail)(f'golden unknown ku_ids: {unknown[:5]}')
    (ok if all(q.get('expected_mode') in ('answer','partial','refuse') for q in g) else fail)('golden modes valid')
    (ok if all(q.get('partial_reason') for q in g if q.get('expected_mode')=='partial') else fail)('golden partial_reason missing')
    (ok if all(q.get('expected_refusal_reason') for q in g if q.get('expected_mode')=='refuse') else fail)('golden refusal_reason missing')
except Exception as e:
    fail(f'golden draft check: {e}')
try:
    al=yaml.safe_load((ROOT/'docs/research/aliases-draft.yaml').read_text(encoding='utf-8'))
    need=set(ids); have=set(al.get('aliases',{}))
    (ok if need==have else fail)(f'aliases mismatch missing={sorted(need-have)[:5]} extra={sorted(have-need)[:5]}')
    weak=[k for k,v in al.get('aliases',{}).items() if not any(re.search(r'[\u4e00-\u9fff]',x) for x in v) or not any(re.search(r'[A-Za-z]',x) for x in v)]
    (ok if not weak else fail)(f'aliases zh/en weak: {weak[:5]}')
except Exception as e:
    fail(f'aliases check: {e}')
try:
    sx=yaml.safe_load((ROOT/'docs/research/scope-exclusions-draft.yaml').read_text(encoding='utf-8'))
    (ok if len(sx)>=3 else fail)(f'scope exclusions count={len(sx)} (want >=3)')
    (ok if all(x.get('id') and x.get('registry_id') and x.get('as_of') for x in sx) else fail)('scope exclusion fields missing')
except Exception as e:
    fail(f'scope exclusions check: {e}')
srcs=[p for p in (ROOT/'docs/research/sources').rglob('*.md') if p.name!='README.md']
(ok if len(srcs)==20 else fail)(f'sources fulltext count={len(srcs)} (want 20)')

print('== design check ==')
for m in oks: print('PASS',m)
for m in fails: print('FAIL',m)
print(f'\nRESULT: {"PASS" if not fails else "FAIL"}  ({len(oks)} pass / {len(fails)} fail)')
sys.exit(0 if not fails else 1)
