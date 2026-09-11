from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls={
'Math.floor(a.cost*.595*selectedTower.level)':'Math.floor(a.cost*.595*selectedTower.level*(selectedTower.key==="pig"?.8:1))',
'Math.floor(a.cost*.595*t.level)':'Math.floor(a.cost*.595*t.level*(t.key==="pig"?.8:1))'
}
changed=0
for old,new in repls.items():
    count=s.count(old)
    if count:
        s=s.replace(old,new)
        changed+=count
if changed!=3:
    raise SystemExit(f'Expected 3 Pig upgrade-cost formula replacements, got {changed}')
p.write_text(s,encoding='utf-8')
print('Pig tower upgrade costs reduced by 20% at every upgrade level')
