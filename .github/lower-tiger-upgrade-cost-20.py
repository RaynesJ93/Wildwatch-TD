from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='(selectedTower.key==="pig"?.8:1)'
new='((selectedTower.key==="pig"||selectedTower.key==="tiger")?.8:1)'
old2='(t.key==="pig"?.8:1)'
new2='((t.key==="pig"||t.key==="tiger")?.8:1)'
count=s.count(old)+s.count(old2)
if count<2:
    raise SystemExit(f'Expected Pig upgrade-cost formulas, found {count}')
s=s.replace(old,new).replace(old2,new2)
if 'selectedTower.key==="tiger"' not in s or 't.key==="tiger"' not in s:
    raise SystemExit('Tiger cost reduction not applied to all formulas')
p.write_text(s,encoding='utf-8')
print('Tiger tower upgrades are now 20% cheaper at every level')
