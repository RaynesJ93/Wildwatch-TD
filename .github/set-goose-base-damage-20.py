from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
pattern=r'(goose:\{name:"Goose"[^\n]*?dmg:)(\d+(?:\.\d+)?)'
new,n=re.subn(pattern,r'\g<1>20',s,count=1)
if n!=1:
    raise SystemExit(f'Expected 1 Goose damage match, found {n}')
if new==s:
    raise SystemExit('Goose damage already 20 or no change made')
p.write_text(new,encoding='utf-8')
print('Set Goose base damage to 20')
