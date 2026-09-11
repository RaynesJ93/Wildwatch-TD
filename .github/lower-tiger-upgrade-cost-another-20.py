from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Tiger already has a 0.8 multiplier. Another 20% reduction means 0.8 * 0.8 = 0.64 of the original upgrade price.
old='((selectedTower.key==="pig"||selectedTower.key==="tiger")?.8:1)'
new='(selectedTower.key==="pig"?.8:selectedTower.key==="tiger"?.64:1)'
old2='((t.key==="pig"||t.key==="tiger")?.8:1)'
new2='(t.key==="pig"?.8:t.key==="tiger"?.64:1)'
count=s.count(old)+s.count(old2)
if count<2:
    raise SystemExit(f'Expected current Tiger 20% discount formulas, found {count}')
s=s.replace(old,new).replace(old2,new2)
if 'selectedTower.key==="tiger"?.64' not in s or 't.key==="tiger"?.64' not in s:
    raise SystemExit('Second Tiger discount not applied everywhere')
p.write_text(s,encoding='utf-8')
print('Tiger upgrade prices are now 64% of original (20% cheaper, then another 20% cheaper)')
