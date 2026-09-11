from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='const raccoonSpecial=cardLevel(t.key)>=10;'
new='const raccoonSpecial=t.level>=10;'
if old not in s: raise SystemExit('Raccoon special level check marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
