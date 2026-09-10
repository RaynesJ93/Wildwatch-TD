from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
pat=r'(bee:\{name:"Bee"[^\n]*?rate:)1/1\.55(,dmg:15,)'
new=r'\g<1>1/0.62\2'
s2,n=re.subn(pat,new,s,count=1)
if n!=1:
    raise SystemExit(f'Expected to update exactly 1 Bee rate entry, updated {n}')
p.write_text(s2)
