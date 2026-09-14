from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='kills*0.20'
count=s.count(old)
if count < 1:
    raise SystemExit('Expected card kill XP expression not found')
s=s.replace(old,'kills*0.60')
p.write_text(s,encoding='utf-8')
print(f'Updated {count} card kill XP expressions from 0.20 to 0.60')
