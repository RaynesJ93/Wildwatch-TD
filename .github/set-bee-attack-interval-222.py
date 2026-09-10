from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
pattern=r'(bee:\{name:"Bee",emoji:"🐝",rarity:"Common",cost:55,range:165,rate:)([^,]+)(,dmg:6,)'
s,n=re.subn(pattern,r'\g<1>2.22\g<3>',s,count=1)
if n!=1: raise SystemExit(f'Expected one Bee rate replacement, got {n}')
p.write_text(s,encoding='utf-8')
