from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
import re
pattern=r'(bee:\{name:"Bee",emoji:"🐝",rarity:"Common",cost:55,range:165,rate:)([^,]+)(,dmg:15,)'
m=re.search(pattern,s)
if not m: raise SystemExit('Current Bee stats marker not found')
s,n=re.subn(pattern,r'\g<1>3.22\g<3>',s,count=1)
if n!=1: raise SystemExit(f'Expected one Bee replacement, got {n}')
p.write_text(s,encoding='utf-8')
