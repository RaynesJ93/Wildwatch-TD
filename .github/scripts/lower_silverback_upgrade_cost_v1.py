from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='SILVERBACK_UPGRADE_COST_V1'
if marker in s:
    print('Already applied'); raise SystemExit(0)
old='selectedTower.key==="pig"?.8:selectedTower.key==="tiger"?.64:.65'
new='selectedTower.key==="pig"?.8:selectedTower.key==="tiger"?.64:selectedTower.key==="silverback"?.45:.65'
count=s.count(old)
if count!=2: raise RuntimeError(f'Expected 2 selectedTower upgrade cost anchors, found {count}')
s=s.replace(old,new)
old2='t.key==="pig"?.8:t.key==="tiger"?.64:.65'
new2='t.key==="pig"?.8:t.key==="tiger"?.64:t.key==="silverback"?.45:.65'
if old2 not in s: raise RuntimeError('Tower modal upgrade cost anchor not found')
s=s.replace(old2,new2,1)
# Add marker near first formula
s=s.replace('const mult=selectedTower.key==="pig"?.8:selectedTower.key==="tiger"?.64:selectedTower.key==="silverback"?.45:.65;', '// SILVERBACK_UPGRADE_COST_V1: Silverback uses a reduced 0.45 upgrade multiplier.\n    const mult=selectedTower.key==="pig"?.8:selectedTower.key==="tiger"?.64:selectedTower.key==="silverback"?.45:.65;',1)
p.write_text(s,encoding='utf-8')
print('Lowered Silverback Gorilla tower upgrade costs')
